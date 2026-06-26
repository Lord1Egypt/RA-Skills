#!/usr/bin/env python3
"""Poll LMail inbox and optionally acknowledge required messages."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from urllib.parse import urlencode
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from lmail_http import (  # noqa: E402
    LMailHttpError,
    auth_headers,
    expect_success,
    load_json_file,
    request_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Poll inbox messages")
    parser.add_argument("--base-url", default=os.getenv("LMAIL_BASE_URL", "http://localhost:3001"))
    parser.add_argument("--token")
    parser.add_argument("--api-key")
    parser.add_argument("--credentials-file", default=os.getenv("LMAIL_CREDENTIALS_FILE", ".lmail-credentials.json"))
    parser.add_argument("--interval-seconds", type=float, default=5.0)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--sort", choices=["asc", "desc"], default="desc")
    parser.add_argument("--unread", action="store_true", default=True)
    parser.add_argument("--max-iterations", type=int, default=1)
    parser.add_argument("--forever", action="store_true")
    parser.add_argument("--auto-ack", action="store_true")
    parser.add_argument("--timeout", type=int, default=20)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")
    creds = load_json_file(args.credentials_file)
    token = args.token or creds.get("token")
    api_key = args.api_key or creds.get("apiKey")

    iteration = 0
    while True:
        iteration += 1
        query = urlencode(
            {
                "unread": str(bool(args.unread)).lower(),
                "limit": args.limit,
                "sort": args.sort,
            }
        )
        url = f"{base_url}/api/v1/messages/inbox?{query}"

        status, inbox_resp = request_json(
            url=url,
            method="GET",
            headers=auth_headers(token=token, api_key=api_key),
            timeout=args.timeout,
        )
        if status >= 400:
            raise LMailHttpError(f"inbox failed with HTTP {status}: {inbox_resp}")

        inbox_data = expect_success(inbox_resp, "inbox")
        messages = inbox_data if isinstance(inbox_data, list) else []

        print(f"iteration={iteration} messages={len(messages)}")
        for msg in messages:
            msg_id = msg.get("id")
            from_addr = msg.get("fromAddress") or msg.get("from")
            subject = msg.get("subject")
            require_ack = bool(msg.get("requireAck"))
            print(f"- id={msg_id} from={from_addr} subject={subject!r} requireAck={require_ack}")

            if args.auto_ack and require_ack and msg_id:
                ack_url = f"{base_url}/api/v1/messages/{msg_id}/ack"
                ack_status, ack_resp = request_json(
                    url=ack_url,
                    method="POST",
                    headers=auth_headers(token=token, api_key=api_key),
                    payload={},
                    timeout=args.timeout,
                )
                if ack_status >= 400:
                    print(f"  ack failed for {msg_id}: {ack_resp}")
                else:
                    _ = expect_success(ack_resp, "ack")
                    print(f"  ack ok for {msg_id}")

        if not args.forever and iteration >= args.max_iterations:
            break
        time.sleep(args.interval_seconds)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LMailHttpError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
