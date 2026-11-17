#!/usr/bin/env python3
"""
Shopee Store — get_recommended_affiliate_list

官方: https://open.shopee.com/documents/v2/v2.ams.get_recommended_affiliate_list?module=127&type=1

入参说明见 references/apis/get-recommended-affiliate-list.md。
"""

from __future__ import annotations

import json
import sys

from _ams_api_runner import run_ams_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_recommended_affiliate_list.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_ams_api("get_recommended_affiliate_list", params, "get_recommended_affiliate_list.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
