#!/usr/bin/env python3
"""
Shopee Store — update_stock

官方: https://open.shopee.com/documents/v2/v2.global_product.update_stock?module=90&type=1

入参说明见 references/apis/update-stock.md。
"""

from __future__ import annotations

import json
import sys

from _global_product_api_runner import run_global_product_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: update_stock.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_global_product_api("update_stock", params, "update_stock.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
