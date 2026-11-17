#!/usr/bin/env python3
"""
Shopee Store — publish_item_to_outlet_shop

官方: https://open.shopee.com/documents/v2/v2.product.publish_item_to_outlet_shop?module=89&type=1

入参说明见 references/apis/publish-item-to-outlet-shop.md。
"""

from __future__ import annotations

import json
import sys

from _product_api_runner import run_product_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: publish_item_to_outlet_shop.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_product_api("publish_item_to_outlet_shop", params, "publish_item_to_outlet_shop.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
