#!/usr/bin/env python3
"""
Shopee Store — get_shopee_ip_ranges

官方: https://open.shopee.com/documents/v2/v2.public.get_shopee_ip_ranges?module=104&type=1

入参说明见 references/apis/get-shopee-ip-ranges.md。
"""

from __future__ import annotations

import json
import sys

from _public_api_runner import run_public_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_shopee_ip_ranges.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_public_api("get_shopee_ip_ranges", params, "get_shopee_ip_ranges.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
