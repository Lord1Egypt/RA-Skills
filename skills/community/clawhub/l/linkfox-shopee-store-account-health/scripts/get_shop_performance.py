#!/usr/bin/env python3
"""
Shopee Store — get_shop_performance (v2.account_health.get_shop_performance)

官方: https://open.shopee.com/documents/v2/v2.account_health.get_shop_performance?module=103&type=1

入参说明见 references/apis/get-shop-performance.md。

Usage:
  python get_shop_performance.py '{"shopId":"67890"}'
"""

from __future__ import annotations

import json
import sys

from _account_health_api_runner import run_account_health_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_shop_performance.py '<JSON>'\n"
            "Required: shopId OR merchantId\n"
            "See references/apis/get-shop-performance.md for full parameter docs.",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_account_health_api("get_shop_performance", params, "get_shop_performance.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
