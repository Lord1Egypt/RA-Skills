#!/usr/bin/env python3
"""
Shopee Store — get_targeted_campaign_settings

官方: https://open.shopee.com/documents/v2/v2.ams.get_targeted_campaign_settings?module=127&type=1

入参说明见 references/apis/get-targeted-campaign-settings.md。
"""

from __future__ import annotations

import json
import sys

from _ams_api_runner import run_ams_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_targeted_campaign_settings.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_ams_api("get_targeted_campaign_settings", params, "get_targeted_campaign_settings.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
