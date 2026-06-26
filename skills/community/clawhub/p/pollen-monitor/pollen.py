#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
花粉浓度查询脚本 v1.0.0
用法：python pollen.py [城市拼音] [城市中文名]
示例：python pollen.py beijing 北京

支持范围：仅支持中国大陆 53 个城市
数据来源：中国天气网 & 全国医院联合发布
"""

__version__ = "1.0.0"

import sys
import subprocess
import json
from datetime import datetime, timedelta

def get_date_range():
    """获取 7 天前到今天的日期范围"""
    end = datetime.now()
    start = end - timedelta(days=7)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

def fetch_pollen_data(city_en, start, end):
    """调用 API 获取花粉数据"""
    url = f"https://graph.weatherdt.com/ty/pollen/v2/hfindex.html?eletype=1&city={city_en}&start={start}&end={end}&predictFlag=true"
    
    try:
        result = subprocess.run(
            ['curl', '-s', url],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except Exception as e:
        print(f"❌ 获取数据失败：{e}")
        sys.exit(1)
    
    return None

def get_emoji(level_code):
    """根据等级代码返回 emoji"""
    emojis = {
        "-1": "⚪",
        "0": "⚪",
        "1": "🟢",
        "2": "🟡", 
        "3": "🟠",
        "4": "🔴",
        "5": "🔴🔴"
    }
    return emojis.get(str(level_code), "⚪")

def main():
    # 版本查询
    if len(sys.argv) > 1 and sys.argv[1] in ['-v', '--version', 'version']:
        print(f"pollen-monitor v{__version__}")
        sys.exit(0)
    
    # 默认北京
    city_en = sys.argv[1] if len(sys.argv) > 1 else "beijing"
    city_cn = sys.argv[2] if len(sys.argv) > 2 else "北京"
    
    # 获取日期范围
    start, end = get_date_range()
    
    # 获取数据
    data = fetch_pollen_data(city_en, start, end)
    
    if not data:
        print("❌ 获取花粉数据失败")
        print("💡 提示：该城市可能不在支持列表中，仅支持中国大陆 53 个城市")
        print("📋 查询链接：https://m.weather.com.cn/huafen/index.html?id=101010100")
        sys.exit(1)
    
    # 检查是否返回有效数据
    if not data.get('dataList') or len(data.get('dataList', [])) < 2:
        print(f"❌ {city_cn} 暂无花粉监测数据")
        print("💡 提示：该城市可能不在支持列表中，仅支持中国大陆 53 个城市")
        print("📋 查询链接：https://m.weather.com.cn/huafen/index.html?id=101010100")
        sys.exit(1)
    
    # 检查是否所有数据都是"暂无"（海外城市或不支持的城市）
    data_list = sorted(data.get('dataList', []), key=lambda x: x.get('addTime', ''))
    all_empty = all(d.get('levelCode', 0) in [-1, 0] or not d.get('level') for d in data_list)
    if all_empty:
        print(f"❌ {city_cn} 不在支持列表中")
        print("💡 提示：本技能仅支持中国大陆 53 个城市")
        print("📋 查询支持的城市列表：https://m.weather.com.cn/huafen/index.html?id=101010100")
        sys.exit(1)
    
    # 解析数据
    season_name = data.get('seasonLevelName', '花粉季')
    data_list = sorted(data.get('dataList', []), key=lambda x: x.get('addTime', ''))
    
    if len(data_list) < 2:
        print("❌ 数据不足")
        sys.exit(1)
    
    # 今天的数据（倒数第二个）
    today = data_list[-2]
    today_level = today.get('level', '未知')
    today_level_code = today.get('levelCode', '0')
    today_msg = today.get('levelMsg', '无数据')
    today_date = today.get('addTime', '未知')
    today_week = today.get('week', '未知')
    
    # 明天的数据（最后一个，预报）
    tomorrow = data_list[-1]
    tomorrow_level = tomorrow.get('level', '未知')
    tomorrow_level_code = tomorrow.get('levelCode', '0')
    tomorrow_msg = tomorrow.get('levelMsg', '无数据')
    tomorrow_date = tomorrow.get('addTime', '未知')
    tomorrow_week = tomorrow.get('week', '未知')
    
    # 输出结果
    print("🌸 {} 花粉浓度报告".format(city_cn))
    print("━" * 30)
    print("季节：{}花粉季".format(season_name))
    print()
    print("📅 {} ({})".format(today_week, today_date))
    print("   等级：{} {}".format(get_emoji(today_level_code), today_level))
    print("   建议：{}".format(today_msg))
    print()
    print("📅 {} ({}) 预报".format(tomorrow_week, tomorrow_date))
    print("   等级：{} {}".format(get_emoji(tomorrow_level_code), tomorrow_level))
    print("   建议：{}".format(tomorrow_msg))
    print()
    print("━" * 30)
    print("💡 数据来源：中国天气网 & 全国医院联合发布")
    print("🕐 更新时间：每日 08:00")

if __name__ == '__main__':
    main()
