#!/usr/bin/env python3
"""
Shopee Store — get_shipping_carrier

官方: https://open.shopee.com/documents/v2/v2.returns.get_shipping_carrier?module=102&type=1

入参说明见 references/apis/get-shipping-carrier.md。
"""

from __future__ import annotations

import json
import sys

from _returns_api_runner import run_returns_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_shipping_carrier.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_returns_api("get_shipping_carrier", params, "get_shipping_carrier.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
