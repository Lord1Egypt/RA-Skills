#!/usr/bin/env python3
"""Fetch registration events for auditing."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lmail_http import (  # noqa: E402
    LMailHttpError,
    auth_headers,
    expect_success,
    json_pretty,
    load_json_file,
    request_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch registration events")
    parser.add_argument("--base-url", default=os.getenv("LMAIL_BASE_URL", "http://localhost:3001"))
    parser.add_argument("--admin-token")
    parser.add_argument("--admin-api-key")
    parser.add_argument("--credentials-file", default=os.getenv("LMAIL_CREDENTIALS_FILE", ".lmail-credentials.json"))
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--event-type")
    parser.add_argument("--outcome")
    parser.add_argument("--save")
    parser.add_argument("--timeout", type=int, default=20)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")
    creds = load_json_file(args.credentials_file)

    token = args.admin_token or creds.get("token")
    api_key = args.admin_api_key or creds.get("apiKey")

    query: dict[str, str | int] = {"limit": args.limit, "offset": args.offset}
    if args.event_type:
        query["eventType"] = args.event_type
    if args.outcome:
        query["outcome"] = args.outcome

    url = f"{base_url}/api/v1/admin/registration/events?{urlencode(query)}"
    status, events_resp = request_json(
        url=url,
        method="GET",
        headers=auth_headers(token=token, api_key=api_key),
        timeout=args.timeout,
    )
    if status >= 400:
        raise LMailHttpError(f"registration/events failed with HTTP {status}: {events_resp}")

    events_data = expect_success(events_resp, "registration/events")
    output = {
        "ok": True,
        "step": "admin_fetch_registration_events",
        "count": len(events_data) if isinstance(events_data, list) else None,
        "data": events_data,
    }

    if args.save:
        Path(args.save).write_text(json_pretty(output) + "\n", encoding="utf-8")

    print(json_pretty(output))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LMailHttpError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
