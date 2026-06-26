---
name: oo
description: Use when user mentions a ConnectOnion agent address (0x...), asks to connect/delegate to a remote agent, or uses /oo command. Also triggers when user wants to set up ConnectOnion environment for agent networking.
argument-hint: <0xAddress> <task description>
---

# ConnectOnion Agent Networking

Connect to remote ConnectOnion agents, delegate tasks, and handle multi-turn collaboration.

## Environment Setup

Before any interaction, verify the environment is ready. Run these checks sequentially — stop on first failure:

**1. Check connectonion is installed:**
```bash
python -c "import connectonion; print(connectonion.__version__)"
```
If ImportError: run `pip install connectonion`, then re-check.

**2. Check agent identity exists:**
```bash
ls .co/keys/agent.key 2>/dev/null || ls ~/.co/keys/agent.key 2>/dev/null
```
If neither exists: run `co init` to generate identity.

**3. Verify identity is usable:**
```bash
python -c "
from connectonion import address
from pathlib import Path
a = address.load(Path('.co')) or address.load(Path.home() / '.co')
print(a['address'])
"
```
If fails: report the error and stop. The user needs to fix their `.co/` directory.

> **Note:** `import connectonion` prints `[env] ...` lines to stdout. For all environment checks, **parse only the last line** of stdout output. Ignore everything else.

Skip environment checks after the first successful run in a session.

## Connecting to a Remote Agent

### Parsing User Intent

Extract from the user's message:
- **Target address**: match regex `0x[0-9a-fA-F]{64}` (66 chars total)
- **Task description**: everything else

For `/oo` slash command: `/oo <address> <task description>`

### Connection Strategy: Direct-First with Relay Fallback

The default `connect()` library has a known issue: the relay API may not return an `online` field, causing direct endpoint resolution to always fail and falling back to relay — which itself may be unreliable. To work around this, the skill uses a **smart connection script** that:

1. Queries the relay API for the agent's registered endpoints
2. Tries each endpoint directly (verifying via `/info`)
3. Falls back to relay only if all direct endpoints fail

### One-shot Task

Generate and execute this Python script (fill in `{address}` and `{task}`):

```python
import sys, json, time, uuid, asyncio
import httpx, websockets
from connectonion import address
from pathlib import Path

TARGET = "{address}"
TASK = "{task}"
TIMEOUT = 60
RELAY_URL = "wss://oo.openonion.ai"

keys = address.load(Path(".co")) or address.load(Path.home() / ".co")

def _sort_endpoints(endpoints):
    def priority(url):
        if "localhost" in url or "127.0.0.1" in url:
            return 0
        if any(x in url for x in ("192.168.", "10.", "172.16.", "172.17.", "172.18.")):
            return 1
        return 2
    return sorted(endpoints, key=priority)

def discover_direct_ws(target, relay_url):
    """Query relay API for endpoints and find a working direct WebSocket."""
    https_relay = relay_url.replace("wss://", "https://").replace("ws://", "http://").rstrip("/")
    try:
        resp = httpx.get(f"{https_relay}/api/relay/agents/{target}", timeout=5)
        if resp.status_code != 200:
            return None
        info = resp.json()
    except Exception:
        return None

    endpoints = info.get("endpoints", [])
    if not endpoints:
        return None

    http_endpoints = [ep for ep in _sort_endpoints(endpoints)
                      if ep.startswith("http://") or ep.startswith("https://")]

    for http_url in http_endpoints:
        try:
            r = httpx.get(f"{http_url}/info", timeout=3, proxy=None)
            if r.status_code == 200 and r.json().get("address") == target:
                ws_url = http_url.replace("https://", "wss://").replace("http://", "ws://")
                if not ws_url.endswith("/ws"):
                    ws_url = ws_url.rstrip("/") + "/ws"
                return ws_url
        except Exception:
            continue
    return None

async def direct_connect(ws_url, target, keys, task, timeout):
    """Connect directly to agent WebSocket, send task, return result."""
    async with websockets.connect(ws_url, proxy=None) as ws:
        # Signed CONNECT
        ts = int(time.time())
        payload = {"to": target, "timestamp": ts}
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        signature = address.sign(keys, canonical.encode())
        connect_msg = {
            "type": "CONNECT", "timestamp": ts, "to": target,
            "payload": payload, "from": keys["address"], "signature": signature.hex()
        }
        await ws.send(json.dumps(connect_msg))

        # Wait for CONNECTED
        raw = await asyncio.wait_for(ws.recv(), timeout=10)
        event = json.loads(raw)
        if event.get("type") == "ERROR":
            raise ConnectionError(f"Auth error: {event.get('message', event.get('error'))}")
        if event.get("type") != "CONNECTED":
            raise ConnectionError(f"Unexpected: {event.get('type')}")

        # Signed INPUT
        ts2 = int(time.time())
        input_id = str(uuid.uuid4())
        input_payload = {"prompt": task, "timestamp": ts2}
        input_canonical = json.dumps(input_payload, sort_keys=True, separators=(",", ":"))
        input_sig = address.sign(keys, input_canonical.encode())
        input_msg = {
            "type": "INPUT", "input_id": input_id, "prompt": task, "timestamp": ts2,
            "payload": input_payload, "from": keys["address"], "signature": input_sig.hex()
        }
        await ws.send(json.dumps(input_msg))

        # Stream until OUTPUT
        while True:
            msg = await asyncio.wait_for(ws.recv(), timeout=timeout)
            ev = json.loads(msg)
            t = ev.get("type")
            if t == "OUTPUT":
                return ev.get("result", ""), True
            elif t == "ask_user":
                return ev.get("text", ""), False
            elif t == "ERROR":
                raise ConnectionError(f"Agent error: {ev.get('message', ev.get('error'))}")

# --- Main ---
result_text, done = None, None

# Step 1: Try direct connection
ws_url = discover_direct_ws(TARGET, RELAY_URL)
if ws_url:
    try:
        result_text, done = asyncio.run(direct_connect(ws_url, TARGET, keys, TASK, TIMEOUT))
        print(f"CO_METHOD: direct", flush=True)
    except Exception as e:
        print(f"CO_DIRECT_FAIL: {e}", flush=True)

# Step 2: Fallback to relay
if result_text is None:
    try:
        from connectonion import connect
        agent = connect(TARGET, keys=keys)
        response = agent.input(TASK, timeout=TIMEOUT)
        result_text, done = response.text, response.done
        print(f"CO_METHOD: relay", flush=True)
    except Exception as e:
        print(f"CO_RELAY_FAIL: {e}", flush=True)
        sys.exit(1)

print(f"CO_RESPONSE: {json.dumps(result_text)}", flush=True)
print(f"CO_DONE: {done}", flush=True)
```

