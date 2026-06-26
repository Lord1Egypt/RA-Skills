# Minecraft Bridge Dependency Guide

This is the canonical dependency reference for any other skill that wants to use live Minecraft data or live bot actions.

## Core Rule

OpenClaw does not provide native skill dependency management. A dependent skill must check bridge availability itself before assuming the bridge is usable.

### Three states to handle

```text
A. Bridge not running
   curl -> ECONNREFUSED
   Action: tell the user to start the bridge

B. Bridge running, bot offline
   GET /status -> {"connected": false}
   Action: tell the user to open Minecraft / verify host+port

C. Bridge running, bot connected
   GET /status -> {"connected": true, ...}
   Action: proceed
```

---

## Standard Health Check (Shell)

```bash
BRIDGE_PORT="${MC_BRIDGE_PORT:-3001}"
BRIDGE_URL="http://localhost:${BRIDGE_PORT}"

check_bridge() {
  if ! curl -sf "${BRIDGE_URL}/status" > /tmp/mc_status.json 2>/dev/null; then
    echo "ERROR:NOT_RUNNING"
    return 1
  fi

  local connected
  connected=$(python3 -c "import json; print(json.load(open('/tmp/mc_status.json')).get('connected', False))" 2>/dev/null)

  if [ "$connected" != "True" ] && [ "$connected" != "true" ]; then
    echo "ERROR:BOT_OFFLINE"
    return 2
  fi

  echo "OK"
  return 0
}
```

Recommended handling:
- `NOT_RUNNING` → instruct the user to start `bridge-server.js`
- `BOT_OFFLINE` → instruct the user to open Minecraft and verify `MC_HOST` / `MC_PORT`
- `OK` → continue

---

## Standard Health Check (Node.js)

```javascript
const http = require('http');

async function checkBridge(port = parseInt(process.env.MC_BRIDGE_PORT) || 3001) {
  return new Promise((resolve) => {
    const req = http.get(`http://localhost:${port}/status`, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const status = JSON.parse(data);
          if (status.connected) resolve({ ok: true, status });
          else resolve({ ok: false, reason: 'BOT_OFFLINE', status });
        } catch {
          resolve({ ok: false, reason: 'INVALID_RESPONSE' });
        }
      });
    });
    req.on('error', (e) => {
      if (e.code === 'ECONNREFUSED') resolve({ ok: false, reason: 'NOT_RUNNING' });
      else resolve({ ok: false, reason: e.code });
    });
    req.setTimeout(2000, () => {
      req.destroy();
      resolve({ ok: false, reason: 'TIMEOUT' });
    });
  });
}
```

---

## Dependency Statement Pattern for Other Skills

In any dependent skill, use a short prerequisite section like:

```markdown
## Prerequisites

This skill needs `minecraft-bridge` for live game-state reads or live bot actions.
Before using live actions:
1. Start the bridge
2. Check `GET /status`
3. If offline, degrade gracefully or ask the user to open Minecraft
```

---

## Offline-First Design Principle

Not every Minecraft skill should require the bridge.

| Skill type | Bridge required? | Preferred behavior |
|---|---|---|
| Knowledge/wiki | No | Work fully offline |
| Planning | Optional | Plan offline, execute only when bridge is available |
| Live bot control | Yes | Require bridge |
| RCON admin | No bridge, separate protocol | Use RCON instead |

If a skill's main value is knowledge or planning, degrade gracefully instead of hard-failing when the bridge is unavailable.

---

## Concurrency Note

The bridge runs on a single Node.js event loop.
- GET requests are generally safe to perform concurrently
- POST action requests may queue or conflict
- Check `status.currentAction` before issuing a new long-running action if coordination matters
