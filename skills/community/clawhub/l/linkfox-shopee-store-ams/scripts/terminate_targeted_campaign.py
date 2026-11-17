#!/usr/bin/env python3
"""
Shopee Store — terminate_targeted_campaign

官方: https://open.shopee.com/documents/v2/v2.ams.terminate_targeted_campaign?module=127&type=1

入参说明见 references/apis/terminate-targeted-campaign.md。
"""

from __future__ import annotations

import json
import sys

from _ams_api_runner import run_ams_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: terminate_targeted_campaign.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_ams_api("terminate_targeted_campaign", params, "terminate_targeted_campaign.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
