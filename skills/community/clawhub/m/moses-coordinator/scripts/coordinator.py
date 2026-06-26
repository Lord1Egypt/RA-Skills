#!/usr/bin/env python3
"""
MO§ES™ Coordinator Daemon — WebSocket session monitor
Detects sequence violations and logs them to the governance audit trail.

Monitors OpenClaw Gateway WebSocket for session events.
Checks Primary → Secondary → Observer sequence on each event.
Violations → logged to audit trail + printed to operator.

Usage:
  python3 coordinator.py          — run in foreground
  python3 coordinator.py &        — run in background

Requires: pip3 install websockets
Patent pending: Serial No. 63/877,177
"""

import asyncio
import json
import os
import subprocess
import sys

GATEWAY_WS = "ws://127.0.0.1:18789"
AUDIT_SCRIPT = os.path.expanduser(
    "~/.openclaw/workspace/skills/moses-governance/scripts/audit_stub.py"
)
STATE_PATH = os.path.expanduser("~/.openclaw/governance/state.json")

SEQUENCE = ["primary", "secondary", "observer"]


def log_violation(detail: str):
    """Log a sequence violation to the governance audit trail."""
    print(f"[COORDINATOR] VIOLATION — {detail}")
    try:
        subprocess.run([
            "python3", AUDIT_SCRIPT, "log",
            "coordinator", "sequence_violation", "FAIL",
            "COORDINATOR", "DEFENSE", "Observer"
        ], check=False)
    except Exception as e:
        print(f"[COORDINATOR] Audit log failed: {e}")


async def monitor():
    try:
        import websockets
    except ImportError:
        print("[COORDINATOR] Missing dependency: pip3 install websockets")
        sys.exit(1)

    session_state = {}  # session_id → last_agent_index

    print(f"[COORDINATOR] MO§ES™ Coordinator starting")
    print(f"[COORDINATOR] Connecting to {GATEWAY_WS}")

    try:
        async with websockets.connect(GATEWAY_WS) as ws:
            await ws.send(json.dumps({"type": "subscribe", "events": ["session_update"]}))
            print("[COORDINATOR] Subscribed to session events. Monitoring sequence compliance...")

            async for message in ws:
                try:
                    event = json.loads(message)
                except json.JSONDecodeError:
                    continue

                if event.get("type") != "session_update":
                    continue

                session_id = event.get("session_id")
                agent = event.get("agent", "").lower().strip()

                if agent not in SEQUENCE:
                    continue

                current_index = SEQUENCE.index(agent)
                last_index = session_state.get(session_id, -1)

                # Primary can always initiate (reset/start)
                if current_index == 0:
                    session_state[session_id] = 0
                    continue

                expected_index = last_index + 1
                if current_index != expected_index:
                    expected = SEQUENCE[expected_index] if expected_index < len(SEQUENCE) else "primary"
                    detail = (
                        f"session={session_id} agent={agent} responded out of sequence. "
                        f"Expected {expected} (index {expected_index}), got {agent} (index {current_index})"
                    )
                    log_violation(detail)
                else:
                    session_state[session_id] = current_index
                    # Full cycle complete — reset
                    if current_index == len(SEQUENCE) - 1:
                        session_state[session_id] = -1

    except ConnectionRefusedError:
        print(f"[COORDINATOR] Cannot connect to {GATEWAY_WS}")
        print("[COORDINATOR] Is OpenClaw Gateway running?")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[COORDINATOR] Shutting down.")


if __name__ == "__main__":
    asyncio.run(monitor())
