#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港口指南：列表检索（可选港名/代码，不传则全量）与按港口 id 查详情。
详情参数 portId 取自列表项字段 piuid。
需环境变量 `HIFLEET_API_KEY`。
可选 HIFLEET_API_BASE（默认 https://api.hifleet.com，无末尾斜杠）。

用法:
  python get_port.py search [--port-name NAME] [--port-code CODE]
  python get_port.py detail <portId>   # portId 为列表返回的 piuid

Security: 仅向 HIFLEET_API_BASE 下 /portguide/getPort/token 与 /portguide/getPortDetail/token 发起 GET；标准库 only。
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
    p = argparse.ArgumentParser(description="港口指南：列表 / 详情")
    sub = p.add_subparsers(dest="cmd", required=True)

    ps = sub.add_parser("search", help="港口列表（可选 --port-name / --port-code，不传则全量）")
    ps.add_argument("--port-name", dest="port_name", default=None)
    ps.add_argument("--port-code", dest="port_code", default=None)

    pd = sub.add_parser("detail", help="港口详情（portId 为列表中的 piuid）")
    pd.add_argument("port_id", help="港口 id（整数，来自列表 piuid）")

    args = p.parse_args()

    api_key = get_api_key()
    if not api_key:
        print("请先配置 HIFLEET_API_KEY", file=sys.stderr)
        sys.exit(1)

    base = api_base()

    try:
        if args.cmd == "search":
            params: Dict[str, str] = {"api_key": api_key}
            if args.port_name:
                params["portName"] = args.port_name
            if args.port_code:
                params["portCode"] = args.port_code
            url = base + "/portguide/getPort/token?" + urllib.parse.urlencode(params)
            data = http_get(url)
        else:
            pid = str(args.port_id).strip()
            if not pid.isdigit():
                print("portId 应为整数（列表项 piuid）", file=sys.stderr)
                sys.exit(1)
            params = {"api_key": api_key, "portId": pid}
            url = base + "/portguide/getPortDetail/token?" + urllib.parse.urlencode(params)
            data = http_get(url)
    except Exception as e:
        print("请求失败: %s" % e, file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
