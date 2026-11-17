#!/usr/bin/env python3
"""
Shopee Store — remove_all_products_open_campaign_setting

官方: https://open.shopee.com/documents/v2/v2.ams.remove_all_products_open_campaign_setting?module=127&type=1

入参说明见 references/apis/remove-all-products-open-campaign-setting.md。
"""

from __future__ import annotations

import json
import sys

from _ams_api_runner import run_ams_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: remove_all_products_open_campaign_setting.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_ams_api("remove_all_products_open_campaign_setting", params, "remove_all_products_open_campaign_setting.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
