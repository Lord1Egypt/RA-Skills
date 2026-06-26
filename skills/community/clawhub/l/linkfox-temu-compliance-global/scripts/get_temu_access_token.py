#!/usr/bin/env python3
"""
Get Temu accessToken from local store.

Usage:
  python get_temu_access_token.py '{
    "storeKey": "my-shop",
    "site": "cn",
    "managementType": "semi-managed",
    "tokenPurpose": "product-inventory"
  }'
"""

import json
import sys

from _temu_common import load_json_arg, require_text, validate_management_type, validate_site
from _temu_token_store import get_token

def main():
    if len(sys.argv) < 2:
        print("Usage: get_temu_access_token.py '<JSON parameters>'", file=sys.stderr)
        sys.exit(1)

    params = load_json_arg(sys.argv)
    store_key = require_text(params, "storeKey")
    site = validate_site(require_text(params, "site"))
    management_type = validate_management_type(require_text(params, "managementType"))
    token_purpose = str(params.get("tokenPurpose", "default")).strip() or "default"

    token = get_token(store_key, site, management_type, token_purpose)
    if not token:
        print(
            json.dumps(
                {
                    "found": False,
                    "storeKey": store_key,
                    "site": site,
                    "managementType": management_type,
                    "tokenPurpose": token_purpose,
                    "hint": "Run temu_token_guide.py then save_temu_access_token.py",
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        sys.exit(1)

    print(
        json.dumps(
            {
                "found": True,
                "storeKey": store_key,
                "site": site,
                "managementType": management_type,
                "tokenPurpose": token_purpose,
                "accessToken": token,
            },
            indent=2,
            ensure_ascii=False,
        )
    )

if __name__ == "__main__":
    main()
