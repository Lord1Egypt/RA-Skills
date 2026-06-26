#!/usr/bin/env python3
"""Login with phone and verification code."""

import argparse
from typing import Any, Dict

from client_common import has_error, load_env_file, post_json, print_json, require_env, save_session


def login(phone: str, verify_code: str, session_id: str = "") -> Dict[str, Any]:
    api_base_url = require_env("API_BASE_URL").rstrip("/")
    token = require_env("CLAWHUB_SKILL_TOKEN")

    payload: Dict[str, Any] = {
        "phone": phone,
        "verify_code": verify_code,
    }
    if session_id:
        payload["session_id"] = session_id

    url = f"{api_base_url}/session/login"
    return post_json(url, payload, token=token)


def main() -> None:
    parser = argparse.ArgumentParser(description="Login and create/reuse session")
    parser.add_argument("--env", default=".env", help="Path to env file, default: .env")
    parser.add_argument("--phone", required=True, help="Phone number")
    parser.add_argument("--verify-code", required=True, help="Verification code")
    parser.add_argument("--session-id", default="", help="Optional existing session id")
    parser.add_argument(
        "--session-file",
        default=".session.json",
        help="Where to persist user_id/session_id, default: .session.json",
    )
    args = parser.parse_args()

    load_env_file(args.env)
    result = login(args.phone, args.verify_code, args.session_id)

    if has_error(result):
        print_json(result)
        raise SystemExit(1)

    if result.get("user_id") and result.get("session_id"):
        save_session(
            {
                "user_id": result["user_id"],
                "session_id": result["session_id"],
            },
            path=args.session_file,
        )
    else:
        print_json(result)
        raise SystemExit("[ERROR] login response missing user_id/session_id")

    print_json(result)


if __name__ == "__main__":
    main()
