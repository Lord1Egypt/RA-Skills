#!/usr/bin/env python3
"""
Shopee Store — get_shop_toggle_info

官方: https://open.shopee.com/documents/v2/v2.ads.get_shop_toggle_info?module=117&type=1

入参说明见 references/apis/get-shop-toggle-info.md。
"""

from __future__ import annotations

import json
import sys

from _ads_api_runner import run_ads_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_shop_toggle_info.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_ads_api("get_shop_toggle_info", params, "get_shop_toggle_info.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
