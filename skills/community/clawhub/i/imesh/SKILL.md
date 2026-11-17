---
name: imesh
description: Operate an IMesh Python mesh for discovering trusted peers, starting a local node, calling remote skills, managing identities, and checking mesh health.
metadata:
  openclaw:
    requires:
      bins:
        - IMesh
    install:
      - kind: python
        package: IMesh
        command: python -m pip install -e .
---

# IMesh

Use this skill to operate the IMesh local-first AI-agent mesh from a shell.
IMesh uses an asynchronous WebSocket node, HMAC-signed task requests, mDNS peer
discovery, streaming task chunks, optional E2EE, and a FastAPI gateway.

## Safety rules

- Keep `OPENCLAW_WAN_ENABLED=false` (the default) unless the operator explicitly requests WAN connectivity.
- Never expose a remote skill unless it is registered with `expose_remote=True` and the peer is trusted.
- Set `OPENCLAW_PSK` to a long random shared secret before connecting peers. Both sides must share the exact same value.
- Do not print, copy, log, or commit private keys, API keys, `.env` files, or the gateway database (`*.db`).
- Prefer `127.0.0.1` while testing. Ask for explicit operator confirmation before using `0.0.0.0` or any public address.
- When `OPENCLAW_AUTH_REQUIRED=true`, always pass the Bearer token on execution endpoints.

## Common operations

### Start a local node

```bash
IMesh start --host 127.0.0.1 --port 8765
```

### Discover peers on the local network

```bash
IMesh discover
```

Returns a JSON array of peers with `name`, `host`, `port`, `skills`, and `reachable` fields.

### Call a skill on a trusted peer

```bash
IMesh call local echo \
  --url ws://127.0.0.1:8765 \
  --payload '{"message":"hello"}'
```

### Start the HTTP gateway

```bash
IMesh gateway --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/` in a browser for the interactive portal.

### Check gateway health

```bash
curl http://127.0.0.1:8000/api/v1/health
```

### List available skills

```bash
curl http://127.0.0.1:8000/api/v1/skills
```

### Execute a skill via the gateway

```bash
curl -X POST http://127.0.0.1:8000/api/v1/execute \
  -H 'Content-Type: application/json' \
  -d '{"skill": "echo", "payload": {"message": "hello"}}'
```

### Execute via OpenAI-compatible endpoint

```bash
curl -X POST http://127.0.0.1:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"openclaw-mesh","messages":[{"role":"user","content":"hello"}]}'
```

To target a specific skill: add `"skill": "skill_name"` to the body, or prefix the message with `call skill_name`.

### Identity management

```bash
# Generate a new Ed25519 keypair
IMesh keygen
IMesh keygen --output /path/to/identity.pem

# Show the current node identity (public key, name, path)
IMesh identity
IMesh identity --key /path/to/identity.pem
```

### Issue and use an API key

```bash
# Issue a new key
curl -X POST http://127.0.0.1:8000/api/v1/checkout/free-key

# Use the key on protected endpoints
curl -X POST http://127.0.0.1:8000/api/v1/execute \
  -H "Authorization: Bearer imesh_..." \
  -H 'Content-Type: application/json' \
  -d '{"skill":"echo","payload":{"msg":"ok"}}'
```

## Configuration

All variables use the `OPENCLAW_` prefix. They can be set in the environment or a `.env` file.

```bash
export OPENCLAW_PSK='replace-with-a-long-random-secret'
export OPENCLAW_DEFAULT_PORT=8765
export OPENCLAW_MDNS_ENABLED=true
export OPENCLAW_WAN_ENABLED=false
export OPENCLAW_AUTH_REQUIRED=false          # set true to enforce API keys
export OPENCLAW_GATEWAY_DB_PATH=./openclaw_gateway.db
export OPENCLAW_IDENTITY_KEY_PATH=./.openclaw_identity.pem
export OPENCLAW_PEER_TTL_SECONDS=120
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| No peers returned by `discover` | mDNS blocked or disabled | Enable mDNS; open UDP 5353 on the firewall |
| Call rejected with signature error | PSK mismatch | Ensure both peers use the exact same `OPENCLAW_PSK` |
| Skill unknown | Skill not registered | Check `GET /api/v1/skills` or the node registry |
| `expose_remote` denied | Skill registered with `expose_remote=False` | Register the skill with `expose_remote=True` |
| Gateway returns 401 | Missing or invalid Bearer token | Issue a key with `/api/v1/checkout/free-key` |
| `EventLoopBlocked` warning | Blocking Zeroconf call in async context | Update to the current `discovery.py` (uses `asyncio.to_thread`) |
| Generator skill fails | Incorrect sync generator in async context | Update to the current `node.py` (uses `inspect.isgeneratorfunction`) |

Run `pytest -q` after changing the installation or runtime to verify the full test suite.
