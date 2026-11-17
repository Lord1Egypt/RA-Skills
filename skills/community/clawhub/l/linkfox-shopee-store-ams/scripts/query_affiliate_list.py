#!/usr/bin/env python3
"""
Shopee Store — query_affiliate_list

官方: https://open.shopee.com/documents/v2/v2.ams.query_affiliate_list?module=127&type=1

入参说明见 references/apis/query-affiliate-list.md。
"""

from __future__ import annotations

import json
import sys

from _ams_api_runner import run_ams_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: query_affiliate_list.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_ams_api("query_affiliate_list", params, "query_affiliate_list.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
