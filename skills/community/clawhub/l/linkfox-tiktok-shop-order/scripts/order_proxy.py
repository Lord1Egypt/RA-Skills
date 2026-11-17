#!/usr/bin/env python3
"""TikTok Shop ERP Order — generic developerProxy caller (appType=erp)."""

from __future__ import annotations

import json
import sys

from _order_api_runner import run_order_proxy


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: order_proxy.py '<JSON>'\n"
            "Required: openId, path, method\n"
            "order/* paths need shop_cipher (auto if only 1 authorized shop)",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_order_proxy(params), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
