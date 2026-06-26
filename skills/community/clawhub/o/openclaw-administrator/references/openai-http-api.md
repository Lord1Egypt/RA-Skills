# OpenAI-Compatible HTTP API

OpenClaw's Gateway can serve an OpenAI-compatible HTTP surface at the same port as the WebSocket. **Disabled by default.**

## Enable

Add to `~/.openclaw/openclaw.json`:

```json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": { "enabled": true }
      }
    }
  }
}
```

Or via CLI:
```bash
openclaw config set gateway.http.endpoints.chatCompletions.enabled true
openclaw gateway restart
```

## Endpoints (when enabled)

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/v1/chat/completions` | Chat completions (OpenAI-compatible) |
| `GET` | `/v1/models` | List agent targets |
| `GET` | `/v1/models/{id}` | Get single agent target |
| `POST` | `/v1/embeddings` | Embeddings |
| `POST` | `/v1/responses` | OpenResponses-compatible endpoint |

All run on the same port as the Gateway WebSocket (default `18789`).

## Gateway token

The HTTP endpoint uses the same token as your OpenClaw gateway. Send it as a bearer token on every request:

```
Authorization: Bearer <your-gateway-token>
```

Gateway token config modes (set in `openclaw.json`):
- `gateway.auth.mode="token"`: token comes from `gateway.auth.token` or the `OPENCLAW_GATEWAY_TOKEN` env var
- `gateway.auth.mode="password"`: password comes from `gateway.auth.password` or `OPENCLAW_GATEWAY_PASSWORD`
- `gateway.auth.mode="none"`: no token needed (only appropriate on a private/loopback interface)

Keep this endpoint on loopback or a private network — not exposed to the public internet.

## Model Field = Agent Target

The OpenAI `model` field is treated as an **agent target**, not a raw provider model id:

| `model` value | Routes to |
|---|---|
| `"openclaw"` | Configured default agent |
| `"openclaw/default"` | Configured default agent (stable alias) |
| `"openclaw/<agentId>"` | Specific agent (e.g. `"openclaw/research"`) |
| `"openclaw:<agentId>"` | Legacy alias (still supported) |
| `"agent:<agentId>"` | Legacy alias (still supported) |

`openclaw/default` is always stable even if the real default agent id changes between environments.

## Optional Request Headers

| Header | Effect |
|---|---|
| `x-openclaw-model: <provider/model>` | Override backend model for the selected agent |
| `x-openclaw-agent-id: <agentId>` | Compatibility agent override |
| `x-openclaw-session-key: <key>` | Fully control session routing |
| `x-openclaw-message-channel: <ch>` | Set synthetic ingress channel context |

`x-openclaw-model` examples: `openai/gpt-4o`, `anthropic/claude-opus-4-6`, `gpt-4o` (bare alias).

## Session Behavior

- **Default:** stateless per request — a new session key is generated each call.
- **With `user` field:** if the request includes an OpenAI `user` string, the Gateway derives a stable session key from it, so repeated calls share the same agent session.

## Streaming

Set `"stream": true` to receive Server-Sent Events (SSE):
- `Content-Type: text/event-stream`
- Each event line: `data: <json>`
- Stream ends: `data: [DONE]`

## Examples

### Non-streaming chat completion

```bash
curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "openclaw/default",
    "messages": [{"role":"user","content":"hi"}]
  }'
```

### Streaming with backend model override

```bash
curl -N http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-model: anthropic/claude-opus-4-6' \
  -d '{
    "model": "openclaw/research",
    "stream": true,
    "messages": [{"role":"user","content":"Explain the gateway architecture"}]
  }'
```

### Target a specific agent

```bash
curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "openclaw/coding",
    "messages": [{"role":"user","content":"Review this PR"}]
  }'
```

### Stable session (using `user` field)

```bash
curl -sS http://127.0.0.1:18789/v1/chat/completions \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "openclaw/default",
    "user": "my-stable-session-id",
    "messages": [{"role":"user","content":"Remember what we discussed?"}]
  }'
```

### List agent targets

```bash
curl -sS http://127.0.0.1:18789/v1/models \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

Returns `openclaw`, `openclaw/default`, and `openclaw/<agentId>` entries. Not raw provider catalogs.

### Get a single agent target

```bash
curl -sS http://127.0.0.1:18789/v1/models/openclaw%2Fdefault \
  -H 'Authorization: Bearer YOUR_TOKEN'
```

### Embeddings

```bash
curl -sS http://127.0.0.1:18789/v1/embeddings \
  -H 'Authorization: Bearer YOUR_TOKEN' \
  -H 'Content-Type: application/json' \
  -H 'x-openclaw-model: openai/text-embedding-3-small' \
  -d '{
    "model": "openclaw/default",
    "input": ["embed this text", "and this one too"]
  }'
```

`input` can be a string or array of strings. Use `x-openclaw-model` to specify the embedding model; without it, the agent's normal embedding setup is used.

## Open WebUI Quick Setup

1. Base URL: `http://127.0.0.1:18789/v1`
   - Docker on macOS: `http://host.docker.internal:18789/v1`
2. API key: your gateway bearer token
3. Model: `openclaw/default`

Smoke test first:
```bash
curl -sS http://127.0.0.1:18789/v1/models -H 'Authorization: Bearer YOUR_TOKEN'
```

If `openclaw/default` is in the response, Open WebUI (and most other compatible frontends) will connect without extra config.

## Notes

- `/v1/models` lists OpenClaw agent targets — not raw provider model catalogs.
- Sub-agents are internal execution topology and do not appear as pseudo-models.
- Backend provider/model overrides belong in `x-openclaw-model`, not the OpenAI `model` field.
- Requests are executed as normal Gateway agent runs — same codepath as `openclaw agent`.
