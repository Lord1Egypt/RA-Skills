#!/usr/bin/env python3
"""
Shopee Store — get_metric_source_detail (v2.account_health.get_metric_source_detail)

官方: https://open.shopee.com/documents/v2/v2.account_health.get_metric_source_detail?module=103&type=1

入参说明见 references/apis/get-metric-source-detail.md。

Usage:
  python get_metric_source_detail.py '{"shopId":"67890","metric_id":3,"page_no":1,"page_size":20}'
"""

from __future__ import annotations

import json
import sys

from _account_health_api_runner import run_account_health_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_metric_source_detail.py '<JSON>'\n"
            "Required: shopId OR merchantId, metric_id\n"
            "Optional: page_no (default 1), page_size (1-100, default 10)\n"
            "See references/apis/get-metric-source-detail.md for full parameter docs.",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_account_health_api(
                "get_metric_source_detail", params, "get_metric_source_detail.py"
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
