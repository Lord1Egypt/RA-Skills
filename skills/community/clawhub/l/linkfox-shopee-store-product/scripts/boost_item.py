#!/usr/bin/env python3
"""
Shopee Store — boost_item

官方: https://open.shopee.com/documents/v2/v2.product.boost_item?module=89&type=1

入参说明见 references/apis/boost-item.md。
"""

from __future__ import annotations

import json
import sys

from _product_api_runner import run_product_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: boost_item.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_product_api("boost_item", params, "boost_item.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
