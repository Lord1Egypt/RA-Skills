#!/usr/bin/env python3
"""
Shopee Store — create_gms_product_campaign

官方: https://open.shopee.com/documents/v2/v2.ads.create_gms_product_campaign?module=117&type=1

入参说明见 references/apis/create-gms-product-campaign.md。
"""

from __future__ import annotations

import json
import sys

from _ads_api_runner import run_ads_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: create_gms_product_campaign.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_ads_api("create_gms_product_campaign", params, "create_gms_product_campaign.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
