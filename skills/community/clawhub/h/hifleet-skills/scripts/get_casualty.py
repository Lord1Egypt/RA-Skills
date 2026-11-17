#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
船舶事故事件：按 IMO 查列表，按 eventId 查详情。
需环境变量 HIFLEET_API_KEY。
可选 HIFLEET_API_BASE（默认 https://api.hifleet.com，无末尾斜杠）。

用法:
  python get_casualty.py list <IMO>
  python get_casualty.py detail <eventId>

Security: 仅向 HIFLEET_API_BASE 下 /casualty/list/token 与 /casualty/detail/token 发起 GET；标准库 only。
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
    p = argparse.ArgumentParser(description="船舶事故事件：列表 / 详情")
    sub = p.add_subparsers(dest="cmd", required=True)

    pl = sub.add_parser("list", help="按 IMO 查询事故/事件列表")
    pl.add_argument("imo", help="IMO 号（通常 7 位）")

    pd = sub.add_parser("detail", help="按 eventId 查询事故详情")
    pd.add_argument("event_id", help="事件 ID（来自列表 eventId）")

    args = p.parse_args()

    api_key = get_api_key()
    if not api_key:
        print("请先配置 HIFLEET_API_KEY", file=sys.stderr)
        sys.exit(1)

    base = api_base()

    try:
        if args.cmd == "list":
            imo = str(args.imo).strip().upper().replace("IMO", "")
            params = {"api_key": api_key, "imo": imo}
            url = base + "/casualty/list/token?" + urllib.parse.urlencode(params)
            data = http_get(url)
        else:
            eid = str(args.event_id).strip()
            if not eid.isdigit():
                print("eventId 应为整数", file=sys.stderr)
                sys.exit(1)
            params = {"api_key": api_key, "eventId": eid}
            url = base + "/casualty/detail/token?" + urllib.parse.urlencode(params)
            data = http_get(url)
    except Exception as e:
        print("请求失败: %s" % e, file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
