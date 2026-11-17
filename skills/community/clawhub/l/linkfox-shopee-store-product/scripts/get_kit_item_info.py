#!/usr/bin/env python3
"""
Shopee Store — get_kit_item_info

官方: https://open.shopee.com/documents/v2/v2.product.get_kit_item_info?module=89&type=1

入参说明见 references/apis/get-kit-item-info.md。
"""

from __future__ import annotations

import json
import sys

from _product_api_runner import run_product_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_kit_item_info.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_product_api("get_kit_item_info", params, "get_kit_item_info.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
