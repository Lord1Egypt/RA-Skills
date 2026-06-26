#!/usr/bin/env python3
"""
查询天气生活指数
"""

import argparse
import json
import sys

from qweather_api import api


# 指数类型映射
INDEX_TYPES = {
    "1": "运动指数",
    "2": "洗车指数",
    "3": "穿衣指数",
    "4": "感冒指数",
    "5": "紫外线指数",
    "6": "旅游指数",
    "7": "花粉过敏指数",
    "8": "舒适度指数",
    "9": "交通指数",
    "10": "防晒指数",
    "11": "化妆指数",
    "12": "空调开启指数",
    "13": "晾晒指数",
    "14": "钓鱼指数",
    "15": "太阳镜指数",
    "16": "空气污染扩散条件指数"
}


def main():
    parser = argparse.ArgumentParser(description="查询天气生活指数")
    parser.add_argument("--city", required=True, help="城市名称(必需)")
    parser.add_argument("--days", default="1d", choices=["1d", "3d"], help="预报天数(默认1d)")
    parser.add_argument("--types", default="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16", help="指数类型ID(逗号分隔)")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON")

    args = parser.parse_args()

    # 获取城市位置
    location_id = api.get_city_location(args.city)
    if not location_id:
        print(f"错误: 未找到城市 '{args.city}' 的位置信息", file=sys.stderr)
        sys.exit(1)

    # 调用 API
    endpoint = f"v7/indices/{args.days}"
    params = {"location": location_id, "type": args.types, "lang": "zh"}
    result = api.request(endpoint, params)

    if not result:
        print("错误: 获取生活指数数据失败", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        daily = result.get("daily", [])

        print(f"\n📍 {args.city} - 生活指数预报")
        print("=" * 60)

        for item in daily:
            date = item.get('date', '')
            name = INDEX_TYPES.get(item.get('type', ''), item.get('name', ''))
            category = item.get('category', '')
            level = item.get('level', '')
            text = item.get('text', '')

            print(f"\n📅 {date}")
            print(f"🏷️  {name}")
            print(f"📊 {category} (等级{level})")
            print(f"💡 建议: {text}")


if __name__ == "__main__":
    main()
