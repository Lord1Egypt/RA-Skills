#!/usr/bin/env python3
"""
TikTok Video Products — get_shop_products (Get Shop Products 202509)
官方: https://partner.tiktokshop.com/docv2/page/get-shop-products-202509

Usage:
  python get_shop_products.py '{"openId": "...", "page_size": 20}'
  python get_shop_products.py '{"openId": "...", "title_keyword": "apple", "page_size": 20}'
"""

from __future__ import annotations

import json
import sys

from _products_api_runner import run_products_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_shop_products.py '<JSON>'\n"
            "Required: openId, page_size (default 20)\n"
            "Optional: title_keyword, sort_field, sort_order, page_token\n"
            "Returns product_id for use in linkfox-tiktok-video precheck/post APIs",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    params.setdefault("page_size", 20)
    print(
        json.dumps(
            run_products_api("get_shop_products", params, "get_shop_products.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
