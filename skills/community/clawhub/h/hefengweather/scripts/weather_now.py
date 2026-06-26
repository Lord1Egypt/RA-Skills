#!/usr/bin/env python3
"""
查询实时天气
"""

import argparse
import json
import sys

from qweather_api import api


def main():
    parser = argparse.ArgumentParser(description="查询实时天气数据")
    parser.add_argument("--city", help="城市名称")
    parser.add_argument("--location", help="LocationID 或经纬度坐标")
    parser.add_argument("--lang", default="zh", help="语言(默认zh)")
    parser.add_argument("--unit", default="m", choices=["m", "i"], help="单位(默认m公制)")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON")

    args = parser.parse_args()

    # 验证参数
    if not args.location and not args.city:
        print("错误: 必须提供 --city 或 --location 其中之一", file=sys.stderr)
        sys.exit(1)

    # 获取位置
    location = args.location
    if not location:
        location = api.get_city_location(args.city)
        if not location:
            print(f"错误: 未找到城市 '{args.city}' 的位置信息", file=sys.stderr)
            sys.exit(1)

    # 调用 API
    params = {"location": location, "lang": args.lang, "unit": args.unit}
    result = api.request("v7/weather/now", params)

    if not result:
        print("错误: 获取天气数据失败", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        basic = result.get("basic", {})
        now = result.get("now", {})
        update_time = result.get("updateTime", "")

        print(f"\n📍 {basic.get('location', '')} ({basic.get('parentCity', '')} {basic.get('adminArea', '')})")
        print(f"🌡️  温度: {now.get('temp', '--')}°C")
        print(f"☁️  天气: {now.get('text', '--')}")
        print(f"💨 风向: {now.get('windDir', '--')}")
        print(f"🌪️  风力: {now.get('windScale', '--')}级")
        print(f"💧 湿度: {now.get('humidity', '--')}%")
        print(f"🔽 气压: {now.get('pressure', '--')}hPa")
        print(f"👁️  能见度: {now.get('vis', '--')}km")
        if update_time:
            print(f"🕐 更新时间: {update_time}")


if __name__ == "__main__":
    main()
