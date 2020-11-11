

# -*- coding: utf-8 -*-
import requests
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pymysql
import datetime


def auto():
    with open("/usr/local/code.txt", "r") as f:  # 打开文件
        data = f.read().replace("'", "")  # 读取文件
    today = datetime.date.today()
    yesterday = str(today - datetime.timedelta(days=1)).replace("-", "")
    alist = data.replace(" ", "").split(",")
    for i in range(0, len(alist)):
        print("i:", i)  # 打印当前写入进度
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='201410101bxp',
            db='Astock'
        )
        cursor = connection.cursor()
        headers = {
            "User-Agent": ":Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/86.0.4240.75 Safari/537.36"
        }
        stock_code0 = alist[i]
        stock_codesh = stock_code0.replace("SH", "0")
        stock_codehs = stock_codesh.replace("SZ", "1")
        url = "http://quotes.money.163.com/service/chddata.html?code=" + stock_codehs + "&start=" + yesterday +\
            "&end=" + yesterday + "&fields=TCLOSE;HIGH;LOW;TOPEN;CHG;PCHG;VOTURNOVER;VATURNOVER"
        try:
            response = requests.get(url.split('\n')[0], headers=headers)
            response.encoding = "gbk"
            response.raise_for_status()
        except BaseException:
            time.sleep(60)
            continue
        text_2 = response.text.replace(" ", "").split("\n")
        print(text_2)
        if len(text_2) < 3:
            continue
        if not text_2[1]:
            break
        for j in range(1, len(text_2) - 1):
            text_3 = text_2[j].replace(" ", "").split(",")
            if len(text_3) < 2:
                continue
            try:
                date = text_3[0]
            except BaseException:
                date = "0000-00-00"
            try:
                code = str(text_3[1]).replace("'", "")
            except BaseException:
                code = ""
            try:
                name = str(text_3[2])
            except BaseException:
                name = ""
            try:
                tclose = float(text_3[3])
            except BaseException:
                tclose = 0.0
            try:
                high = float(text_3[4])
            except BaseException:
                high = 0.0
            try:
                low = float(text_3[5])
            except BaseException:
                low = 0.0
            try:
                topen = float(text_3[6])
            except BaseException:
                topen = 0.0
            try:
                chg = float(text_3[7])
            except BaseException:
                chg = 0.0
            try:
                pchg = float(text_3[8])
            except BaseException:
                pchg = 0.0
            try:
                if len(str(text_3[9])) > 9:
                    voturnover = 0
                else:
                    voturnover = int(text_3[9])
            except BaseException:
                voturnover = 0
            try:
                vaturnover = float(text_3[10])
            except BaseException:
                vaturnover = 0.0
            data_temp = (date, code, name, tclose, high, low, topen, chg, pchg, voturnover, vaturnover)
            try:
                cursor.execute(
                    ("insert into stock{}(date,code,name,tclose,high,low,topen,chg,pchg,voturnover,vaturnover) "
                     "values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')".format(stock_code0)) % (data_temp))
                connection.commit()
            except BaseException:
                continue
        time.sleep(5)


sched = BlockingScheduler()
trigger = CronTrigger(hour=9, minute=30)
sched.add_job(auto, trigger)
sched.start()
