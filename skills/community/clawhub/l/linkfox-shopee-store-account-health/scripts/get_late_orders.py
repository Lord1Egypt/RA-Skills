#!/usr/bin/env python3
"""
Shopee Store — get_late_orders (v2.account_health.get_late_orders)

官方: https://open.shopee.com/documents/v2/v2.account_health.get_late_orders?module=103&type=1

入参说明见 references/apis/get-late-orders.md。

Usage:
  python get_late_orders.py '{"shopId":"67890","page_no":1,"page_size":20}'
"""

from __future__ import annotations

import json
import sys

from _account_health_api_runner import run_account_health_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_late_orders.py '<JSON>'\n"
            "Required: shopId OR merchantId\n"
            "Optional: page_no (default 1), page_size (1-100, default 10)\n"
            "See references/apis/get-late-orders.md for full parameter docs.",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_account_health_api("get_late_orders", params, "get_late_orders.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
