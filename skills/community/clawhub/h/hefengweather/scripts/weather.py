#!/usr/bin/env python3
"""
查询天气预报(3-30天)
"""

import argparse
import json
import sys

from qweather_api import api


def main():
    parser = argparse.ArgumentParser(description="查询天气预报(3-30天)")
    parser.add_argument("--city", required=True, help="城市名称(必需)")
    parser.add_argument("--days", default="3d", choices=["3d", "7d", "10d", "15d", "30d"], help="预报天数(默认3d)")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON")

    args = parser.parse_args()

    # 获取城市位置
    location_id = api.get_city_location(args.city)
    if not location_id:
        print(f"错误: 未找到城市 '{args.city}' 的位置信息", file=sys.stderr)
        sys.exit(1)

    # 调用 API
    endpoint = f"v7/weather/{args.days}"
    result = api.request(endpoint, {"location": location_id})

    if not result:
        print("错误: 获取天气数据失败", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        basic = result.get("basic", {})
        daily = result.get("daily", [])

        print(f"\n📍 {basic.get('location', '')} - {args.days.upper()} 天气预报")
        print("=" * 60)

        for day in daily:
            print(f"\n📅 {day.get('fxDate', '')}")
            print(f"   白天: {day.get('textDay', '--')} | 夜间: {day.get('textNight', '--')}")
            print(f"   温度: {day.get('tempMin', '--')}~{day.get('tempMax', '--')}°C")
            print(f"   风向: {day.get('windDirDay', '--')} | 风力: {day.get('windScaleDay', '--')}级")
            print(f"   湿度: {day.get('humidity', '--')}% | 降水概率: {day.get('pop', '--')}%")


if __name__ == "__main__":
    main()
