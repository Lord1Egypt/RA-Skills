#!/usr/bin/env python3
"""
查询气象灾害预警信息
"""

import argparse
import json
import sys

from qweather_api import api


def main():
    parser = argparse.ArgumentParser(description="查询气象灾害预警信息")
    parser.add_argument("--city", required=True, help="城市名称(必需)")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON")

    args = parser.parse_args()

    # 获取城市位置
    location_id = api.get_city_location(args.city)
    if not location_id:
        print(f"错误: 未找到城市 '{args.city}' 的位置信息", file=sys.stderr)
        sys.exit(1)

    # 调用 API
    result = api.request("v7/warning/now", {"location": location_id, "lang": "zh"})

    if not result:
        print("错误: 获取预警数据失败", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        warnings = result.get("warning", [])

        if not warnings:
            print(f"\n✅ {args.city} 当前无气象预警")
        else:
            print(f"\n⚠️  {args.city} 气象预警信息")
            print("=" * 60)

            for w in warnings:
                print(f"\n🚨 {w.get('title', '未知预警')}")
                print(f"📅 发布时间: {w.get('pubTime', '')}")
                print(f"🎯 预警级别: {w.get('level', '')}")
                print(f"📍 影响区域: {w.get('areas', '')}")
                print(f"📝 预警内容:\n{w.get('text', '')}")


if __name__ == "__main__":
    main()
