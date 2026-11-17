#!/usr/bin/env python3
"""TikTok Shop ERP Logistics — get_warehouse_list

Get warehouse list for the shop.
Official: https://partner.tiktokshop.com/docv2/page/get-warehouse-list-202309

Usage:
  python get_warehouse_list.py '{"openId":"..."}'
  python get_warehouse_list.py '{"openId":"...","shop_cipher":"GCP_..."}'
"""

from __future__ import annotations

import json
import sys

from _logistics_api_runner import run_logistics_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_warehouse_list.py '<JSON>'\n"
            "Hint: openId\n"
            "Auth: openId (linkfox-tiktok-shop-auth; token backendized)\n"
            "Needs shop_cipher (auto if only 1 shop)",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_logistics_api("get_warehouse_list", params, "get_warehouse_list.py"),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
