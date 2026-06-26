#!/usr/bin/env python3
"""
查询格点实时天气数据
"""

import argparse
import json
import sys

from qweather_api import api


def main():
    parser = argparse.ArgumentParser(description="查询格点实时天气数据(高分辨率数值模式)")
    parser.add_argument("--location", required=True, help="经纬度坐标,如 116.41,39.92")
    parser.add_argument("--lang", default="zh", help="语言(默认zh)")
    parser.add_argument("--unit", default="m", choices=["m", "i"], help="单位(默认m公制)")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON")

    args = parser.parse_args()

    # 验证并格式化经纬度
    if "," not in args.location:
        print("错误: location 参数格式错误,期望格式: 经度,纬度", file=sys.stderr)
        sys.exit(1)

    try:
        lon_str, lat_str = [s.strip() for s in args.location.split(",", 1)]
        lon = float(lon_str)
        lat = float(lat_str)

        if not (-180 <= lon <= 180) or not (-90 <= lat <= 90):
            print("错误: 经纬度超出有效范围", file=sys.stderr)
            sys.exit(1)

        formatted_loc = f"{lon:.2f},{lat:.2f}"
    except ValueError as e:
        print(f"错误: 无法解析坐标参数 - {e}", file=sys.stderr)
        sys.exit(1)

    # 调用 API
    params = {"location": formatted_loc, "lang": args.lang, "unit": args.unit}
    result = api.request("v7/grid-weather/now", params)

    if not result:
        print("错误: 获取格点实时天气数据失败", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        now = result.get("now", {})
        update_time = result.get("updateTime", "")

        print(f"\n📍 格点位置: {args.location}")
        print("=" * 60)
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
