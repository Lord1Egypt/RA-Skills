#!/usr/bin/env python3
"""
股票行情获取 - 调试版本
测试各个数据源的连通性
"""

import requests
import time
from datetime import datetime

symbol = '600769'
market = 'sh' if symbol.startswith('6') else 'sz'

print(f"测试股票：{symbol}\n")
print("="*70 + "\n")

# 测试 1：腾讯财经
print("1️⃣ 腾讯财经...")
try:
    url = f"http://qt.gtimg.cn/q={market}{symbol}"
    print(f"   URL: {url}")
    start = time.time()
    response = requests.get(url, timeout=5)
    elapsed = time.time() - start
    print(f"   状态码：{response.status_code}")
    print(f"   耗时：{elapsed:.2f}s")
    print(f"   内容长度：{len(response.text)}")
    if response.status_code == 200 and '=' in response.text:
        parts = response.text.split('"')[1].split('~')
        if len(parts) >= 50:
            print(f"   ✅ 成功！价格：¥{parts[3]}")
    else:
        print(f"   ❌ 解析失败")
except Exception as e:
    print(f"   ❌ 错误：{e}")

print("\n" + "="*70 + "\n")

# 测试 2：新浪财经
print("2️⃣ 新浪财经...")
try:
    url = f"http://hq.sinajs.cn/list={market}{symbol}"
    print(f"   URL: {url}")
    start = time.time()
    response = requests.get(url, timeout=5)
    elapsed = time.time() - start
    print(f"   状态码：{response.status_code}")
    print(f"   耗时：{elapsed:.2f}s")
    print(f"   内容长度：{len(response.text)}")
    if response.status_code == 200 and '=' in response.text:
        parts = response.text.split('=')[1].strip('"').split(',')
        if len(parts) >= 32:
            print(f"   ✅ 成功！价格：¥{parts[3]}")
    else:
        print(f"   ❌ 解析失败")
except Exception as e:
    print(f"   ❌ 错误：{e}")

print("\n" + "="*70 + "\n")

# 测试 3：东方财富
print("3️⃣ 东方财富...")
try:
    market_code = '1' if symbol.startswith('6') else '0'
    url = "http://push2.eastmoney.com/api/qt/stock/get"
    params = {
        'secid': f'{market_code}.{symbol}',
        'fields': 'f57,f58,f2,f3,f4'
    }
    print(f"   URL: {url}")
    print(f"   参数：{params}")
    start = time.time()
    response = requests.get(url, params=params, timeout=5)
    elapsed = time.time() - start
    print(f"   状态码：{response.status_code}")
    print(f"   耗时：{elapsed:.2f}s")
    print(f"   内容长度：{len(response.text)}")
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            d = data['data']
            print(f"   ✅ 成功！价格：¥{d.get('f2', 0)}")
        else:
            print(f"   ❌ 无数据")
    else:
        print(f"   ❌ 请求失败")
except Exception as e:
    print(f"   ❌ 错误：{e}")

print("\n" + "="*70 + "\n")

# 测试 4：网易财经
print("4️⃣ 网易财经...")
try:
    market_code = '0' if symbol.startswith('6') else '1'
    url = f"http://api.money.126.net/data/feed/{market_code}{symbol},money.api"
    print(f"   URL: {url}")
    start = time.time()
    response = requests.get(url, timeout=5)
    elapsed = time.time() - start
    print(f"   状态码：{response.status_code}")
    print(f"   耗时：{elapsed:.2f}s")
    print(f"   内容长度：{len(response.text)}")
    if response.status_code == 200:
        text = response.text.replace('_ntes_quote_callback(', '').rstrip(')')
        import json
        data = json.loads(text)
        if data.get('data'):
            d = data['data'][f'{market_code}{symbol}']
            print(f"   ✅ 成功！价格：¥{d.get('price', 0)}")
        else:
            print(f"   ❌ 无数据")
    else:
        print(f"   ❌ 请求失败")
except Exception as e:
    print(f"   ❌ 错误：{e}")

print("\n" + "="*70 + "\n")

# 测试 5：雪球财经
print("5️⃣ 雪球财经...")
try:
    market_code = 'SH' if symbol.startswith('6') else 'SZ'
    url = f"https://stock.xueqiu.com/v5/stock/quote.json?symbol={market_code}{symbol}"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://xueqiu.com/'
    }
    print(f"   URL: {url}")
    start = time.time()
    response = requests.get(url, headers=headers, timeout=5)
    elapsed = time.time() - start
    print(f"   状态码：{response.status_code}")
    print(f"   耗时：{elapsed:.2f}s")
    print(f"   内容长度：{len(response.text)}")
    if response.status_code == 200:
        data = response.json()
        if data.get('data') and data['data'].get('quote'):
            d = data['data']['quote']
            print(f"   ✅ 成功！价格：¥{d.get('current', 0)}")
        else:
            print(f"   ❌ 无数据")
    else:
        print(f"   ❌ 请求失败")
except Exception as e:
    print(f"   ❌ 错误：{e}")

print("\n" + "="*70 + "\n")

# 测试 6：百度股市通
print("6️⃣ 百度股市通...")
try:
    url = f"https://finance.pae.baidu.com/api/getstockinfo"
    params = {
        'symbol': f'{market}{symbol}',
        'type': 'stock'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://gushitong.baidu.com/'
    }
    print(f"   URL: {url}")
    start = time.time()
    response = requests.get(url, params=params, headers=headers, timeout=5)
    elapsed = time.time() - start
    print(f"   状态码：{response.status_code}")
    print(f"   耗时：{elapsed:.2f}s")
    print(f"   内容长度：{len(response.text)}")
    if response.status_code == 200:
        data = response.json()
        if data.get('Result'):
            d = data['Result']
            print(f"   ✅ 成功！价格：¥{d.get('price', 0)}")
        else:
            print(f"   ❌ 无数据")
    else:
        print(f"   ❌ 请求失败")
except Exception as e:
    print(f"   ❌ 错误：{e}")

print("\n" + "="*70)
print(f"\n测试完成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
