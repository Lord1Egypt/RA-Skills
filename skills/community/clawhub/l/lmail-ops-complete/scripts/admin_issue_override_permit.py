#!/usr/bin/env python3
"""Issue admin override permit for registration cooldown exceptions."""

from __future__ import annotations

import argparse
import json
import os
import sys
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
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Issue admin override permit")
    parser.add_argument("--base-url", default=os.getenv("LMAIL_BASE_URL", "http://localhost:3001"))
    parser.add_argument("--admin-token")
    parser.add_argument("--admin-api-key")
    parser.add_argument("--credentials-file", default=os.getenv("LMAIL_CREDENTIALS_FILE", ".lmail-credentials.json"))
    parser.add_argument("--reason", required=True)
    parser.add_argument("--save-permit", help="path to store permit token")
    parser.add_argument("--show-permit", action="store_true")
    parser.add_argument("--timeout", type=int, default=20)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")
    creds = load_json_file(args.credentials_file)

    token = args.admin_token or creds.get("token")
    api_key = args.admin_api_key or creds.get("apiKey")

    status, override_resp = request_json(
        url=f"{base_url}/api/v1/admin/registration/override-permit",
        method="POST",
        headers=auth_headers(token=token, api_key=api_key),
        payload={"reason": args.reason},
        timeout=args.timeout,
    )
    if status >= 400:
        raise LMailHttpError(f"override-permit failed with HTTP {status}: {override_resp}")

    override_data = expect_success(override_resp, "override-permit")
    permit = str(override_data.get("permit") or "")

    if args.save_permit and permit:
        Path(args.save_permit).write_text(permit + "\n", encoding="utf-8")
        try:
            os.chmod(args.save_permit, 0o600)
        except OSError:
            pass

    result = {
        "ok": True,
        "step": "admin_issue_override_permit",
        "reason": args.reason,
        "permitMasked": mask_secret(permit),
        "expiresAt": override_data.get("expiresAt"),
        "savePermit": args.save_permit,
    }
    if args.show_permit:
        result["permit"] = permit

    print(json_pretty(result))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LMailHttpError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
