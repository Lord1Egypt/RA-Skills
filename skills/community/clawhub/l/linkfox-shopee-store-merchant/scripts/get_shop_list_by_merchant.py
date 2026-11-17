#!/usr/bin/env python3
"""
Shopee Store — get_shop_list_by_merchant

官方: https://open.shopee.com/documents/v2/v2.merchant.get_shop_list_by_merchant?module=93&type=1

入参说明见 references/apis/get-shop-list-by-merchant.md。
"""

from __future__ import annotations

import json
import sys

from _merchant_api_runner import run_merchant_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_shop_list_by_merchant.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_merchant_api("get_shop_list_by_merchant", params, "get_shop_list_by_merchant.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
