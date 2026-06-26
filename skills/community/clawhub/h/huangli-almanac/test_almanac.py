#!/usr/bin/env python3
"""
黄历万年历测试脚本
验证 API 是否正常响应
"""

import requests
import json
from datetime import datetime, timedelta

# API 地址
API_BASE = "https://api.tiax.cn/almanac/"

def test_almanac(year, month, day):
    """查询指定日期的黄历信息"""
    url = f"{API_BASE}?year={year}&month={month}&day={day}"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        print(f"📅 查询：{year}-{month}-{day}")
        print("-" * 50)
        print(f"公历日期：{data.get('公历日期', 'N/A')}")
        print(f"农历日期：{data.get('农历日期', 'N/A')}")
        print(f"干支日期：{data.get('干支日期', 'N/A')}")
        print(f"五行纳音：{data.get('五行纳音', 'N/A')}")
        print(f"值日星神：{data.get('值日星神', 'N/A')}")
        print()
        print(f"宜：{data.get('宜', 'N/A')}")
        print(f"忌：{data.get('忌', 'N/A')}")
        print()
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}")
        return None

def test_today():
    """查询今天的黄历"""
    today = datetime.now()
    return test_almanac(today.year, today.month, today.day)

def test_tomorrow():
    """查询明天的黄历"""
    tomorrow = datetime.now() + timedelta(days=1)
    return test_almanac(tomorrow.year, tomorrow.month, tomorrow.day)

if __name__ == "__main__":
    print("=" * 50)
    print("黄历万年历测试")
    print("=" * 50)
    print()
    
    # 测试今天
    print("1️⃣  查询今天")
    test_today()
    
    print()
    
    # 测试明天
    print("2️⃣  查询明天")
    test_tomorrow()
    
    print()
    
    # 测试特定日期
    print("3️⃣  查询 2024 年 5 月 20 日")
    test_almanac(2024, 5, 20)
    
    print()
    
    # 测试特定日期
    print("4️⃣  查询 2023 年 3 月 2 日")
    test_almanac(2023, 3, 2)
