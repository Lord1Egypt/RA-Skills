#!/usr/bin/env python3
"""Send SMS verification code."""

import argparse
from typing import Any, Dict

from client_common import has_error, load_env_file, post_json, print_json, require_env


def send_code(phone: str) -> Dict[str, Any]:
    site_base_url = require_env("SITE_BASE_URL").rstrip("/")
    url = f"{site_base_url}/chainlit/send-verification-code"
    return post_json(url, {"phone": phone})


def main() -> None:
    parser = argparse.ArgumentParser(description="Send verification code")
    parser.add_argument("--env", default=".env", help="Path to env file, default: .env")
    parser.add_argument("--phone", required=True, help="Phone number, e.g. 13800138000")
    args = parser.parse_args()

    load_env_file(args.env)
    result = send_code(args.phone)
    print_json(result)
    if has_error(result):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
