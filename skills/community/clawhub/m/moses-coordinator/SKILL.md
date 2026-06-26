---
name: moses-coordinator
description: "MO§ES™ Coordinator — Lightweight daemon that monitors OpenClaw Gateway WebSocket for session events, detects sequence violations (Primary → Secondary → Observer), and logs them. Optional component of the moses-governance bundle. Requires background process."
metadata:
  openclaw:
    emoji: 🔄
    tags: [coordinator, multi-agent, sequencing, daemon, websocket]
    version: 0.1.2
    bins:
      - python3
    stateDirs:
      - ~/.openclaw/audits/moses
example: |
  # Run coordinator daemon in background
  python3 scripts/coordinator.py &
  # Or via launchd/systemd for persistent operation
---

# MO§ES™ Coordinator

The coordinator is the external sequence enforcer. It monitors session events via the OpenClaw Gateway WebSocket and detects when agents respond out of order, modes are violated, or constitutional drift occurs.

This is optional. The skill family enforces governance via prompt directives. The coordinator adds a second enforcement layer via event monitoring.

---

## What It Does

1. Connects to OpenClaw Gateway WebSocket: `ws://127.0.0.1:18789`
2. Subscribes to session update events
3. On each session event, checks:
   - Was the responding agent in the correct sequence position?
   - Did the response comply with the active governance mode?
   - Was the audit log appended before the response?
4. Violations → logged to audit trail + operator notified

---

## Coordinator Script

Save as `scripts/coordinator.py` in the skill directory:

```python
#!/usr/bin/env python3
"""
MO§ES™ Coordinator Daemon — WebSocket session monitor
Detects sequence violations and logs them to audit trail
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

async def monitor():
    try:
        import websockets
    except ImportError:
        print("[COORDINATOR] Install websockets: pip3 install websockets")
        sys.exit(1)

    session_state = {}  # session_id → last_agent_index

    print(f"[COORDINATOR] Connecting to {GATEWAY_WS}")

    async with websockets.connect(GATEWAY_WS) as ws:
        await ws.send(json.dumps({"type": "subscribe", "events": ["session_update"]}))
        print("[COORDINATOR] Subscribed to session events. Monitoring...")

        async for message in ws:
            event = json.loads(message)
            if event.get("type") != "session_update":
                continue

            session_id = event.get("session_id")
            agent = event.get("agent", "").lower()

            if agent not in SEQUENCE:
                continue

            current_index = SEQUENCE.index(agent)
            last_index = session_state.get(session_id, -1)

            if current_index != last_index + 1 and current_index != 0:
                # Sequence violation
                expected = SEQUENCE[last_index + 1] if last_index + 1 < len(SEQUENCE) else "primary"
                detail = f"Sequence violation in session {session_id}: {agent} responded but expected {expected}"
                print(f"[COORDINATOR] VIOLATION — {detail}")

                subprocess.run([
                    "python3", AUDIT_SCRIPT, "log",
                    "--agent", "coordinator",
                    "--action", "sequence_violation",
                    "--detail", detail,
                    "--outcome", "blocked_and_logged"
                ])
            else:
                session_state[session_id] = current_index
                if current_index == len(SEQUENCE) - 1:
                    # Full cycle complete, reset
                    session_state[session_id] = -1

if __name__ == "__main__":
    asyncio.run(monitor())
```

---

## Running the Coordinator

**Manual (dev):**
```bash
python3 ~/.openclaw/workspace/skills/moses-coordinator/scripts/coordinator.py &
```

**Persistent (macOS launchd):**
Create `~/Library/LaunchAgents/com.elloCello.moses-coordinator.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.elloCello.moses-coordinator</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>/Users/YOUR_USER/.openclaw/workspace/skills/moses-coordinator/scripts/coordinator.py</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
</dict>
</plist>
```
Then: `launchctl load ~/Library/LaunchAgents/com.elloCello.moses-coordinator.plist`

---

## Dependencies

```bash
pip3 install websockets
```

---

## External Script — audit_stub.py

On sequence violations, the coordinator calls `audit_stub.py` via subprocess to log the event. This script is part of the `moses-governance` skill bundle and ships in this repo at:

```
~/.openclaw/workspace/skills/moses-governance/scripts/audit_stub.py
```

It writes to the local ledger at `~/.openclaw/audits/moses/audit_ledger.jsonl`. No network calls. No credentials required. Source is included and reviewable.

`MOSES_OPERATOR_SECRET` is **not used** by this skill. Do not provide it — the coordinator does not need it.
