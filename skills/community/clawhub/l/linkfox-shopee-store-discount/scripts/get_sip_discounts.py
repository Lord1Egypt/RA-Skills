#!/usr/bin/env python3
"""
Shopee Store — get_sip_discounts

官方: https://open.shopee.com/documents/v2/v2.discount.get_sip_discounts?module=99&type=1

入参说明见 references/apis/get-sip-discounts.md。
"""

from __future__ import annotations

import json
import sys

from _discount_api_runner import run_discount_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_sip_discounts.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_discount_api("get_sip_discounts", params, "get_sip_discounts.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
