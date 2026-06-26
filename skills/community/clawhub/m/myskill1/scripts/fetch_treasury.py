#!/usr/bin/env python3
"""
US 10-Year Treasury Yield Tracker
从 CNBC 和 Treasury.gov 抓取数据，写入 CSV，并记录极简日志
"""

import requests
import re
import csv
import os
from datetime import datetime

# 文件路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
DATA_FILE = os.path.join(SCRIPT_DIR, "../../../testdata/us_treasury_10y.csv")
LOG_DIR = os.path.join(SKILL_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "fetch.log")

# 确保目录存在
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


def fetch_cnbc_10y():
    """
    从 CNBC 抓取 US10Y 数据
    返回：(yield, change) 或 (None, None)
    """
    url = 'https://www.cnbc.com/quotes/US10Y'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 直接用正则提取 last 和 change
        last_match = re.search(r'"last":\s*"([^"]+)"', response.text)
        change_match = re.search(r'"change":\s*"([^"]+)"', response.text)

        if last_match:
            last_yield = last_match.group(1)  # 如 "4.334%"
            change = change_match.group(1) if change_match else None

            # 去掉 % 符号
            yield_value = last_yield.replace('%', '').strip()
            print(f"✅ CNBC: Yield={yield_value}%, Change={change}")
            return yield_value, change
        else:
            print("⚠️ CNBC: 未找到 yield 数据")
            return None, None

    except Exception as e:
        print(f"❌ CNBC 抓取失败：{e}")
        return None, None


def fetch_treasury_10y():
    """
    从 Treasury.gov 抓取 10YR 数据
    返回：yield 或 None
    """
    url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 查找表格
        table_match = re.search(r'<table.*?</table>', response.text, re.DOTALL)
        if not table_match:
            print("⚠️ Treasury.gov: 未找到表格")
            return None

        table = table_match.group(0)

        # 找所有行
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table, re.DOTALL)
        print(f"   找到 {len(rows)} 行")

        # 找 10 Yr 列索引
        yr10_index = 23

        # 找第一行有效数据
        for i, row in enumerate(rows[1:5]):  # 只检查前几行
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
            if len(cells) > yr10_index:
                date_cell = re.sub(r'<[^>]+>', '', cells[0]).strip()
                yr10_cell = re.sub(r'<[^>]+>', '', cells[yr10_index]).strip()
                print(f"   行 {i+1}: Date={date_cell[:20]}, 10Y={yr10_cell}")

                # 检查是否是有效数据
                if re.match(r'\d', date_cell) and re.match(r'[\d.]+', yr10_cell):
                    print(f"✅ Treasury.gov: Yield={yr10_cell}%")
                    return yr10_cell

        print("⚠️ Treasury.gov: 未找到有效数据")
        return None

    except Exception as e:
        print(f"❌ Treasury.gov 抓取失败：{e}")
        return None


def get_today_str():
    """获取今天的日期字符串（YYYY-MM-DD）"""
    return datetime.now().strftime('%Y-%m-%d')


def get_run_timestamp():
    """获取当前执行时间字符串"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def write_log(action, status, cnbc_yield, treasury_yield):
    """写入极简日志"""
    log_line = (
        f"{get_run_timestamp()} | {action} | {status} | "
        f"cnbc={cnbc_yield or 'N/A'} treasury={treasury_yield or 'N/A'}\n"
    )
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line)
    print(f"📝 日志已写入：{LOG_FILE}")


def write_to_csv(cnbc_yield, treasury_yield):
    """
    写入 CSV 文件
    如果今天已存在，覆盖该行；否则追加新行
    返回：append 或 overwrite
    """
    today = get_today_str()

    # 读取现有数据
    rows = []
    today_exists = False

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            if header:
                rows.append(header)

            for row in reader:
                if row and row[0] == today:
                    # 覆盖今天的行
                    row = [today, cnbc_yield or 'N/A', treasury_yield or 'N/A']
                    today_exists = True
                rows.append(row)

    action = 'overwrite' if today_exists else 'append'

    # 如果今天不存在，追加新行
    if not today_exists:
        if not rows:
            rows.append(['Date', 'CNBC_10Y', 'Treasury_10Y'])
        rows.append([today, cnbc_yield or 'N/A', treasury_yield or 'N/A'])

    # 写入文件
    with open(DATA_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ 数据已写入：{DATA_FILE}")
    print(f"   日期：{today}")
    print(f"   动作：{action}")
    print(f"   CNBC: {cnbc_yield or 'N/A'}%")
    print(f"   Treasury: {treasury_yield or 'N/A'}%")
    return action


def get_status(cnbc_yield, treasury_yield):
    """根据抓取结果生成极简状态"""
    if cnbc_yield and treasury_yield:
        return 'success'
    if cnbc_yield or treasury_yield:
        return 'partial'
    return 'fail'


def main():
    print('🔍 开始抓取美国 10 年期国债利率数据...')
    print('=' * 60)

    # 抓取 CNBC 数据
    print('\n1. 抓取 CNBC US10Y...')
    cnbc_yield, _ = fetch_cnbc_10y()

    # 抓取 Treasury.gov 数据
    print('\n2. 抓取 Treasury.gov...')
    treasury_yield = fetch_treasury_10y()

    # 写入 CSV
    print('\n3. 写入 CSV...')
    action = write_to_csv(cnbc_yield, treasury_yield)

    # 写入日志
    print('\n4. 写入日志...')
    status = get_status(cnbc_yield, treasury_yield)
    write_log(action, status, cnbc_yield, treasury_yield)

    print('\n✅ 完成')


if __name__ == "__main__":
    main()
