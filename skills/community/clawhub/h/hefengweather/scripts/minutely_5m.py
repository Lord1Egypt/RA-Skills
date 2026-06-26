#!/usr/bin/env python3
"""
查询未来2小时5分钟级降水预报
"""

import argparse
import json
import sys

from qweather_api import api


def main():
    parser = argparse.ArgumentParser(description="查询未来2小时5分钟级降水预报")
    parser.add_argument("--location", required=True, help="经纬度坐标或城市名")
    parser.add_argument("--lang", default="zh", help="语言(默认zh)")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON")

    args = parser.parse_args()

    # 处理位置
    loc_value = args.location
    if "," not in loc_value:
        resolved = api.get_city_location(loc_value, return_coords=True)
        if not resolved:
            print(f"错误: 无法解析位置 '{loc_value}'", file=sys.stderr)
            sys.exit(1)
        loc_value = resolved

    # 调用 API
    params = {"location": loc_value, "lang": args.lang}
    result = api.request("v7/minutely/5m", params)

    if not result:
        print("错误: 获取分钟级降水数据失败", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        basic = result.get("basic", {})
        summary = result.get("summary", "")
        minutely = result.get("minutely", [])

        print(f"\n📍 {basic.get('location', '')} - 未来2小时降水预报")
        print("=" * 60)
        print(f"📊 {summary}")

        if minutely:
            print(f"\n⏰ 详细预报:")
            for m in minutely[:24]:  # 显示前2小时
                print(f"   {m.get('fxTime', '')} | "
                      f"降水: {m.get('precip', '--')}mm | "
                      f"类型: {m.get('type', '--')} | "
                      f"{m.get('text', '--')}")


if __name__ == "__main__":
    main()
