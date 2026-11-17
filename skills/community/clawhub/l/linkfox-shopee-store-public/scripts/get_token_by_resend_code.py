#!/usr/bin/env python3
"""
Shopee Store — get_token_by_resend_code

官方: https://open.shopee.com/documents/v2/v2.public.get_token_by_resend_code?module=104&type=1

入参说明见 references/apis/get-token-by-resend-code.md。
"""

from __future__ import annotations

import json
import sys

from _public_api_runner import run_public_api


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: get_token_by_resend_code.py '<JSON>'", file=sys.stderr)
        sys.exit(1)
    params = json.loads(sys.argv[1])
    print(json.dumps(run_public_api("get_token_by_resend_code", params, "get_token_by_resend_code.py"), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
