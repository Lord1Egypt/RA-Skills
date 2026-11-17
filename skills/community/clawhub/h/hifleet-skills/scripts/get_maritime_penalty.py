#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海事行政处罚列表查询。
需环境变量 HIFLEET_API_KEY。
可选 HIFLEET_API_BASE（默认 https://api.hifleet.com，无末尾斜杠）。

用法:
  python get_maritime_penalty.py --ship-name 远航
  python get_maritime_penalty.py --mmsi 412345678
  python get_maritime_penalty.py --start-time 2024-01-01 --end-time 2024-12-31
  python get_maritime_penalty.py --ship-name 远航 --page 1 --page-size 20

Security: 仅向 HIFLEET_API_BASE 下 /maritime/penalty/list/token 发起 GET；标准库 only。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional


def get_api_key() -> Optional[str]:
    return os.environ.get("HIFLEET_API_KEY")


def api_base() -> str:
    return (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")


def http_get(url: str) -> Dict[str, Any]:
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main() -> None:
    p = argparse.ArgumentParser(description="海事行政处罚列表")
    p.add_argument("--mmsi", default=None, help="MMSI")
    p.add_argument("--ship-name", dest="ship_name", default=None, help="船名/违法主体名")
    p.add_argument("--start-time", dest="start_time", default=None, help="yyyy-MM-dd")
    p.add_argument("--end-time", dest="end_time", default=None, help="yyyy-MM-dd")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--page-size", dest="page_size", type=int, default=20)
    args = p.parse_args()

    api_key = get_api_key()
    if not api_key:
        print("请先配置 HIFLEET_API_KEY", file=sys.stderr)
        sys.exit(1)

    if not any([args.mmsi, args.ship_name, args.start_time, args.end_time]):
        print("请至少提供 --mmsi、--ship-name 或 --start-time/--end-time", file=sys.stderr)
        sys.exit(1)

    params: Dict[str, str] = {
        "api_key": api_key,
        "page": str(args.page),
        "pageSize": str(args.page_size),
    }
    if args.mmsi:
        params["mmsi"] = str(args.mmsi).strip()
    if args.ship_name:
        params["shipName"] = args.ship_name.strip()
    if args.start_time:
        params["startTime"] = args.start_time.strip()
    if args.end_time:
        params["endTime"] = args.end_time.strip()

    url = api_base() + "/maritime/penalty/list/token?" + urllib.parse.urlencode(params)
    try:
        data = http_get(url)
    except Exception as e:
        print("请求失败: %s" % e, file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
