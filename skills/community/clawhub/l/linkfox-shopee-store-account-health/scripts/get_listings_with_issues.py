#!/usr/bin/env python3
"""
Shopee Store — get_listings_with_issues (v2.account_health.get_listings_with_issues)

官方: https://open.shopee.com/documents/v2/v2.account_health.get_listings_with_issues?module=103&type=1

入参说明见 references/apis/get-listings-with-issues.md。

Usage:
  python get_listings_with_issues.py '{"shopId":"67890","page_no":1,"page_size":50}'
"""

from __future__ import annotations

import json
import sys

from _account_health_api_runner import run_account_health_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_listings_with_issues.py '<JSON>'\n"
            "Required: shopId OR merchantId\n"
            "Optional: page_no (default 1), page_size (1-100, default 10)\n"
            "See references/apis/get-listings-with-issues.md for full parameter docs.",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_account_health_api(
                "get_listings_with_issues", params, "get_listings_with_issues.py"
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
