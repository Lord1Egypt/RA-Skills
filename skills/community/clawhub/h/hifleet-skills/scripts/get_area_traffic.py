#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查询指定区域内的当前船舶。支持三种方式：
  1) bbox：左下经度、左下纬度、右上经度、右上纬度；
  2) areaId：区域清单接口返回的 id（用户文字描述区域时可先查区域清单，用 name/cnName 匹配得到 id）；
  3) polygon：WKT 格式多边形，参数名 polygon。
需配置环境变量 `HIFLEET_API_KEY`。
可选 `HIFLEET_API_BASE`（默认 https://api.hifleet.com，无末尾斜杠）。

用法:
  python get_area_traffic.py <左下经度> <左下纬度> <右上经度> <右上纬度>
  例如: python get_area_traffic.py 120 15 121 17
  python get_area_traffic.py --area-id <areaId>
  例如: python get_area_traffic.py --area-id 52
  python get_area_traffic.py --polygon "POLYGON((lon1 lat1,lon2 lat2,...))"
  例如: python get_area_traffic.py --polygon "POLYGON((120 15,121 15,121 17,120 17,120 15))"

Security: 仅向 HIFLEET_API_BASE 下 position/gettraffic/token 发起 GET；标准库 only。
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def api_base():
    return (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")


def get_api_key():
    return os.environ.get("HIFLEET_API_KEY")


def get_area_traffic(api_key: str, bbox: str = None, area_id: int = None, polygon: str = None) -> dict:
    """bbox、area_id、polygon 三选一。polygon 为 WKT 格式，如 POLYGON((lon1 lat1,...))。"""
    params = {"api_key": api_key}
    if area_id is not None:
        params["areaId"] = area_id
    elif bbox:
        params["bbox"] = bbox
    elif polygon:
        params["polygon"] = polygon
    else:
        raise ValueError("必须提供 bbox、areaId 或 polygon 之一")
    url = api_base() + "/position/gettraffic/token?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main():
    parser = argparse.ArgumentParser(description="查询指定区域内的当前船舶（bbox、areaId 或 polygon 三选一）")
    parser.add_argument("--area-id", type=int, help="区域 id，来自区域清单接口 position/areas/token 的 list[].id")
    parser.add_argument("--polygon", type=str, help="WKT 格式多边形，如 POLYGON((lon1 lat1,lon2 lat2,...))")
    parser.add_argument("bbox", nargs="*", type=float, help="左下经度 左下纬度 右上经度 右上纬度（与 --area-id/--polygon 互斥）")
    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key:
        print("请先配置 HiFleet 授权 api_key（环境变量 HIFLEET_API_KEY）", file=sys.stderr)
        sys.exit(1)

    modes = sum([args.area_id is not None, bool(args.polygon), len(args.bbox) == 4])
    if modes > 1:
        print("请只使用 --area-id、--polygon 或 bbox 四参数之一", file=sys.stderr)
        sys.exit(1)

    if args.area_id is not None:
        try:
            data = get_area_traffic(api_key=api_key, area_id=args.area_id)
        except Exception as e:
            print("请求失败: %s" % e, file=sys.stderr)
            sys.exit(1)
    elif args.polygon:
        try:
            data = get_area_traffic(api_key=api_key, polygon=args.polygon)
        except Exception as e:
            print("请求失败: %s" % e, file=sys.stderr)
            sys.exit(1)
    elif len(args.bbox) == 4:
        lon_min, lat_min, lon_max, lat_max = args.bbox[0], args.bbox[1], args.bbox[2], args.bbox[3]
        if lon_min >= lon_max or lat_min >= lat_max:
            print("请保证 左下经度 < 右上经度 且 左下纬度 < 右上纬度", file=sys.stderr)
            sys.exit(1)
        bbox = "%s,%s,%s,%s" % (lon_min, lat_min, lon_max, lat_max)
        try:
            data = get_area_traffic(api_key=api_key, bbox=bbox)
        except Exception as e:
            print("请求失败: %s" % e, file=sys.stderr)
            sys.exit(1)
    else:
        print("用法: python get_area_traffic.py <左下经度> <左下纬度> <右上经度> <右上纬度>", file=sys.stderr)
        print("  或: python get_area_traffic.py --area-id <areaId>", file=sys.stderr)
        print("  或: python get_area_traffic.py --polygon \"POLYGON((lon1 lat1,...))\"", file=sys.stderr)
        print("例如: python get_area_traffic.py 120 15 121 17", file=sys.stderr)
        print("     python get_area_traffic.py --area-id 52  # 区域 id 来自 get_areas.py 区域清单", file=sys.stderr)
        print("     python get_area_traffic.py --polygon \"POLYGON((120 15,121 15,121 17,120 17,120 15))\"", file=sys.stderr)
        sys.exit(1)

    if data.get("result") != "ok":
        print(json.dumps(data, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
