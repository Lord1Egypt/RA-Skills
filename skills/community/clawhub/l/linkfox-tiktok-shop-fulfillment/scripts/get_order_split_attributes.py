#!/usr/bin/env python3
"""TikTok Shop ERP Fulfillment — get_order_split_attributes

Get whether orders can/must be split and related split attributes.
Official: https://partner.tiktokshop.com/docv2/page/get-order-split-attributes-202309

Usage:
  python get_order_split_attributes.py '{"openId":"...","order_ids":["5764..."]}'
  python get_order_split_attributes.py '{"openId":"...","order_ids":"5764...,5765..."}'
"""

from __future__ import annotations

import json
import sys

from _fulfillment_api_runner import run_fulfillment_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_order_split_attributes.py '<JSON>'\n"
            "Hint: openId, order_ids (string or string[])\n"
            "Auth: openId (linkfox-tiktok-shop-auth; token backendized)\n"
            "Needs shop_cipher (auto if only 1 shop)",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(
        json.dumps(
            run_fulfillment_api(
                "get_order_split_attributes", params, "get_order_split_attributes.py"
            ),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
