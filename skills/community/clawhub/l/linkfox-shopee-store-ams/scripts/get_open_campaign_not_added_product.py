#!/usr/bin/env python3
"""
Shopee Store — get_open_campaign_not_added_product

官方: https://open.shopee.com/documents/v2/v2.ams.get_open_campaign_not_added_product?module=127&type=1

入参说明见 references/apis/get-open-campaign-not-added-product.md。
"""

from __future__ import annotations

import json
import sys

from _ams_api_runner import run_ams_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_open_campaign_not_added_product.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_ams_api("get_open_campaign_not_added_product", params, "get_open_campaign_not_added_product.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
