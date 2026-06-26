#!/usr/bin/env python3
"""
查询日出日落时间
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone

from qweather_api import api


def main():
    parser = argparse.ArgumentParser(description="查询日出日落时间")
    parser.add_argument("--location", required=True, help="城市名、LocationID或经纬度")
    parser.add_argument("--date", help="日期(格式yyyyMMdd,默认今天)")
    parser.add_argument("--lang", default="zh", help="语言(默认zh)")
    parser.add_argument("--raw", action="store_true", help="输出原始JSON")

    args = parser.parse_args()

    # 处理日期
    if args.date:
        try:
            target_date = datetime.strptime(args.date, "%Y%m%d").date()
        except ValueError:
            print("错误: 日期格式错误,需为 yyyyMMdd", file=sys.stderr)
            sys.exit(1)
    else:
        target_date = (datetime.now(timezone.utc) + timedelta(hours=8)).date()
        args.date = target_date.strftime("%Y%m%d")

    # 处理位置
    loc_value = args.location
    if "," in loc_value:
        try:
            lon_str, lat_str = [s.strip() for s in loc_value.split(",", 1)]
            lon = float(lon_str)
            lat = float(lat_str)
            loc_value = f"{lon:.2f},{lat:.2f}"
        except ValueError:
            print("错误: 无法解析经纬度", file=sys.stderr)
            sys.exit(1)
    elif not loc_value.isdigit():
        resolved = api.get_city_location(loc_value)
        if not resolved:
            print(f"错误: 无法解析位置 '{loc_value}'", file=sys.stderr)
            sys.exit(1)
        loc_value = resolved

    # 调用 API
    params = {"location": loc_value, "date": args.date, "lang": args.lang}
    result = api.request("v7/astronomy/sun", params)

    if not result:
        print("错误: 获取日出日落数据失败", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        basic = result.get("basic", {})
        sun = result.get("sun", [])

        print(f"\n📍 {basic.get('location', '')} - {args.date} 日出日落")
        print("=" * 60)

        if sun:
            s = sun[0]
            print(f"🌅 日出: {s.get('sunrise', '--')}")
            print(f"🌇 日落: {s.get('sunset', '--')}")
            if s.get('sunriseEpoch'):
                print(f"⏰ 日出时间戳: {s.get('sunriseEpoch')}")
            if s.get('sunsetEpoch'):
                print(f"⏰ 日落时间戳: {s.get('sunsetEpoch')}")


if __name__ == "__main__":
    main()
