#!/usr/bin/env python3
"""Fail-closed write authorization guard for Hemlane CLI scripts."""
from __future__ import annotations
import json, os, sys

AUTHORIZED_DISCORD_SENDER_SHA256 = "d40800cb299a0988be92536d6ac5a7e99659ec6d9fef7b7779a8fdeb980f8da1"

def requester_discord_id() -> str | None:
    for key in ("OPENCLAW_DISCORD_SENDER_ID", "OPENCLAW_SENDER_ID", "DISCORD_SENDER_ID", "OPENCLAW_AUTHOR_ID", "OPENCLAW_USER_ID"):
        val = os.environ.get(key)
        if val:
            return str(val)
    for key in ("OPENCLAW_INBOUND_META", "OPENCLAW_MESSAGE_META", "OPENCLAW_REQUEST_META", "OPENCLAW_CONTEXT_JSON"):
        raw = os.environ.get(key)
        if not raw:
            continue
        try:
            meta = json.loads(raw)
        except Exception:
            continue
        for field in ("sender_id", "author_id", "user_id", "member_id", "senderId", "authorId", "userId"):
            val = meta.get(field)
            if val:
                return str(val)
    return None

def require_earl_write(action: str) -> None:
    caller = requester_discord_id()
    if caller and __import__("hashlib").sha256(caller.encode()).hexdigest() == AUTHORIZED_DISCORD_SENDER_SHA256:
        return
    print(json.dumps({
        "error": "write_blocked",
        "action": action,
        "message": "Hemlane write action requires a verified privileged caller. No trusted matching caller metadata was present, so the script failed closed.",
    }, indent=2), file=sys.stderr)
    raise SystemExit(77)
