#!/usr/bin/env python3
"""
Shopee Store — get_punishment_history (v2.account_health.get_punishment_history)

官方: https://open.shopee.com/documents/v2/v2.account_health.get_punishment_history?module=103&type=1

入参说明见 references/apis/get-punishment-history.md。

Usage:
  python get_punishment_history.py '{"shopId":"67890","punishment_status":1,"page_size":20}'
"""

from __future__ import annotations

import json
import sys

from _account_health_api_runner import run_account_health_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_punishment_history.py '<JSON>'\n"
            "Required: shopId OR merchantId, punishment_status (1=Ongoing, 2=Ended)\n"
            "Optional: page_no (default 1), page_size (1-100, default 10)\n"
            "See references/apis/get-punishment-history.md for full parameter docs.",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_account_health_api(
                "get_punishment_history", params, "get_punishment_history.py"
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
