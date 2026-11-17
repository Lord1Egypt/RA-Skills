#!/usr/bin/env python3
"""
Shopee Store — get_penalty_point_history (v2.account_health.get_penalty_point_history)

官方: https://open.shopee.com/documents/v2/v2.account_health.get_penalty_point_history?module=103&type=1

入参说明见 references/apis/get-penalty-point-history.md。

Usage:
  python get_penalty_point_history.py '{"shopId":"67890","page_no":1,"page_size":50}'
  python get_penalty_point_history.py '{"shopId":"67890","violation_type":5,"page_size":20}'
"""

from __future__ import annotations

import json
import sys

from _account_health_api_runner import run_account_health_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_penalty_point_history.py '<JSON>'\n"
            "Required: shopId OR merchantId\n"
            "Optional: page_no (default 1), page_size (1-100, default 10), violation_type\n"
            "See references/apis/get-penalty-point-history.md for full parameter docs.",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_account_health_api(
                "get_penalty_point_history", params, "get_penalty_point_history.py"
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
