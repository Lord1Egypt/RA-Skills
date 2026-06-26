#!/usr/bin/env python3
"""
Mock Weather Query Script
Returns simulated weather data for any city.
Usage: python3 mock_weather.py <city> [--forecast <days>]
"""

import sys
import random
import argparse
from datetime import datetime, timedelta

# Simulated weather conditions pool
CONDITIONS = ["晴", "多云", "阴", "小雨", "中雨", "大雨", "雷阵雨", "小雪", "雾"]
WIND_DIRS = ["东风", "南风", "西风", "北风", "东南风", "西南风", "东北风", "西北风"]

def get_weather(city: str, days: int = 1):
    """Generate mock weather for a city."""
    # Use city name as seed for consistent results per city
    seed = sum(ord(c) for c in city) + datetime.now().day
    rng = random.Random(seed)

    results = []
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        temp_high = rng.randint(15, 35)
        temp_low = temp_high - rng.randint(5, 12)
        condition = rng.choice(CONDITIONS)
        wind_dir = rng.choice(WIND_DIRS)
        wind_level = rng.randint(1, 5)
        humidity = rng.randint(40, 90)

        results.append({
            "date": date.strftime("%Y-%m-%d"),
            "city": city,
            "condition": condition,
            "temp_high": temp_high,
            "temp_low": temp_low,
            "humidity": humidity,
            "wind": f"{wind_dir}{wind_level}级",
        })

    return results

def format_output(data: list) -> str:
    lines = []
    for d in data:
        lines.append(
            f"📅 {d['date']}  📍 {d['city']}\n"
            f"   天气：{d['condition']}\n"
            f"   气温：{d['temp_low']}°C ~ {d['temp_high']}°C\n"
            f"   湿度：{d['humidity']}%\n"
            f"   风力：{d['wind']}\n"
        )
    return "\n".join(lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mock weather query")
    parser.add_argument("city", help="City name")
    parser.add_argument("--forecast", type=int, default=1, help="Number of forecast days (1-7)")
    args = parser.parse_args()

    days = max(1, min(7, args.forecast))
    data = get_weather(args.city, days)
    print(format_output(data))
