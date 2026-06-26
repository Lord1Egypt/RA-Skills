#!/usr/bin/env python3
"""Login using API key then verify account identity."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lmail_http import (  # noqa: E402
    LMailHttpError,
    auth_headers,
    expect_success,
    json_pretty,
    load_json_file,
    mask_secret,
    request_json,
    save_json_file,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Login and verify account")
    parser.add_argument("--base-url", default=os.getenv("LMAIL_BASE_URL", "http://localhost:3001"))
    parser.add_argument("--api-key", help="API key, fallback to credentials file")
    parser.add_argument("--credentials-file", default=os.getenv("LMAIL_CREDENTIALS_FILE", ".lmail-credentials.json"))
    parser.add_argument("--timeout", type=int, default=20)
    return parser.parse_args()


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")

    creds = load_json_file(args.credentials_file)
    api_key = args.api_key or creds.get("apiKey")
    if not api_key:
        raise LMailHttpError("Missing API key; provide --api-key or ensure credentials file has apiKey")

    status, login_resp = request_json(
        url=f"{base_url}/api/v1/auth/login",
        method="POST",
        payload={"apiKey": api_key},
        timeout=args.timeout,
    )
    if status >= 400:
        raise LMailHttpError(f"login failed with HTTP {status}: {login_resp}")

    login_data = expect_success(login_resp, "login")
    token = str(login_data.get("token") or "")
    if not token:
        raise LMailHttpError("login response missing token")

    status, verify_resp = request_json(
        url=f"{base_url}/api/v1/auth/verify",
        method="GET",
        headers=auth_headers(token=token),
        timeout=args.timeout,
    )
    if status >= 400:
        raise LMailHttpError(f"verify failed with HTTP {status}: {verify_resp}")

    verify_data = expect_success(verify_resp, "verify")

    merged = dict(creds)
    merged.update(
        {
            "baseUrl": base_url,
            "apiKey": api_key,
            "token": token,
            "verifiedAt": now_iso(),
            "address": verify_data.get("address", creds.get("address")),
            "displayName": verify_data.get("displayName", creds.get("displayName")),
        }
    )
    save_json_file(args.credentials_file, merged)

    print(
        json_pretty(
            {
                "ok": True,
                "step": "login_verify",
                "account": {
                    "id": verify_data.get("id"),
                    "address": verify_data.get("address"),
                    "displayName": verify_data.get("displayName"),
                    "role": verify_data.get("role"),
                    "status": verify_data.get("status"),
                },
                "tokenMasked": mask_secret(token),
                "apiKeyMasked": mask_secret(str(api_key)),
                "credentialsFile": args.credentials_file,
            }
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LMailHttpError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
