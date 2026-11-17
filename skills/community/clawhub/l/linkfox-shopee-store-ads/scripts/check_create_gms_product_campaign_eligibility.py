#!/usr/bin/env python3
"""
Shopee Store — check_create_gms_product_campaign_eligibility

官方: https://open.shopee.com/documents/v2/v2.ads.check_create_gms_product_campaign_eligibility?module=117&type=1

入参说明见 references/apis/check-create-gms-product-campaign-eligibility.md。
"""

"""
Shopee Store — check_create_gms_product_campaign_eligibility (v2.ads.check_create_gms_product_campaign_eligibility)
官方: https://open.shopee.com/documents/v2/v2.ads.check_create_gms_product_campaign_eligibility?module=117&type=1
"""

from __future__ import annotations

import json
import sys

from _ads_api_runner import run_ads_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: check_create_gms_product_campaign_eligibility.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_ads_api("check_create_gms_product_campaign_eligibility", params, "check_create_gms_product_campaign_eligibility.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
