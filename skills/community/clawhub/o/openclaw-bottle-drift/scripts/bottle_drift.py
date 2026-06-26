#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bottle Drift client CLI.
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict

MAX_MESSAGE_LEN = 240
MAX_NAME_LEN = 40


def json_print(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=raw,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {"ok": False, "error": body}
        data.setdefault("status", exc.code)
        return data
    except urllib.error.URLError as exc:
        return {"ok": False, "error": f"network error: {exc}"}


def get_json(url: str) -> Dict[str, Any]:
    request = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {"ok": False, "error": body}
        data.setdefault("status", exc.code)
        return data
    except urllib.error.URLError as exc:
        return {"ok": False, "error": f"network error: {exc}"}


def validate_name(name: str, field_name: str) -> None:
    value = name.strip()
    if not value:
        raise ValueError(f"{field_name} is required")
    if len(value) > MAX_NAME_LEN:
        raise ValueError(f"{field_name} must be <= {MAX_NAME_LEN} chars")


def command_heartbeat(args: argparse.Namespace) -> int:
    validate_name(args.name, "name")
    payload = {
        "user_id": args.user_id,
        "display_name": args.name,
        "callback_url": args.callback_url or None,
        "accept_bottles": not args.pause_receiving,
    }
    json_print(post_json(args.relay.rstrip("/") + "/api/presence/heartbeat", payload))
    return 0


def command_send(args: argparse.Namespace) -> int:
    validate_name(args.name, "name")
    message = args.message.strip()
    if not message:
        raise ValueError("message is required")
    if len(message) > MAX_MESSAGE_LEN:
        raise ValueError(f"message must be <= {MAX_MESSAGE_LEN} chars")
    payload = {
        "sender_id": args.user_id,
        "sender_name": args.name,
        "message": message,
        "fanout": args.fanout,
        "ttl_seconds": args.ttl_seconds,
    }
    json_print(post_json(args.relay.rstrip("/") + "/api/bottles/send", payload))
    return 0


def command_reply(args: argparse.Namespace) -> int:
    validate_name(args.name, "name")
    reply_text = args.reply.strip()
    if not reply_text:
        raise ValueError("reply is required")
    if len(reply_text) > MAX_MESSAGE_LEN:
        raise ValueError(f"reply must be <= {MAX_MESSAGE_LEN} chars")
    payload = {
        "token": args.token,
        "replier_name": args.name,
        "reply_text": reply_text,
    }
    json_print(post_json(args.relay.rstrip("/") + "/api/bottles/reply", payload))
    return 0


def command_inbox(args: argparse.Namespace) -> int:
    user_id = urllib.parse.quote(args.user_id, safe="")
    json_print(get_json(args.relay.rstrip("/") + f"/api/inbox/{user_id}"))
    return 0


def command_online(args: argparse.Namespace) -> int:
    url = args.relay.rstrip("/") + "/api/users/online"
    if args.exclude:
        url += "?exclude=" + urllib.parse.quote(args.exclude, safe="")
    json_print(get_json(url))
    return 0


def command_dashboard(args: argparse.Namespace) -> int:
    json_print({
        "ok": True,
        "dashboard_url": args.relay.rstrip("/") + "/",
        "reply_page_example": args.relay.rstrip("/") + "/r/<reply_token>",
    })
    return 0


def command_presence_loop(args: argparse.Namespace) -> int:
    validate_name(args.name, "name")
    payload = {
        "user_id": args.user_id,
        "display_name": args.name,
        "callback_url": args.callback_url or None,
        "accept_bottles": not args.pause_receiving,
    }
    url = args.relay.rstrip("/") + "/api/presence/heartbeat"
    try:
        while True:
            result = post_json(url, payload)
            json_print(result)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nstopped", file=sys.stderr)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Bottle Drift client CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--relay", required=True, help="relay base URL, e.g. http://127.0.0.1:8765")
    common.add_argument("--user-id", required=True, help="stable user identifier")

    hb = sub.add_parser("heartbeat", parents=[common], help="send a presence heartbeat")
    hb.add_argument("--name", required=True, help="display name")
    hb.add_argument("--callback-url", default="", help="optional callback URL")
    hb.add_argument("--pause-receiving", action="store_true", help="announce online but temporarily refuse bottles")
    hb.set_defaults(func=command_heartbeat)

    send = sub.add_parser("send", parents=[common], help="send a bottle")
    send.add_argument("--name", required=True, help="display name")
    send.add_argument("--message", required=True, help="gift message")
    send.add_argument("--fanout", type=int, default=1, help="number of recipients (max 3)")
    send.add_argument("--ttl-seconds", type=int, default=86400, help="message lifetime in seconds")
    send.set_defaults(func=command_send)

    inbox = sub.add_parser("inbox", parents=[common], help="show inbox/outbox/replies")
    inbox.set_defaults(func=command_inbox)

    online = sub.add_parser("online", help="show online subscribers")
    online.add_argument("--relay", required=True, help="relay base URL")
    online.add_argument("--exclude", default="", help="exclude one user_id")
    online.set_defaults(func=command_online)

    reply = sub.add_parser("reply", help="reply to a bottle")
    reply.add_argument("--relay", required=True, help="relay base URL")
    reply.add_argument("--token", required=True, help="reply token")
    reply.add_argument("--name", required=True, help="replier display name")
    reply.add_argument("--reply", required=True, help="reply text")
    reply.set_defaults(func=command_reply)

    dash = sub.add_parser("dashboard", help="show dashboard URL")
    dash.add_argument("--relay", required=True, help="relay base URL")
    dash.set_defaults(func=command_dashboard)

    loop = sub.add_parser("presence-loop", parents=[common], help="keep sending heartbeat")
    loop.add_argument("--name", required=True, help="display name")
    loop.add_argument("--callback-url", default="", help="optional callback URL")
    loop.add_argument("--pause-receiving", action="store_true", help="announce online but refuse bottles")
    loop.add_argument("--interval", type=int, default=30, help="heartbeat interval in seconds")
    loop.set_defaults(func=command_presence_loop)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except ValueError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
