#!/usr/bin/env python3
"""
查询实时空气质量
"""

import argparse
import json
import sys

from qweather_api import api


def main():
    parser = argparse.ArgumentParser(description="查询实时空气质量")
    parser.add_argument("--city", required=True, help="城市名称(必需)")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON")

    args = parser.parse_args()

    # 获取城市经纬度
    location_coords = api.get_city_location(args.city, return_coords=True)
    if not location_coords:
        print(f"错误: 未找到城市 '{args.city}' 的位置信息", file=sys.stderr)
        sys.exit(1)

    try:
        lat, lon = location_coords.split(",")
    except ValueError:
        print("错误: 无法解析经纬度信息", file=sys.stderr)
        sys.exit(1)

    # 调用 API
    endpoint = f"airquality/v1/current/{lat}/{lon}"
    result = api.request(endpoint, {"lang": "zh"})

    if not result:
        print("错误: 获取空气质量数据失败", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        station = result.get("station", {})
        now = result.get("now", {})

        print(f"\n📍 {station.get('name', '')} - 实时空气质量")
        print("=" * 60)
        print(f"🌫️  AQI: {now.get('aqi', '--')} ({now.get('category', '--')})")
        print(f"🏭 PM2.5: {now.get('pm2p5', '--')}μg/m³")
        print(f"💨 PM10: {now.get('pm10', '--')}μg/m³")
        print(f"🌿 NO2: {now.get('no2', '--')}μg/m³")
        print(f"😷 SO2: {now.get('so2', '--')}μg/m³")
        print(f"🍃 O3: {now.get('o3', '--')}μg/m³")
        print(f"🍂 CO: {now.get('co', '--')}mg/m³")
        print(f"📊 主要污染物: {now.get('primary', '--')}")


if __name__ == "__main__":
    main()
