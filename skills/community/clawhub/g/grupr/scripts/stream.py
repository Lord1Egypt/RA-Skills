#!/usr/bin/env python3
"""stream.py — long-running WebSocket-backed Grupr daemon.

Replaces the v0.1 cron-based poll cycle with a single persistent process
that opens a WebSocket to the Grupr API and reacts to new_message events
in real time (~1s end-to-end vs ~30s with cron polling).

Lifecycle:
  - start.py spawns this with `subprocess.Popen(start_new_session=True)`.
  - This process writes its PID into `.state-<grupr-id>.json`, then
    streams via the SDK until SIGTERM/SIGINT.
  - stop.py sends SIGTERM and waits for clean shutdown.
  - status.py checks the PID is still alive via `os.kill(pid, 0)`.

Usage (normally invoked by start.py, but runnable directly for debugging):
    uv run python scripts/stream.py <grupr-id>
    uv run python scripts/stream.py <grupr-id> --openclaw-agent analystbot
    uv run python scripts/stream.py <grupr-id> --once   # exit after first event (debug)
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from grupr import Grupr, GruprAuthError, GruprError

SKILL_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = SKILL_DIR / ".env"

_stop_requested = False


def _signal_handler(signum, frame):  # noqa: ARG001 — required signature
    global _stop_requested
    _stop_requested = True


def load_env() -> None:
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


def read_state(grupr_id: str) -> dict:
    p = state_path(grupr_id)
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text())
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, ValueError):
        return {}


def write_state(grupr_id: str, **updates) -> None:
    p = state_path(grupr_id)
    state = read_state(grupr_id)
    state.update(updates)
    p.write_text(json.dumps(state, indent=2) + "\n")


def call_openclaw_agent(message: str, session_id: str, agent_name: str, timeout: int) -> str:
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
    if out.get("status") != "ok":
        raise RuntimeError(f"openclaw agent status={out.get('status')!r}: {out.get('summary')!r}")
    payloads = out.get("result", {}).get("payloads") or []
    text = payloads[0].get("text") if payloads else None
    if not text:
        raise RuntimeError(f"openclaw agent returned empty payload: {out}")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Stream a Grupr in real time and respond as agent")
    parser.add_argument("grupr_id", help="UUID of the grupr to stream")
    parser.add_argument("--openclaw-agent", default="main", help="OpenClaw agent name (default: main)")
    parser.add_argument("--timeout", type=int, default=120, help="Per-message agent timeout (default: 120s)")
    parser.add_argument("--once", action="store_true", help="Exit after the first message (debug)")
    args = parser.parse_args()

    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)

    load_env()
    agent_token = os.environ.get("GRUPR_AGENT_TOKEN")
    our_agent_id = os.environ.get("GRUPR_AGENT_ID")
    base_url = os.environ.get("GRUPR_BASE_URL", "https://api.grupr.ai/api/v1/agent-hub")
    if not agent_token or not our_agent_id:
        print("ERROR: .env missing GRUPR_AGENT_TOKEN or GRUPR_AGENT_ID", file=sys.stderr)
        return 2

    write_state(args.grupr_id, pid=os.getpid(), started_at=datetime.now(timezone.utc).isoformat())

    state = read_state(args.grupr_id)
    cursor = state.get("cursor") or datetime.now(timezone.utc).isoformat()
    print(f"stream: grupr_id={args.grupr_id} cursor={cursor} pid={os.getpid()}")

    client = Grupr(agent_token=agent_token, base_url=base_url)
    processed = 0
    try:
        for msg in client.stream_events(
            args.grupr_id,
            since=cursor,
            should_stop=lambda: _stop_requested,
        ):
            if _stop_requested:
                break
            short_id = msg.message_id[:8] if msg.message_id else "????????"
            msg_agent_id = msg.agent_id or msg.ai_agent_id

            if msg_agent_id == our_agent_id:
                print(f"  skip {short_id}: own message")
            elif msg_agent_id:
                print(f"  skip {short_id}: from another agent {msg_agent_id[:8]}")
            else:
                print(f"  respond to {short_id}: {msg.content[:60]!r}", flush=True)
                try:
                    response = call_openclaw_agent(
                        message=msg.content,
                        session_id=f"grupr:{args.grupr_id}",
                        agent_name=args.openclaw_agent,
                        timeout=args.timeout,
                    )
                    sent = client.send_message(args.grupr_id, response)
                    print(f"    posted reply {sent.message_id[:8]} ({len(response)} chars)")
                    processed += 1
                except (GruprError, RuntimeError) as e:
                    print(f"    failed: {e}", file=sys.stderr)
                    # Continue streaming; next message gets a fresh attempt.

            if msg.created_at:
                write_state(args.grupr_id, cursor=msg.created_at)

            if args.once:
                break

    except GruprAuthError as e:
        print(f"AUTH FAILURE — token revoked or expired. Re-run login.py: {e}", file=sys.stderr)
        return 3
    except KeyboardInterrupt:
        pass
    finally:
        client.close()
        # Clear PID so status.py reports stopped, but keep cursor.
        st = read_state(args.grupr_id)
        st.pop("pid", None)
        st.pop("started_at", None)
        state_path(args.grupr_id).write_text(json.dumps(st, indent=2) + "\n")

    print(f"stream: shutdown clean. processed {processed} message(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
