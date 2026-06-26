#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PSC OpenClaw 统计：区间对比 / 缺陷 Top / 占比对比（旗国或 type_ins）。
GET {BASE}/pscapi/openclaw/stats/compare|defects/top|mix/compare
需环境变量 `HIFLEET_API_KEY`；可选 `HIFLEET_API_BASE`。
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


def http_get(url: str) -> dict:
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def is_hi_ok(data: dict) -> bool:
    return str(data.get("status")) == "1"


def print_hi_error(data: dict) -> None:
    msg = data.get("msg") or data.get("message") or ""
    code = data.get("code")
    if code is not None:
        print(f"code={code} {msg}".strip(), file=sys.stderr)
    else:
        print(msg or json.dumps(data, ensure_ascii=False), file=sys.stderr)


def main() -> int:
    api_key = get_api_key()
    if not api_key:
        print("请配置 HIFLEET_API_KEY", file=sys.stderr)
        return 1

    parser = argparse.ArgumentParser(description="PSC OpenClaw 统计 CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_cmp = sub.add_parser("compare", help="区间对比 stats/compare")
    p_cmp.add_argument("--date-from", dest="date_from")
    p_cmp.add_argument("--date-to", dest="date_to")
    p_cmp.add_argument("--base-date-from", dest="base_date_from")
    p_cmp.add_argument("--base-date-to", dest="base_date_to")
    p_cmp.add_argument("--no-compare-previous", dest="compare_previous", action="store_false", default=True)
    p_cmp.add_argument("--group-by", dest="group_by", default="AUTHORITY")
    p_cmp.add_argument("--authority-contains", dest="authority_contains")
    p_cmp.add_argument("--flag-contains", dest="flag_contains")
    p_cmp.add_argument("--port-contains", dest="port_contains")
    p_cmp.add_argument("--mou")
    p_cmp.add_argument("--limit", type=int, default=50)

    p_def = sub.add_parser("defects", help="缺陷 Top stats/defects/top")
    p_def.add_argument("--date-from", dest="date_from")
    p_def.add_argument("--date-to", dest="date_to")
    p_def.add_argument("--authority-contains", dest="authority_contains")
    p_def.add_argument("--flag-contains", dest="flag_contains")
    p_def.add_argument("--limit", type=int, default=30)

    p_mix = sub.add_parser("mix", help="占比对比 stats/mix/compare")
    p_mix.add_argument("--date-from-recent", dest="date_from_recent")
    p_mix.add_argument("--date-to-recent", dest="date_to_recent")
    p_mix.add_argument("--date-from-base", dest="date_from_base")
    p_mix.add_argument("--date-to-base", dest="date_to_base")
    p_mix.add_argument("--mix-dimension", dest="mix_dimension", default="FLAG")
    p_mix.add_argument("--authority-contains", dest="authority_contains")
    p_mix.add_argument("--flag-contains", dest="flag_contains")
    p_mix.add_argument("--port-contains", dest="port_contains")
    p_mix.add_argument("--mou")
    p_mix.add_argument("--limit", type=int, default=20)

    ns = parser.parse_args()

    params: Dict[str, Any] = {"api_key": api_key}
    path = ""
    if ns.cmd == "compare":
        path = "/pscapi/openclaw/stats/compare"
        if ns.date_from:
            params["dateFrom"] = ns.date_from
        if ns.date_to:
            params["dateTo"] = ns.date_to
        if ns.base_date_from:
            params["baseDateFrom"] = ns.base_date_from
        if ns.base_date_to:
            params["baseDateTo"] = ns.base_date_to
        params["comparePrevious"] = "true" if ns.compare_previous else "false"
        params["groupBy"] = ns.group_by
        if ns.authority_contains:
            params["authorityContains"] = ns.authority_contains
        if ns.flag_contains:
            params["flagContains"] = ns.flag_contains
        if ns.port_contains:
            params["portContains"] = ns.port_contains
        if ns.mou:
            params["mou"] = ns.mou
        params["limit"] = str(ns.limit)
    elif ns.cmd == "defects":
        path = "/pscapi/openclaw/stats/defects/top"
        if ns.date_from:
            params["dateFrom"] = ns.date_from
        if ns.date_to:
            params["dateTo"] = ns.date_to
        if ns.authority_contains:
            params["authorityContains"] = ns.authority_contains
        if ns.flag_contains:
            params["flagContains"] = ns.flag_contains
        params["limit"] = str(ns.limit)
    else:
        path = "/pscapi/openclaw/stats/mix/compare"
        if ns.date_from_recent:
            params["dateFromRecent"] = ns.date_from_recent
        if ns.date_to_recent:
            params["dateToRecent"] = ns.date_to_recent
        if ns.date_from_base:
            params["dateFromBase"] = ns.date_from_base
        if ns.date_to_base:
            params["dateToBase"] = ns.date_to_base
        params["mixDimension"] = ns.mix_dimension
        if ns.authority_contains:
            params["authorityContains"] = ns.authority_contains
        if ns.flag_contains:
            params["flagContains"] = ns.flag_contains
        if ns.port_contains:
            params["portContains"] = ns.port_contains
        if ns.mou:
            params["mou"] = ns.mou
        params["limit"] = str(ns.limit)

    url = api_base() + path + "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    try:
        data = http_get(url)
    except Exception as e:
        print(f"请求失败: {e}", file=sys.stderr)
        return 1
    if not is_hi_ok(data):
        print_hi_error(data)
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(data.get("data"), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
