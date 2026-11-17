#!/usr/bin/env python3
"""TikTok Shop ERP Product — generic developerProxy caller (appType=erp).

Usage:
  python product_proxy.py '{"openId":"...","path":"product/202312/prerequisites","method":"GET"}'
"""

from __future__ import annotations

import json
import sys

from _product_api_runner import run_product_proxy


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage: product_proxy.py '<JSON>'\n"
            "Required: openId, path, method\n"
            "product/* paths also need shop_cipher (auto if only 1 authorized shop)",
            file=sys.stderr,
        )
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_product_proxy(params), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
