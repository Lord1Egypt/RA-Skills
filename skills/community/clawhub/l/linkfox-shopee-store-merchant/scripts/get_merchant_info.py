#!/usr/bin/env python3
"""
Shopee Store — get_merchant_info

官方: https://open.shopee.com/documents/v2/v2.merchant.get_merchant_info?module=93&type=1

入参说明见 references/apis/get-merchant-info.md。
"""

from __future__ import annotations

import json
import sys

from _merchant_api_runner import run_merchant_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_merchant_info.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_merchant_api("get_merchant_info", params, "get_merchant_info.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
