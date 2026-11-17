#!/usr/bin/env python3
"""TikTok Shop ERP return_refund — get_reject_reasons

Usage:
  python get_reject_reasons.py '<JSON>'
"""

from __future__ import annotations

import json
import sys

from _return_refund_api_runner import run_return_refund_api


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: get_reject_reasons.py '<JSON>'\n"
            "Hint: openId, return_or_cancel_id\n"
            "Auth: openId (linkfox-tiktok-shop-auth; token backendized)\n"
            "Needs shop_cipher (auto if only 1 shop)",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_return_refund_api("get_reject_reasons", params, "get_reject_reasons.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
