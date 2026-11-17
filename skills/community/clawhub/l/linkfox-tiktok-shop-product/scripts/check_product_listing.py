#!/usr/bin/env python3
"""TikTok Shop ERP — check_product_listing
Listing validation

Usage:
  python check_product_listing.py '<JSON>'
"""

from __future__ import annotations

import json
import sys

from _product_api_runner import run_product_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: check_product_listing.py '<JSON>'\n"
            "Hint: openId + requestBody\n"
            "Auth: openId (linkfox-tiktok-shop-auth; token backendized)\n"
            "Most product APIs need shop_cipher (auto if only 1 shop)",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_product_api("check_product_listing", params, "check_product_listing.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
