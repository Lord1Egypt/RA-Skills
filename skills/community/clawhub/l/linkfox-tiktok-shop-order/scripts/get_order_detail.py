#!/usr/bin/env python3
"""TikTok Shop ERP Order — get_order_detail
Order detail 202507

Usage:
  python get_order_detail.py '<JSON>'
"""

from __future__ import annotations

import json
import sys

from _order_api_runner import run_order_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_order_detail.py '<JSON>'\n"
            "Hint: openId, ids (string or string[])\n"
            "Auth: openId (linkfox-tiktok-shop-auth; token backendized)\n"
            "order APIs need shop_cipher (auto if only 1 shop)",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_order_api("get_order_detail", params, "get_order_detail.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
