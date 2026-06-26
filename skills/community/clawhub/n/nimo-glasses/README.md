# @nimo/openclaw-glasses

> Connect Nimo AI Smart Glasses to OpenClaw via Companion App — private, on-device AI voice conversations.

Data flows directly from the glasses → Companion App → your OpenClaw Gateway. **No data passes through Nimo servers.**

---

## Features

- 🔗 **Secure pairing** — 6-digit one-time link code, rotates after each pairing
- 💬 **Chat API** — HTTP endpoint for text → AI reply
- 📡 **SSE streaming** — real-time token-by-token AI responses
- 🔐 **Session tokens** — bearer-token auth with 24h expiry
- ⚙️ **Configurable** — custom system prompt, max response length

---

## Installation

### Option A: From local path (development)

```bash
openclaw plugins install /path/to/nimo-openclaw-glasses-plugin
```

### Option B: Link for development (no copy)

```bash
openclaw plugins install -l /path/to/nimo-openclaw-glasses-plugin
```

### Option C: Copy into extensions directory (recommended for quick setup)

```bash
cp -r /path/to/nimo-openclaw-glasses-plugin ~/.openclaw/extensions/nimo-glasses
```

> **Important:** The plugin entry file must be `index.ts` at the root of the plugin directory (not in `src/`).

Then enable the plugin in your OpenClaw config:

```json5
{
  "plugins": {
    "allow": ["nimo-glasses"],
    "entries": {
      "nimo-glasses": {
        "enabled": true,
        "config": {
          "maxResponseLength": 300,
          "systemPrompt": "You are a helpful AI assistant in Nimo smart glasses. Be concise."
        }
      }
    }
  }
}
```

Restart the gateway:

```bash
openclaw gateway restart
```

---

## Pairing Flow

```
┌─────────────────────────────────────────────────────┐
│  1. Plugin starts → generates link code (e.g. A3X7K9) │
│     → logs to console + GET /nimo/health              │
│                                                       │
│  2. Open Nimo Companion App                           │
│     → Enter gateway URL (e.g. http://192.168.1.x:18789) │
│     → Enter link code                                │
│                                                       │
│  3. App calls POST /nimo/pair { linkCode: "A3X7K9" } │
│     → Plugin returns { token, expiresAt }            │
│     → Link code is invalidated + new one generated   │
│                                                       │
│  4. App stores token, uses it for all future calls   │
└─────────────────────────────────────────────────────┘
```

---

## API Reference

All routes use `auth: "plugin"` (no gateway auth required — plugin manages its own sessions).

### GET `/nimo/health`

Health check. Also exposes the current link code for initial pairing.

**Response:**
```json
{
  "status": "ok",
  "plugin": "nimo-glasses",
  "linkCode": "A3X7K9"
}
```

---

### POST `/nimo/pair`

Exchange a link code for a session token.

**Request body:**
```json
{
  "linkCode": "A3X7K9"
}
```

**Response (success):**
```json
{
  "token": "550e8400-e29b-41d4-a716-446655440000",
  "expiresAt": "2026-03-31T22:00:00.000Z"
}
```

**Response (failure — invalid code):**
```json
{ "error": "Invalid link code" }
```
HTTP status: 401

> After a successful pair, the link code is invalidated and a new one is generated.

---

### POST `/nimo/chat`

Send a message to the AI agent.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request body:**
```json
{
  "text": "What's the weather like today?",
  "stream": false
}
```

**Response (non-stream, `stream: false`):**
```json
{
  "text": "I don't have real-time access to weather data, but you can check..."
}
```

**Response (stream mode, `stream: true`):**
```json
{ "status": "streaming" }
```
HTTP status: 202 — then connect to `/nimo/events` to receive token chunks via SSE.

---

### GET `/nimo/events`

SSE long-connection for receiving AI reply chunks in streaming mode.

**Headers:**
```
Authorization: Bearer <token>
Accept: text/event-stream
```

**SSE event format:**
```
data: {"type":"text","content":"The weather","done":false}
data: {"type":"text","content":" today is sunny","done":false}
data: {"type":"text","content":"","done":true}
```

Fields:
- `type`: `"text"` | `"error"` | `"connected"`
- `content`: text chunk (empty string on final event)
- `done`: `true` signals end of response

---

## Configuration

| Field               | Type      | Default | Description                              |
|---------------------|-----------|---------|------------------------------------------|
| `maxResponseLength` | `integer` | `300`   | Max tokens in AI response                |
| `systemPrompt`      | `string`  | —       | Custom system prompt for the AI agent    |

Example:
```json5
{
  "plugins": {
    "entries": {
      "nimo-glasses": {
        "enabled": true,
        "config": {
          "maxResponseLength": 150,
          "systemPrompt": "You are Ori, an AI assistant in smart glasses. Be very brief — 1-2 sentences max. Respond in the user's language."
        }
      }
    }
  }
}
```

---

## Security Notes

- **Link code** is single-use and 6 characters (alphanumeric, confusable characters excluded)
- **Session tokens** are UUID v4, stored in memory only, expire after 24 hours
- **All routes** require either a valid session token (bearer) or the link code — no unauthenticated access to AI
- **Internal AI call** uses `http://localhost:{port}/v1/chat/completions` — stays within the local network
- The plugin does **not** store conversation history — each `/nimo/chat` call is independent

---

## Development

To run locally alongside the gateway:

```bash
# Link the plugin (symlink, no copy)
openclaw plugins install -l ./nimo-openclaw-glasses-plugin

# Enable in config
openclaw plugins enable nimo-glasses

# Restart gateway
openclaw gateway restart

# Watch the logs for the link code
openclaw gateway logs
```

Test the endpoints:

```bash
# Health check
curl http://localhost:18789/nimo/health

# Pair
curl -X POST http://localhost:18789/nimo/pair \
  -H "Content-Type: application/json" \
  -d '{"linkCode":"A3X7K9"}'

# Chat (non-stream)
curl -X POST http://localhost:18789/nimo/chat \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello! Who are you?","stream":false}'

# SSE stream (use a separate terminal first)
curl -N http://localhost:18789/nimo/events \
  -H "Authorization: Bearer <your-token>"

# Chat (stream mode)
curl -X POST http://localhost:18789/nimo/chat \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"text":"Tell me a joke.","stream":true}'
```

---

## Architecture

```
Nimo Glasses
    │  (Bluetooth/WiFi)
    ▼
Nimo Companion App
    │  (HTTP/JSON + SSE)
    ▼
OpenClaw Gateway
    │  (:18789/nimo/*)
    ▼
nimo-glasses plugin (this)
    │  (http://localhost:18789/v1/chat/completions)
    ▼
OpenClaw AI Agent
    │
    ▼
LLM (Claude / Gemini / etc.)
```

---

## License

MIT © Nimo AI
