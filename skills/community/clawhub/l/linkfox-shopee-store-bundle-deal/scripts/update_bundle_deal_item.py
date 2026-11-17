#!/usr/bin/env python3
"""
Shopee Store — update_bundle_deal_item

官方: https://open.shopee.com/documents/v2/v2.bundle_deal.update_bundle_deal_item?module=110&type=1

入参说明见 references/apis/update-bundle-deal-item.md。
"""

from __future__ import annotations

import json
import sys

from _bundle_deal_api_runner import run_bundle_deal_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: update_bundle_deal_item.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_bundle_deal_api("update_bundle_deal_item", params, "update_bundle_deal_item.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
