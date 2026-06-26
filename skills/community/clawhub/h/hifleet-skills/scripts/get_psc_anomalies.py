#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PSC 统计异常事件：列表 / 严重度汇总 / 按 ID 详情。
接口：GET {BASE}/pscapi/openclaw/anomalies、.../summary、.../anomalies/{id}
需环境变量 `HIFLEET_API_KEY`。
可选 HIFLEET_API_BASE（默认 https://api.hifleet.com，无末尾斜杠）。

用法:
  python get_psc_anomalies.py list [--date-from YYYY-MM-DD] [--date-to YYYY-MM-DD]
      [--authority X] [--authority-contains X] [--flag X] [--flag-contains X] [--port X] [--severity HIGH] [--page 1] [--page-size 20]
  python get_psc_anomalies.py summary [--date-from ...] [--date-to ...] [同上筛选]
  python get_psc_anomalies.py get <id>

Security: 仅向 HIFLEET_API_BASE 下述 pscapi/openclaw 路径发起 GET；标准库 only。
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


def add_common_filters(p: argparse.ArgumentParser) -> None:
    p.add_argument("--date-from", dest="date_from", default=None, help="yyyy-MM-dd")
    p.add_argument("--date-to", dest="date_to", default=None, help="yyyy-MM-dd")
    p.add_argument("--authority", default=None)
    p.add_argument("--authority-contains", dest="authority_contains", default=None)
    p.add_argument("--flag", default=None)
    p.add_argument("--flag-contains", dest="flag_contains", default=None)
    p.add_argument("--port", default=None)
    p.add_argument("--severity", default=None)
    p.add_argument("--anomaly-type", dest="anomaly_type", default=None)
    p.add_argument("--slice-type", dest="slice_type", default=None)
    p.add_argument("--metric", default=None)
    p.add_argument("--status", default=None)


def build_filter_params(ns: argparse.Namespace) -> Dict[str, str]:
    out: Dict[str, str] = {}
    mapping = [
        ("date_from", "dateFrom"),
        ("date_to", "dateTo"),
        ("authority", "authority"),
        ("authority_contains", "authorityContains"),
        ("flag", "flag"),
        ("flag_contains", "flagContains"),
        ("port", "port"),
        ("severity", "severity"),
        ("anomaly_type", "anomalyType"),
        ("slice_type", "sliceType"),
        ("metric", "metric"),
        ("status", "status"),
    ]
    for attr, qname in mapping:
        v = getattr(ns, attr, None)
        if v is not None and str(v).strip() != "":
            out[qname] = str(v).strip()
    return out


def run_list(ns: argparse.Namespace, api_key: str) -> int:
    params: Dict[str, Any] = {"api_key": api_key, "page": str(ns.page), "pageSize": str(ns.page_size)}
    params.update(build_filter_params(ns))
    url = api_base() + "/pscapi/openclaw/anomalies?" + urllib.parse.urlencode(params)
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


def run_summary(ns: argparse.Namespace, api_key: str) -> int:
    params: Dict[str, Any] = {"api_key": api_key}
    params.update(build_filter_params(ns))
    url = api_base() + "/pscapi/openclaw/anomalies/summary?" + urllib.parse.urlencode(params)
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


def run_get(aid: int, api_key: str) -> int:
    params = {"api_key": api_key}
    url = (
        api_base()
        + "/pscapi/openclaw/anomalies/"
        + str(int(aid))
        + "?"
        + urllib.parse.urlencode(params)
    )
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


def main() -> int:
    api_key = get_api_key()
    if not api_key:
        print(
            "请配置 HIFLEET_API_KEY",
            file=sys.stderr,
        )
        return 1

    parser = argparse.ArgumentParser(description="PSC 统计异常 openclaw 接口 CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="分页列表")
    add_common_filters(p_list)
    p_list.add_argument("--page", type=int, default=1)
    p_list.add_argument("--page-size", dest="page_size", type=int, default=20)
    p_list.set_defaults(func=lambda ns: run_list(ns, api_key))

    p_sum = sub.add_parser("summary", help="按 severity 汇总")
    add_common_filters(p_sum)
    p_sum.set_defaults(func=lambda ns: run_summary(ns, api_key))

    p_get = sub.add_parser("get", help="按 ID 详情")
    p_get.add_argument("id", type=int)
    p_get.set_defaults(func=lambda ns: run_get(ns.id, api_key))

    ns = parser.parse_args()
    return int(ns.func(ns))


if __name__ == "__main__":
    sys.exit(main())
