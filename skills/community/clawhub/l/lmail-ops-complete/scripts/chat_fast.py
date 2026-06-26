#!/usr/bin/env python3
"""Single-command fast chat operations for LMail (send/check/send-check)."""

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
    load_json_file,
    request_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fast chat actions for LMail")
    parser.add_argument("--base-url", default=os.getenv("LMAIL_BASE_URL", "http://localhost:3001"))
    parser.add_argument("--token")
    parser.add_argument("--api-key")
    parser.add_argument("--credentials-file", default=os.getenv("LMAIL_CREDENTIALS_FILE", ".lmail-credentials.json"))
    parser.add_argument("--state-file", default=os.getenv("LMAIL_INBOX_STATE_FILE", ".lmail-inbox-state.json"))
    parser.add_argument("--action", choices=["send", "check", "send-check"], required=True)
    parser.add_argument("--to")
    parser.add_argument("--subject")
    parser.add_argument("--text")
    parser.add_argument("--content-type", default="notification")
    parser.add_argument("--priority", default="normal")
    parser.add_argument("--limit", type=int, default=1)
    parser.add_argument("--unread", action="store_true")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--output", choices=["brief", "json"], default="brief")
    return parser.parse_args()


def require_send_args(args: argparse.Namespace) -> None:
    missing = [k for k, v in {"--to": args.to, "--subject": args.subject, "--text": args.text}.items() if not v]
    if missing:
        raise LMailHttpError(f"Missing required send args: {', '.join(missing)}")


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


def send_message(
    *,
    base_url: str,
    headers: dict[str, str],
    to: str,
    subject: str,
    text: str,
    content_type: str,
    priority: str,
    timeout: int,
) -> dict[str, object]:
    payload = {
        "to": to,
        "subject": subject,
        "body": {"text": text},
        "contentType": content_type,
        "priority": priority,
    }
    status, resp = request_json(
        url=f"{base_url}/api/v1/messages/send",
        method="POST",
        headers=headers,
        payload=payload,
        timeout=timeout,
    )
    if status >= 400:
        raise LMailHttpError(f"send failed with HTTP {status}: {resp}")
    data = expect_success(resp, "chat_fast/send")
    return {
        "to": to,
        "subject": subject,
        "messageId": data.get("id") or data.get("messageId"),
        "threadId": data.get("threadId"),
    }


def check_latest(
    *,
    base_url: str,
    headers: dict[str, str],
    limit: int,
    unread: bool,
    timeout: int,
    state_file: str,
) -> dict[str, object]:
    query = urlencode(
        {
            "unread": str(bool(unread)).lower(),
            "limit": max(1, limit),
            "sort": "desc",
        }
    )
    status, resp = request_json(
        url=f"{base_url}/api/v1/messages/inbox?{query}",
        method="GET",
        headers=headers,
        timeout=timeout,
    )
    if status >= 400:
        raise LMailHttpError(f"inbox failed with HTTP {status}: {resp}")
    data = expect_success(resp, "chat_fast/check")
    messages = data if isinstance(data, list) else []
    prev_state = load_state(state_file)
    previous_message_id = str(prev_state.get("lastMessageId") or "")

    if not messages:
        return {
            "count": 0,
            "status": "EMPTY",
            "newReply": False,
            "latest": None,
            "previousMessageId": previous_message_id or None,
        }

    msg = messages[0]
    body = msg.get("body") if isinstance(msg.get("body"), dict) else {}
    latest_id = str(msg.get("id") or "")
    is_new_reply = bool(latest_id and latest_id != previous_message_id)

    save_state(
        state_file,
        {
            "lastMessageId": latest_id or None,
            "lastSeenAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        },
    )

    return {
        "count": len(messages),
        "status": "NEW_REPLY_RECEIVED" if is_new_reply else "NO_NEW_REPLY",
        "newReply": is_new_reply,
        "previousMessageId": previous_message_id or None,
        "latest": {
            "id": latest_id or None,
            "from": msg.get("fromAddress") or msg.get("from"),
            "subject": msg.get("subject"),
            "body": body.get("text"),
            "threadId": msg.get("threadId"),
            "createdAt": msg.get("createdAt"),
        },
    }


def print_brief(result: dict[str, object]) -> None:
    def pretty_value(value: object) -> str:
        if value is None:
            return "-"
        if isinstance(value, bool):
            return "yes" if value else "no"
        text = str(value).strip()
        return text if text else "-"

    lines: list[str] = []
    lines.append("DONE")
    lines.append(f"ACTION: {pretty_value(result.get('action'))}")

    sent = result.get("sent")
    if isinstance(sent, dict):
        lines.append("SENT: OK")
        lines.append(f"- to: {pretty_value(sent.get('to'))}")
        lines.append(f"- subject: {pretty_value(sent.get('subject'))}")
        lines.append(f"- messageId: {pretty_value(sent.get('messageId'))}")
        lines.append(f"- threadId: {pretty_value(sent.get('threadId'))}")

    inbox = result.get("inbox")
    if isinstance(inbox, dict):
        lines.append(f"INBOX: {pretty_value(inbox.get('status'))}")
        lines.append(f"- newReply: {pretty_value(inbox.get('newReply'))}")
        lines.append(f"- count: {pretty_value(inbox.get('count'))}")
        latest = inbox.get("latest")
        if latest is None:
            lines.append("- latest: none")
        elif isinstance(latest, dict):
            lines.append("LATEST_INBOX:")
            lines.append(f"- from: {pretty_value(latest.get('from'))}")
            lines.append(f"- subject: {pretty_value(latest.get('subject'))}")
            lines.append(f"- body: {pretty_value(latest.get('body'))}")
            lines.append(f"- time: {pretty_value(latest.get('createdAt'))}")
            lines.append(f"- messageId: {pretty_value(latest.get('id'))}")
            lines.append(f"- threadId: {pretty_value(latest.get('threadId'))}")
    print("\n".join(lines))


def main() -> int:
    args = parse_args()
    base_url = args.base_url.rstrip("/")
    creds = load_json_file(args.credentials_file)
    token = args.token or creds.get("token")
    api_key = args.api_key or creds.get("apiKey")
    headers = auth_headers(token=token, api_key=api_key)

    result: dict[str, object] = {"ok": True, "action": args.action}

    if args.action in {"send", "send-check"}:
        require_send_args(args)
        result["sent"] = send_message(
            base_url=base_url,
            headers=headers,
            to=str(args.to),
            subject=str(args.subject),
            text=str(args.text),
            content_type=args.content_type,
            priority=args.priority,
            timeout=args.timeout,
        )

    if args.action in {"check", "send-check"}:
        result["inbox"] = check_latest(
            base_url=base_url,
            headers=headers,
            limit=args.limit,
            unread=args.unread,
            timeout=args.timeout,
            state_file=args.state_file,
        )

    if args.output == "json":
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        print_brief(result)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (LMailHttpError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=True), file=sys.stderr)
        raise SystemExit(1)