Execute via your shell tool. Parse stdout — **only lines starting with `CO_` matter**, ignore all others. The `CO_RESPONSE` value is JSON-encoded (to handle multi-line responses). Decode it before presenting to the user.

- `CO_DONE: True` → return `CO_RESPONSE` content to the user. Done.
- `CO_DONE: False` → the remote agent is asking a follow-up question. See Multi-turn Task below.
- `CO_METHOD: direct` → connected directly (fastest path).
- `CO_METHOD: relay` → connected via relay fallback.
- `CO_DIRECT_FAIL: ...` → direct failed, trying relay next.
- `CO_RELAY_FAIL: ...` → both methods failed. Report error to user.

For long-running tasks, increase timeout to 300.

### Multi-turn Task

Multi-turn requires maintaining session state. Use separate one-shot calls per turn since stdin interaction is unreliable in agent environments. Each turn is a new connection but passes context through the conversation.

For the first turn, use the one-shot script above. For follow-up turns, include conversation context in the prompt (e.g., prepend prior exchanges).

## Response Handling

After each round, parse stdout — **only `CO_` prefixed lines matter**, ignore all others:

- `CO_DONE: True` → return `CO_RESPONSE` content to the user. Done.
- `CO_DONE: False` → the remote agent asked a follow-up question:
  - **If you can answer from context** (file contents, prior conversation, your own knowledge) → answer automatically. Do not bother the user.
  - **If you need the user's input** → show `CO_RESPONSE` to the user, wait for their reply, then send another round.
  - Loop until `CO_DONE: True` or 10 rounds.

## Error Handling

If the script fails, check stderr for these patterns:

| Error in stderr | Cause | Action |
|-----------------|-------|--------|
| `ImportError: No module named 'connectonion'` | Not installed | Run `pip install connectonion` |
| `address.load() returns None` | No identity | Run `co init` |
| `TimeoutError` | Remote agent unreachable or slow | Verify address, check network/proxy, increase timeout |
| `ConnectionRefused` or relay lookup fail | Agent offline | Confirm remote agent is running with `host()` |
| `CO_DIRECT_FAIL` + `CO_RELAY_FAIL` | Both paths failed | Agent likely offline — check with operator |
| Trust/permission error | Not authorized | Tell user to contact the remote agent admin for access |
| `InsufficientCreditsError` | No credits for `co/` models | Run `co status` to check balance |
| Script hangs (no output for >90s) | Remote agent requesting onboard (invite code/payment) | Kill script, tell user the remote agent requires onboarding |
