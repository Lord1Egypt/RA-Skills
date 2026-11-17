#!/usr/bin/env python3
"""TikTok Shop ERP — delete_products
Delete products

Usage:
  python delete_products.py '<JSON>'
"""

from __future__ import annotations

import json
import sys

from _product_api_runner import run_product_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: delete_products.py '<JSON>'\n"
            "Hint: openId, product_ids\n"
            "Auth: openId (linkfox-tiktok-shop-auth; token backendized)\n"
            "Most product APIs need shop_cipher (auto if only 1 shop)",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_product_api("delete_products", params, "delete_products.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
