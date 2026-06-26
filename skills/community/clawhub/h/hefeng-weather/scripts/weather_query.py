#!/usr/bin/env python3
"""
和风天气查询技能
查询实时天气、逐小时预报、每日预报、分钟级降水

依赖：
  pip install requests

环境变量（优先）或配置文件（二选一）：
  export HEFENG_WEATHER_API_KEY="your-api-key"
  
  或创建 config.txt 填入 API Key

用法：
  python weather_query.py "城市名或ID" --type [now|hourly|daily|minutely]
  
示例：
  python weather_query.py "北京" --type now
  python weather_query.py "101010100" --type hourly
  python weather_query.py "上海" --type daily
  python weather_query.py "广州" --type minutely
"""

import os
import sys
import json
import argparse
import requests

# ========== 配置区 ==========
# 和风天气 API 基础 URL
API_BASE_URL = "https://devapi.qweather.com"

# 配置文件路径（skill 根目录，与 SKILL.md 说明一致）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)  # 父目录 = skill 根目录
CONFIG_FILE = os.path.join(SKILL_DIR, "config.txt")
# ========== 配置区结束 ==========

# 常用城市 ID 映射
CITY_IDS = {
    "北京": "101010100",
    "上海": "101020100",
    "广州": "101280101",
    "深圳": "101280601",
    "成都": "101270101",
    "武汉": "101200101",
    "杭州": "101210101",
    "南京": "101190101",
    "西安": "101110101",
    "重庆": "101040100",
    "天津": "101030100",
    "苏州": "101190401",
    "郑州": "101180101",
    "长沙": "101250101",
    "沈阳": "101070101",
    "青岛": "101120201",
    "大连": "101070201",
    "厦门": "101230201",
    "宁波": "101210401",
    "昆明": "101290101",
}


def get_api_key():
    """获取 API Key，优先级：环境变量 > 配置文件"""
    # 优先从环境变量读取
    api_key = os.environ.get("HEFENG_WEATHER_API_KEY")
    if api_key:
        return api_key
    
    # 其次从配置文件读取
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    return line
    
    print(f"错误：未找到 API Key", file=sys.stderr)
    print(f"请设置环境变量 HEFENG_WEATHER_API_KEY 或创建 {CONFIG_FILE}", file=sys.stderr)
    sys.exit(1)


def get_city_id(city):
    """获取城市 ID"""
    # 如果输入已经是数字，直接返回
    if city.isdigit():
        return city
    # 查找映射
    return CITY_IDS.get(city, city)


def query_weather(city, weather_type="now"):
    """查询天气"""
    api_key = get_api_key()
    city_id = get_city_id(city)
    
    endpoints = {
        "now": "/v7/weather/now",
        "hourly": "/v7/weather/24h",
        "daily": "/v7/weather/7d",
        "minutely": "/v7/minutely/15m",
    }
    
    endpoint = endpoints.get(weather_type, "/v7/weather/now")
    url = f"{API_BASE_URL}{endpoint}?location={city_id}&key={api_key}"
    
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        
        if data.get("code") != "200":
            return {"error": f"API返回错误: {data.get('code')}", "raw": data}
        
        return data
        
    except requests.exceptions.RequestException as e:
        return {"error": f"网络请求失败: {e}"}


def format_now(data):
    """格式化实时天气"""
    if "error" in data:
        return data["error"]
    
    now = data.get("now", {})
    result = []
    result.append(f"【实时天气】")
    result.append(f"天气：{now.get('text', '未知')}")
    result.append(f"温度：{now.get('temp', '?')}°C")
    result.append(f"体感：{now.get('feelsLike', '?')}°C")
    result.append(f"风力：{now.get('windDir', '')} {now.get('windScale', '')}级")
    result.append(f"风速：{now.get('windSpeed', '?')} km/h")
    result.append(f"湿度：{now.get('humidity', '?')}%")
    result.append(f"降水量：{now.get('precip', '0')} mm")
    result.append(f"能见度：{now.get('vis', '?')} km")
    result.append(f"气压：{now.get('pressure', '?')} hPa")
    
    return "\n".join(result)


def format_hourly(data):
    """格式化逐小时预报"""
    if "error" in data:
        return data["error"]
    
    result = []
    result.append(f"【逐小时预报】（未来24小时）")
    
    for i, hour in enumerate(data.get("hourly", [])[:24]):
        time = hour.get("fxTime", "")[11:16]
        temp = hour.get("temp", "?")
        text = hour.get("text", "?")
        wind = f"{hour.get('windDir', '')}{hour.get('windScale', '')}级"
        precip = hour.get("precip", "0")
        pop = hour.get("pop", "0")
        
        result.append(f"{time} | {temp}°C | {text:<6} | 降水: {precip}mm | 概率: {pop}% | {wind}")
    
    return "\n".join(result)


def format_daily(data):
    """格式化每日预报"""
    if "error" in data:
        return data["error"]
    
    result = []
    result.append(f"【每日预报】（未来7天）")
    
    for day in data.get("daily", []):
        date = day.get("fxDate", "")
        text_day = day.get("textDay", "?")
        text_night = day.get("textNight", "?")
        temp_max = day.get("tempMax", "?")
        temp_min = day.get("tempMin", "?")
        wind_dir = day.get("windDirDay", "?")
        wind_scale = day.get("windScaleDay", "?")
        precip = day.get("precip", "?")
        humidity = day.get("humidity", "?")
        
        result.append(f"{date} | {text_day}→{text_night} | {temp_min}°C~{temp_max}°C | 降水: {precip}mm | {wind_dir} {wind_scale}级")
    
    return "\n".join(result)


def format_minutely(data):
    """格式化分钟级降水"""
    if "error" in data:
        return data["error"]
    
    result = []
    minutely = data.get("minutely", {})
    summary = minutely.get("summary", "未来2小时无降水")
    
    result.append(f"【分钟级降水】")
    result.append(f"{summary}")
    
    # 只显示前12条（1小时）
    for m in minutely.get("minutely", [])[:12]:
        time = m.get("fxTime", "")[11:16]
        precip = m.get("precip", "0")
        result.append(f"{time} | 降水: {precip}mm")
    
    return "\n".join(result)


def main():
    parser = argparse.ArgumentParser(description="和风天气查询")
    parser.add_argument("city", help="城市名称或ID")
    parser.add_argument("--type", "-t", choices=["now", "hourly", "daily", "minutely"], 
                        default="now", help="天气类型 (默认: now)")
    
    args = parser.parse_args()
    
    # 查询天气
    data = query_weather(args.city, args.type)
    
    # 格式化输出
    formatters = {
        "now": format_now,
        "hourly": format_hourly,
        "daily": format_daily,
        "minutely": format_minutely,
    }
    
    formatter = formatters.get(args.type, format_now)
    output = formatter(data)
    
    print(output)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python weather_query.py \"城市\" --type [now|hourly|daily|minutely]", file=sys.stderr)
        print("", file=sys.stderr)
        print("首次使用请先配置 API Key：", file=sys.stderr)
        print("  export HEFENG_WEATHER_API_KEY=\"your-key\"", file=sys.stderr)
        print(f"  或创建 {CONFIG_FILE} 填入 API Key", file=sys.stderr)
        sys.exit(1)
    
    main()
