#!/usr/bin/env python3
"""Fetch inbox once and print simplified output for quick checks."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
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
    parser = argparse.ArgumentParser(description="Fetch inbox once")
    parser.add_argument("--base-url", default=os.getenv("LMAIL_BASE_URL", "http://localhost:3001"))
    parser.add_argument("--token")
    parser.add_argument("--api-key")
    parser.add_argument("--credentials-file", default=os.getenv("LMAIL_CREDENTIALS_FILE", ".lmail-credentials.json"))
    parser.add_argument("--state-file", default=os.getenv("LMAIL_INBOX_STATE_FILE", ".lmail-inbox-state.json"))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--sort", choices=["asc", "desc"], default="desc")
    parser.add_argument("--unread", action="store_true", default=True)
    parser.add_argument("--from-address")
    parser.add_argument("--subject-contains")
    parser.add_argument("--latest", action="store_true")
    parser.add_argument("--include-body", action="store_true")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--output", choices=["brief", "json"], default="brief")
    return parser.parse_args()


def load_state(path: str) -> dict[str, object]:
    if not path:
        return {}
    state_path = Path(path)
    if not state_path.exists():
        return {}
    try:
        raw = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return raw if isinstance(raw, dict) else {}


def save_state(path: str, payload: dict[str, object]) -> None:
    if not path:
        return
    state_path = Path(path)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")
    creds = load_json_file(args.credentials_file)
    token = args.token or creds.get("token")
    api_key = args.api_key or creds.get("apiKey")

    query = urlencode(
        {
            "unread": str(bool(args.unread)).lower(),
            "limit": args.limit,
            "sort": args.sort,
        }
    )
    status, inbox_resp = request_json(
        url=f"{base_url}/api/v1/messages/inbox?{query}",
        method="GET",
        headers=auth_headers(token=token, api_key=api_key),
        timeout=args.timeout,
    )
    if status >= 400:
        raise LMailHttpError(f"inbox_once failed with HTTP {status}: {inbox_resp}")

    data = expect_success(inbox_resp, "inbox_once")
    messages = data if isinstance(data, list) else []

    filtered = []
    for msg in messages:
        from_addr = str(msg.get("fromAddress") or msg.get("from") or "")
        subject = str(msg.get("subject") or "")

        if args.from_address and from_addr.lower() != args.from_address.lower():
            continue
        if args.subject_contains and args.subject_contains.lower() not in subject.lower():
            continue

        entry = {
            "id": msg.get("id"),
            "from": from_addr,
            "subject": subject,
            "threadId": msg.get("threadId"),
            "requireAck": bool(msg.get("requireAck")),
            "createdAt": msg.get("createdAt"),
        }
        if args.include_body:
            body = msg.get("body") if isinstance(msg.get("body"), dict) else {}
            entry["bodyText"] = body.get("text")
            entry["bodyStructured"] = body.get("structured")
        filtered.append(entry)

    prev_state = load_state(args.state_file)
    previous_message_id = str(prev_state.get("lastMessageId") or "")
    latest_message = filtered[0] if filtered else None
    latest_message_id = str((latest_message or {}).get("id") or "")
    is_new_reply = bool(latest_message_id and latest_message_id != previous_message_id)
    status = "EMPTY" if not filtered else ("NEW_REPLY_RECEIVED" if is_new_reply else "NO_NEW_REPLY")

    if latest_message_id:
        save_state(
            args.state_file,
            {
                "lastMessageId": latest_message_id,
                "lastSeenAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            },
        )

    payload: dict[str, object] = {
        "ok": True,
        "count": len(filtered),
        "status": status,
        "newReply": is_new_reply,
        "messages": filtered,
    }
    if args.latest:
        payload["latest"] = filtered[0] if filtered else None

    if args.output == "json":
        print(json_pretty(payload))
    else:
        print("DONE")
        print(f"INBOX: {status}")
        print(f"- newReply: {'yes' if is_new_reply else 'no'}")
        print(f"- count: {len(filtered)}")
        if latest_message:
            print("LATEST_INBOX:")
            print(f"- from: {latest_message.get('from') or '-'}")
            print(f"- subject: {latest_message.get('subject') or '-'}")
            print(f"- body: {latest_message.get('bodyText') if args.include_body else '[hidden]'}")
            print(f"- time: {latest_message.get('createdAt') or '-'}")
            print(f"- messageId: {latest_message.get('id') or '-'}")
            print(f"- threadId: {latest_message.get('threadId') or '-'}")
        else:
            print("- latest: none")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LMailHttpError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
