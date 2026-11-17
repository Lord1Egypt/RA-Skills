#!/usr/bin/env python3
"""
Shopee Store — get_local_adjustment_rate

官方: https://open.shopee.com/documents/v2/v2.global_product.get_local_adjustment_rate?module=90&type=1

入参说明见 references/apis/get-local-adjustment-rate.md。
"""

from __future__ import annotations

import json
import sys

from _global_product_api_runner import run_global_product_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_local_adjustment_rate.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_global_product_api("get_local_adjustment_rate", params, "get_local_adjustment_rate.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
