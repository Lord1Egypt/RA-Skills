#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按 IMO 查询船舶制裁风险评估。
需环境变量 HIFLEET_API_KEY。
可选 HIFLEET_API_BASE（默认 https://api.hifleet.com，无末尾斜杠）。

用法:
  python get_sanction.py <IMO>

Security: 仅向 HIFLEET_API_BASE 下 /sanction/assess/shiprisk/token 发起 GET；标准库 only。
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
    p = argparse.ArgumentParser(description="船舶制裁风险评估（按 IMO）")
    p.add_argument("imo", help="IMO 号（通常 7 位）")
    args = p.parse_args()

    api_key = get_api_key()
    if not api_key:
        print("请先配置 HIFLEET_API_KEY", file=sys.stderr)
        sys.exit(1)

    imo = str(args.imo).strip().upper().replace("IMO", "")
    if not imo.isdigit() or int(imo) <= 0:
        print("imonumber 应为正整数 IMO", file=sys.stderr)
        sys.exit(1)

    params = {"api_key": api_key, "imonumber": imo}
    url = api_base() + "/sanction/assess/shiprisk/token?" + urllib.parse.urlencode(params)
    try:
        data = http_get(url)
    except Exception as e:
        print("请求失败: %s" % e, file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
