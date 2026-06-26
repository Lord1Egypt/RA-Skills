#!/usr/bin/env python3
"""
腾讯财经API - 精确获取ETF历史成交额
qt[37] = 成交额(万元)
"""
import requests
import json
import csv
import os
from collections import defaultdict

HISTORY_FILE = "/Users/amitabhama/Downloads/etf_history.csv"

ETF_LIST = {
    "sh510300": ("510300", "沪深300ETF"),
    "sh510050": ("510050", "上证50ETF"),
    "sh510500": ("510500", "中证500ETF"),
    "sh588000": ("588000", "科创50ETF"),
    "sh512100": ("512100", "中证1000ETF"),
    "sh512000": ("512000", "券商ETF"),
    "sh515880": ("515880", "通信ETF"),
    "sh512880": ("512880", "证券ETF"),
}

def get_qq_etf_data(symbol, days=30):
    """获取ETF历史数据"""
    url = "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
    params = {'_var': 'kline_dayqfq', 'param': f'{symbol},day,,,{days},qfq'}
    
    try:
        response = requests.get(url, params=params, timeout=15)
        text = response.text
        
        if '=' in text:
            data = json.loads(text.split('=')[1])
            
            if symbol in data.get('data', {}):
                stock_data = data['data'][symbol]
                klines = stock_data.get('qfqday') or stock_data.get('day', [])
                qt = stock_data.get('qt', {}).get(symbol, [])
                
                # 从qt获取今日数据 qt[37] = 成交额(万元)
                today_vol = 0
                today_amount = 0
                if len(qt) > 37:
                    try:
                        today_vol = float(qt[6])  # 成交量(股)
                        today_amount = float(qt[37]) / 10000  # 万元转亿元
                    except: pass
                
                result = []
                for i, d in enumerate(klines):
                    if len(d) >= 6:
                        date = d[0]
                        close_p = float(d[2])
                        high = float(d[3])
                        low = float(d[4])
                        vol = float(d[5])
                        
                        # 估算成交额 = 均价 * 成交量 / 1亿
                        avg_p = (high + low) / 2
                        amount = avg_p * vol / 1e8
                        
                        # 涨跌幅
                        if i > 0:
                            prev = float(klines[i-1][2])
                            change = (close_p - prev) / prev * 100
                        else:
                            change = 0
                        
                        # 最后一天用准确值
                        if i == len(klines) - 1 and today_amount > 0:
                            amount = today_amount
                            vol = today_vol
                        
                        vol_wan = vol / 10000
                        
                        result.append({
                            'date': date,
                            'price': close_p,
                            'change': change,
                            'volume': vol_wan,
                            'amount': amount
                        })
                
                return result
        
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None

def init_history_file():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'code', 'name', 'price', 'change', 'volume', 'amount'])

def save_to_history(date, code, name, price, change, volume, amount):
    existing = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            reader = csv.DictReader(f)
            existing = list(reader)
    
    exists = any(row['date'] == date and row['code'] == code for row in existing)
    
    if not exists:
        with open(HISTORY_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([date, code, name, price, change, volume, amount])

def main():
    print("=" * 70)
    print("🏛️ 腾讯财经 - ETF历史成交额")
    print("=" * 70)
    
    init_history_file()
    all_data = []
    
    for symbol, (code, name) in ETF_LIST.items():
        print(f"\n📊 {code} {name}...", end=" ")
        
        data = get_qq_etf_data(symbol, 30)
        
        if not data:
            print("❌ 失败")
            continue
        
        print(f"✅ {len(data)}天")
        
        for d in data:
            save_to_history(d['date'], code, name, d['price'], 
                           f"{d['change']:.2f}%", f"{d['volume']:.2f}万", 
                           f"{d['amount']:.2f}")
            all_data.append({**d, 'code': code, 'name': name})
    
    # 近10天统计
    print("\n" + "=" * 70)
    print("📈 近10天平均成交额")
    print("=" * 70)
    
    etf_stats = defaultdict(list)
    for d in all_data:
        if d['date'] >= '2025-04-07':
            etf_stats[d['code']].append(d['amount'])
    
    for code in sorted(etf_stats.keys()):
        amounts = etf_stats[code]
        avg = sum(amounts) / len(amounts) if amounts else 0
        print(f"  {code}: {avg:.2f}亿")
    
    # 今日
    print("\n" + "=" * 70)
    print("📅 今日 (2026-04-17)")
    print("=" * 70)
    
    today = [d for d in all_data if d['date'] == '2026-04-17']
    for d in sorted(today, key=lambda x: x['amount'], reverse=True):
        print(f"  {d['code']}: {d['amount']:.2f}亿  {d['change']:+.2f}%")

if __name__ == "__main__":
    main()