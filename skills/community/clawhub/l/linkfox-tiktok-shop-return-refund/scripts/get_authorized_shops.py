#!/usr/bin/env python3
"""TikTok Shop ERP return_refund — get_authorized_shops"""

from __future__ import annotations

import json
import sys

from _return_refund_api_runner import run_return_refund_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_authorized_shops.py '<JSON>'\n"
            "Hint: openId\n"
            "Auth: openId (linkfox-tiktok-shop-auth; token backendized)",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_return_refund_api("get_authorized_shops", params, "get_authorized_shops.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
