#!/usr/bin/env python3
"""Send one LMail message with optional thread metadata."""

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
    request_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send reply/message")
    parser.add_argument("--base-url", default=os.getenv("LMAIL_BASE_URL", "http://localhost:3001"))
    parser.add_argument("--token")
    parser.add_argument("--api-key")
    parser.add_argument("--credentials-file", default=os.getenv("LMAIL_CREDENTIALS_FILE", ".lmail-credentials.json"))
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body-text", required=True)
    parser.add_argument("--structured-json")
    parser.add_argument("--structured-file")
    parser.add_argument("--content-type", default="task_report")
    parser.add_argument("--priority", default="normal")
    parser.add_argument("--thread-id")
    parser.add_argument("--reply-to-id")
    parser.add_argument("--require-ack", action="store_true")
    parser.add_argument("--timeout", type=int, default=20)
    return parser.parse_args()


def load_structured(args: argparse.Namespace) -> dict[str, object] | None:
    if args.structured_json:
        return json.loads(args.structured_json)
    if args.structured_file:
        return json.loads(Path(args.structured_file).read_text(encoding="utf-8"))
    return None


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")
    creds = load_json_file(args.credentials_file)

    token = args.token or creds.get("token")
    api_key = args.api_key or creds.get("apiKey")

    payload: dict[str, object] = {
        "to": args.to,
        "subject": args.subject,
        "body": {
            "text": args.body_text,
        },
        "contentType": args.content_type,
        "priority": args.priority,
        "requireAck": args.require_ack,
    }

    structured = load_structured(args)
    if structured is not None:
        payload["body"]["structured"] = structured

    if args.thread_id:
        payload["threadId"] = args.thread_id
    if args.reply_to_id:
        payload["replyToId"] = args.reply_to_id

    status, send_resp = request_json(
        url=f"{base_url}/api/v1/messages/send",
        method="POST",
        headers=auth_headers(token=token, api_key=api_key),
        payload=payload,
        timeout=args.timeout,
    )
    if status >= 400:
        raise LMailHttpError(f"send failed with HTTP {status}: {send_resp}")

    send_data = expect_success(send_resp, "send")
    print(
        json_pretty(
            {
                "ok": True,
                "step": "send_reply",
                "messageId": send_data.get("id") or send_data.get("messageId"),
                "threadId": send_data.get("threadId") or args.thread_id,
                "to": args.to,
                "subject": args.subject,
            }
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (LMailHttpError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
