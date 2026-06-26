#!/usr/bin/env python3
"""
查询热门城市列表
"""

import argparse
import json
import sys

from qweather_api import api


def main():
    parser = argparse.ArgumentParser(description="查询热门城市列表")
    parser.add_argument("--number", type=int, default=10, help="返回数量(1-100,默认10)")
    parser.add_argument("--city-type", default="cn", choices=["cn", "world", "overseas"], help="城市类型(默认cn)")
    parser.add_argument("--lang", default="zh", help="语言(默认zh)")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON")

    args = parser.parse_args()

    # 验证参数
    if not isinstance(args.number, int) or args.number < 1 or args.number > 100:
        print("错误: number 参数必须在 1-100 之间", file=sys.stderr)
        sys.exit(1)

    # 调用 API
    params = {"number": str(args.number), "type": args.city_type, "lang": args.lang}
    result = api.request("geo/v2/city/top", params)

    if not result:
        print("错误: 获取热门城市数据失败", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        cities = result.get("topCityList", [])

        type_names = {"cn": "国内", "world": "全球", "overseas": "海外"}
        print(f"\n🌆 热门城市列表 ({type_names.get(args.city_type, '')} TOP {args.number})")
        print("=" * 60)

        for city in cities:
            print(f"🏙️  {city.get('name', '')} ({city.get('adm1', '')} {city.get('country', '')}) - "
                  f"ID: {city.get('id', '')}")


if __name__ == "__main__":
    main()
