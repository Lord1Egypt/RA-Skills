#!/usr/bin/env python3
"""
witness.py — MO§ES™ External Witness Logger
Posts key governance events to Moltbook as a public, external audit record.

Answers mia_cat's critique: "who audits the auditor?"
The agent writing to the ledger decides what gets written. The HMAC attestation
helps receivers verify state, but an agent can simply not log something.

External witness solves this: key governance events (loop start, BLOCKED, FAIL,
DECLINE) post to Moltbook as public timestamped records. The public feed is the
second ledger — one the agent cannot unilaterally edit after the fact.

Usage:
  python3 witness.py post <event_type> <detail>
  python3 witness.py post-loop-start "<task>"
  python3 witness.py post-blocked "<action>" "<reason>"
  python3 witness.py post-fail "<action>" "<detail>"

Environment:
  MOLTBOOK_API_KEY       — Moltbook API key (or read from ~/.hange/moltbook_api_key)
  MOLTBOOK_SUBMOLT       — submolt to post to (default: "general")
  MOSES_WITNESS_ENABLED  — set to "1" to enable (off by default, opt-in)
  REFEREE_ENABLED — set to "1" to forward adversarial review results to external reviewer
  REFEREE_URL     — endpoint URL for external blind reviewer (any provider)
  REFEREE_KEY     — API key for external blind reviewer
"""

import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

MOLTBOOK_API = "https://www.moltbook.com/api/v1"
KEY_PATH = os.path.expanduser("~/.hange/moltbook_api_key")
STATE_PATH = os.path.expanduser("~/.openclaw/governance/state.json")


def get_api_key():
    key = os.environ.get("MOLTBOOK_API_KEY")
    if key:
        return key.strip()
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH) as f:
            return f.read().strip()
    return None


def load_state():
    if not os.path.exists(STATE_PATH):
        return {}
    with open(STATE_PATH) as f:
        return json.load(f)


def event_hash(event_type, detail, timestamp):
    return hashlib.sha256(f"{event_type}|{detail}|{timestamp}".encode()).hexdigest()[:16]


def post_to_moltbook(api_key, title, content):
    submolt = os.environ.get("MOLTBOOK_SUBMOLT", "general")
    payload = json.dumps({
        "title": title,
        "content": content,
        "submolt": submolt,
    }).encode()
    req = urllib.request.Request(
        f"{MOLTBOOK_API}/posts",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.read().decode()}"}
    except Exception as e:
        return {"error": str(e)}


def solve_verification(api_key, code, challenge):
    """Auto-solve Moltbook math verification challenge."""
    numbers = re.findall(r'\d+(?:\.\d+)?', challenge)
    if len(numbers) >= 2:
        try:
            answer = str(float(numbers[0]) + float(numbers[1]))
            payload = json.dumps({"verification_code": code, "answer": answer}).encode()
            req = urllib.request.Request(
                f"{MOLTBOOK_API}/verify",
                data=payload,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read()).get("success", False)
        except Exception:
            return False
    return False


def witness_event(event_type, detail, extra=None):
    """Post a governance event to Moltbook as external witness record."""
    if os.environ.get("MOSES_WITNESS_ENABLED", "0") != "1":
        return {"skipped": True, "reason": "MOSES_WITNESS_ENABLED not set to 1"}

    api_key = get_api_key()
    if not api_key:
        return {"skipped": True, "reason": "No Moltbook API key found"}

    state = load_state()
    timestamp = datetime.now(timezone.utc).isoformat()
    ehash = event_hash(event_type, detail, timestamp)
    state_str = (
        f"mode={state.get('mode','?')} "
        f"posture={state.get('posture','?')} "
        f"role={state.get('role','?')}"
    )

    icons = {"loop-start": "▶", "blocked": "⊘", "fail": "✗",
             "decline": "⊘", "recovery": "⚠", "complete": "✓"}
    icon = icons.get(event_type, "•")

    title = f"[MO§ES™ WITNESS] {event_type.upper()} — {ehash}"
    content = (
        f"{icon} **Governance event: {event_type.upper()}**\n\n"
        f"**Detail:** {detail}\n"
        f"**State:** {state_str}\n"
        f"**Timestamp:** {timestamp}\n"
        f"**Event hash:** `{ehash}`\n"
    )
    if extra:
        for k, v in extra.items():
            content += f"**{k}:** {v}\n"
    content += (
        "\n*External witness record. Cannot be retroactively edited to "
        "reflect what was not logged. — MO§ES™ governance harness | mos2es.io*"
    )

    result = post_to_moltbook(api_key, title, content)

    # Auto-solve verification so the post goes live immediately
    verification = result.get("post", {}).get("verification", {})
    if verification.get("verification_code"):
        solved = solve_verification(
            api_key,
            verification["verification_code"],
            verification.get("challenge_text", ""),
        )
        result["verification_solved"] = solved

    return result


def cmd_post(args):
    if len(args) < 2:
        print("Usage: witness.py post <event_type> <detail>")
        sys.exit(1)
    result = witness_event(args[0], " ".join(args[1:]))
    print(json.dumps(result, indent=2))


def cmd_post_loop_start(args):
    task = " ".join(args) if args else "unspecified"
    result = witness_event("loop-start", f"Harness loop initiated: {task}")
    print(json.dumps(result, indent=2))


def cmd_post_blocked(args):
    action = args[0] if args else "unspecified"
    reason = " ".join(args[1:]) if len(args) > 1 else "posture gate"
    result = witness_event("blocked", f"Action blocked: {action}", {"reason": reason})
    print(json.dumps(result, indent=2))


def cmd_post_fail(args):
    action = args[0] if args else "unspecified"
    detail = " ".join(args[1:]) if len(args) > 1 else ""
    result = witness_event("fail", f"Step failed: {action}", {"detail": detail})
    print(json.dumps(result, indent=2))


COMMANDS = {
    "post": cmd_post,
    "post-loop-start": cmd_post_loop_start,
    "post-blocked": cmd_post_blocked,
    "post-fail": cmd_post_fail,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd not in COMMANDS:
        print(f"Usage: witness.py [{'|'.join(COMMANDS)}] ...")
        print("Set MOSES_WITNESS_ENABLED=1 to activate external posting.")
        sys.exit(1)
    COMMANDS[cmd](sys.argv[2:])
