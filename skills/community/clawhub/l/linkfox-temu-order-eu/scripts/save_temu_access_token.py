#!/usr/bin/env python3
"""
Save Temu accessToken to local store for reuse in proxy/fileDownload calls.

Usage:
  python save_temu_access_token.py '{
    "storeKey": "my-shop",
    "site": "cn",
    "managementType": "semi-managed",
    "tokenPurpose": "product-inventory",
    "accessToken": "PASTE_TOKEN_HERE",
    "label": "中国半托管主店"
  }'
"""

import json
import sys

from _temu_common import load_json_arg, require_text, validate_management_type, validate_site
from _temu_token_store import save_token

def main():
    if len(sys.argv) < 2:
        print("Usage: save_temu_access_token.py '<JSON parameters>'", file=sys.stderr)
        sys.exit(1)

    params = load_json_arg(sys.argv)
    store_key = require_text(params, "storeKey")
    site = validate_site(require_text(params, "site"))
    management_type = validate_management_type(require_text(params, "managementType"))
    access_token = require_text(params, "accessToken")
    token_purpose = str(params.get("tokenPurpose", "default")).strip() or "default"
    label = params.get("label")

    result = save_token(
        store_key=store_key,
        site=site,
        management_type=management_type,
        access_token=access_token,
        token_purpose=token_purpose,
        label=label,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
