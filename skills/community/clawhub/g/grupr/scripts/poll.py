#!/usr/bin/env python3
"""poll.py — single-grupr poll cycle. Designed to be invoked by cron.

Reads .env, polls one grupr for new messages, generates responses via
`openclaw agent`, posts back via the Grupr SDK. Advances a per-grupr
cursor on success so the next invocation only sees newer messages.

Skips:
  - messages from our own agent (we authored)
  - messages from any other AI agent (avoids agent⇄agent infinite loops)
  - messages older than the cursor (already processed)

Usage:
    uv run python scripts/poll.py <grupr-id>
    uv run python scripts/poll.py <grupr-id> --dry-run
    uv run python scripts/poll.py <grupr-id> --max-messages 5
    uv run python scripts/poll.py <grupr-id> --openclaw-agent analystbot
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from grupr import Grupr, GruprError

SKILL_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = SKILL_DIR / ".env"


def load_env() -> None:
    """Read KEY=VAL lines from .env into os.environ. No-op if already set."""
    if not ENV_PATH.exists():
        print(f"ERROR: {ENV_PATH} not found. Run scripts/login.py first.", file=sys.stderr)
        sys.exit(2)
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k, v)


def state_path(grupr_id: str) -> Path:
    return SKILL_DIR / f".state-{grupr_id}.json"


def read_cursor(grupr_id: str) -> str | None:
    p = state_path(grupr_id)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text()).get("cursor")
    except (json.JSONDecodeError, ValueError):
        return None


def write_cursor(grupr_id: str, cursor: str) -> None:
    """Update cursor while preserving other fields (e.g. cron_job_id, name)."""
    p = state_path(grupr_id)
    state: dict = {}
    if p.exists():
        try:
            state = json.loads(p.read_text())
            if not isinstance(state, dict):
                state = {}
        except (json.JSONDecodeError, ValueError):
            state = {}
    state["cursor"] = cursor
    p.write_text(json.dumps(state, indent=2) + "\n")


def call_openclaw_agent(
    message: str,
    session_id: str,
    agent_name: str,
    timeout: int,
) -> str:
    """Subprocess `openclaw agent --json`, return the response text payload.

    Raises RuntimeError on failure with a helpful message.
    """
    cmd = [
        "openclaw", "agent",
        "--message", message,
        "--agent", agent_name,
        "--session-id", session_id,
        "--json",
        "--timeout", str(timeout),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
    if proc.returncode != 0:
        raise RuntimeError(
            f"openclaw agent exit {proc.returncode}: {proc.stderr[:500] or proc.stdout[:500]}"
        )
    try:
        out = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"openclaw agent: bad JSON ({e}); first 300 chars: {proc.stdout[:300]}")
    status = out.get("status")
    if status != "ok":
        raise RuntimeError(f"openclaw agent status={status!r}: {out.get('summary')!r}")
    payloads = out.get("result", {}).get("payloads") or []
    text = payloads[0].get("text") if payloads else None
    if not text:
        raise RuntimeError(f"openclaw agent returned empty payload: {out}")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Poll a Grupr and respond as agent")
    parser.add_argument("grupr_id", help="UUID of the grupr to poll")
    parser.add_argument(
        "--openclaw-agent",
        default="main",
        help="OpenClaw agent name to invoke (default: main)",
    )
    parser.add_argument(
        "--max-messages",
        type=int,
        default=10,
        help="Cap on messages to fetch per cycle (default: 10)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Per-message agent timeout in seconds (default: 120)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be done; don't call agent or send replies",
    )
    args = parser.parse_args()

    load_env()
    agent_token = os.environ.get("GRUPR_AGENT_TOKEN")
    our_agent_id = os.environ.get("GRUPR_AGENT_ID")
    base_url = os.environ.get("GRUPR_BASE_URL", "https://api.grupr.ai/api/v1/agent-hub")
    if not agent_token or not our_agent_id:
        print("ERROR: .env missing GRUPR_AGENT_TOKEN or GRUPR_AGENT_ID", file=sys.stderr)
        return 2

    cursor = read_cursor(args.grupr_id) or datetime.now(timezone.utc).isoformat()
    client = Grupr(agent_token=agent_token, base_url=base_url)
    try:
        try:
            result = client.poll_messages(args.grupr_id, after=cursor, limit=args.max_messages)
        except GruprError as e:
            print(f"poll_messages failed: code={e.code} status={e.status}: {e}", file=sys.stderr)
            return 3

        print(f"Polled {len(result.messages)} message(s) after {cursor}")

        processed = 0
        last_cursor = cursor
        for msg in result.messages:
            msg_agent_id = msg.agent_id or msg.ai_agent_id
            short_id = msg.message_id[:8]

            if msg_agent_id == our_agent_id:
                print(f"  skip {short_id}: own message")
                last_cursor = msg.created_at
                continue
            if msg_agent_id:
                print(f"  skip {short_id}: from another agent {msg_agent_id[:8]}")
                last_cursor = msg.created_at
                continue

            print(f"  respond to {short_id}: {msg.content[:60]!r}")
            if args.dry_run:
                print(f"    (dry-run) would call openclaw agent")
                last_cursor = msg.created_at
                continue

            try:
                response = call_openclaw_agent(
                    message=msg.content,
                    session_id=f"grupr:{args.grupr_id}",
                    agent_name=args.openclaw_agent,
                    timeout=args.timeout,
                )
            except Exception as e:
                print(f"    agent call failed: {e}", file=sys.stderr)
                # Stop processing — leave cursor at last_cursor so we retry next poll.
                break

            try:
                sent = client.send_message(args.grupr_id, response)
                print(f"    posted reply {sent.message_id[:8]} ({len(response)} chars)")
            except GruprError as e:
                print(f"    send_message failed: code={e.code} status={e.status}: {e}", file=sys.stderr)
                break

            last_cursor = msg.created_at
            processed += 1

    finally:
        client.close()

    if last_cursor != cursor:
        write_cursor(args.grupr_id, last_cursor)
    print(f"Cursor: {last_cursor}; processed {processed} message(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
