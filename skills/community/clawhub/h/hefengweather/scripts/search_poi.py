#!/usr/bin/env python3
"""
搜索兴趣点(POI)
"""

import argparse
import json
import sys

from qweather_api import api


# POI 类型常量
POI_TYPES = {
    "scenic": "景点",
    "TSTA": "潮汐站点"
}


def main():
    parser = argparse.ArgumentParser(description="搜索兴趣点(POI)")
    parser.add_argument("--location", required=True, help="经纬度、LocationID或城市名")
    parser.add_argument("--keyword", required=True, help="搜索关键词")
    parser.add_argument("--poi-type", required=True, choices=["scenic", "TSTA"], help="POI类型")
    parser.add_argument("--city", help="限定搜索城市")
    parser.add_argument("--radius", type=int, default=5000, help="搜索半径(米),默认5000,范围100-50000")
    parser.add_argument("--page", type=int, default=1, help="页码,默认1")
    parser.add_argument("--lang", default="zh", help="语言(默认zh)")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON")

    args = parser.parse_args()

    # 验证参数
    if not isinstance(args.radius, int) or args.radius < 100 or args.radius > 50000:
        print("错误: radius 参数必须在 100-50000 之间", file=sys.stderr)
        sys.exit(1)

    if not isinstance(args.page, int) or args.page < 1:
        print("错误: page 参数必须 >= 1", file=sys.stderr)
        sys.exit(1)

    # 处理位置
    loc_value = args.location
    if "," in loc_value:
        try:
            parts = [s.strip() for s in loc_value.split(",", 1)]
            if len(parts) != 2:
                raise ValueError("Invalid format")
            lon = float(parts[0])
            lat = float(parts[1])
            formatted_loc = f"{lon:.2f},{lat:.2f}"
        except ValueError:
            print("错误: 经纬度格式错误", file=sys.stderr)
            sys.exit(1)
    elif loc_value.isdigit():
        formatted_loc = loc_value
    else:
        location_id = api.get_city_location(loc_value)
        if not location_id:
            print(f"错误: 无法解析位置 '{loc_value}'", file=sys.stderr)
            sys.exit(1)
        formatted_loc = location_id

    # 构建请求参数
    params = {
        "location": formatted_loc,
        "keyword": args.keyword,
        "type": args.poi_type,
        "radius": str(args.radius),
        "page": str(args.page),
        "lang": args.lang
    }

    # 如果指定了城市,添加城市参数
    if args.city:
        if "," in args.city:
            city_loc = api.get_city_location(args.city.strip())
            if city_loc:
                params["city"] = city_loc
        elif args.city.strip().isdigit():
            params["city"] = args.city.strip()
        else:
            city_location_id = api.get_city_location(args.city.strip())
            if city_location_id:
                params["city"] = city_location_id

    # 调用 API
    result = api.request("geo/v2/poi/lookup", params)

    if not result:
        print("错误: POI搜索失败", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        poi_list = result.get("poi", [])
        type_name = POI_TYPES.get(args.poi_type, args.poi_type)

        print(f"\n🔍 {type_name}搜索结果 - 关键词: {args.keyword}")
        print("=" * 60)

        if not poi_list:
            print("未找到匹配的POI")
        else:
            for poi in poi_list:
                print(f"\n📌 {poi.get('name', '')}")
                print(f"   📍 {poi.get('address', '')}")
                print(f"   🏷️  类型: {poi.get('type', '')}")
                if 'distance' in poi:
                    print(f"   📏 距离: {poi['distance']}米")
                print(f"   🆔 ID: {poi.get('id', '')}")


if __name__ == "__main__":
    main()
