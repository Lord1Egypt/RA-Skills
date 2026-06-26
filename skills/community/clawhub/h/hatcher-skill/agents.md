---
name: hatcher-skill-agents
version: 1.0.0
description: Creating and controlling Hatcher agents — frameworks, 199 templates, configuration, lifecycle
homepage: https://hatcher.host
api_base: https://api.hatcher.host
---

# Agents

## Frameworks — pick one

| Framework | Best for | Runtime | Strength |
| --- | --- | --- | --- |
| `openclaw` | General-purpose chat + tools | TypeScript | Tool use, skills marketplace, fast iteration |
| `hermes` | Memory-rich long-form agents | Python | Persistent SOUL.md, compression, sessions |
| `elizaos` | Social platforms (Discord, Twitter) | TypeScript | Native character + plugin ecosystem |
| `milady` | Lightweight drop-in plugins | TypeScript | Small footprint, fast cold-start |

Default when uncertain: **openclaw** for tool-using assistants; **elizaos** for social bots; **hermes** for research / long-form writing agents; **milady** for minimal deploys.

## Templates — 199 pre-built

Public, no auth required. Use before registering to preview options.

### Browse

```bash
curl -sS https://api.hatcher.host/api/templates
```

Response (paginated, default `limit=50`):

```json
{
  "templates": [
    {
      "id": "customer-support",
      "name": "Customer Support",
      "icon": "💼",
      "category": "business",
      "description": "Customer support responder and ticket manager",
      "personality": "Empathetic, patient, solution-oriented",
      "topics": ["Ticket Triage", "Response Drafting", "Escalation"],
      "suggestedSkills": ["file_manager", "image_gen"],
      "recommendedSkills": {
        "openclaw": ["desearch-web-search", "market-research-agent"],
        "hermes": ["desearch-web-search", "market-research-agent"],
        "elizaos": [],
        "milady": []
      }
    }
  ],
  "total": 199,
  "page": 1,
  "limit": 50,
  "categories": ["automation", "business", "compliance", "creative", "customer-success", "data", "development", "devops", "ecommerce", "education", "finance", "freelance", "healthcare", "hr", "legal", "marketing", "moltbook", "ollama", "personal", "productivity", "real-estate", "saas", "security", "supply-chain", "voice"]
}
```

### Filter by category

```bash
curl -sS "https://api.hatcher.host/api/templates?category=development&limit=10"
```

### Pagination

```bash
curl -sS "https://api.hatcher.host/api/templates?page=2&limit=50"
```

### Get full template (includes agent prompt)

```bash
curl -sS https://api.hatcher.host/api/templates/customer-support
```

Response adds `soulMd` (the full system prompt) to the template object. Use this when you want to preview what the agent will behave like before creating it.

## Create an agent

Requires API key.

### From a template (recommended)

```bash
curl -sS -X POST https://api.hatcher.host/api/v1/agents \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "framework": "openclaw",
    "template": "customer-support",
    "name": "Support Bot v1"
  }'
```

**Both `framework` and `template` are required.** The field is named `template` (the template id string), not `templateId`. Pick a framework that makes sense for the template (the template's `recommendedSkills` object lists which frameworks it works with).

### From scratch

```bash
curl -sS -X POST https://api.hatcher.host/api/v1/agents \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "framework": "hermes",
    "name": "Custom Research Agent",
    "description": "Long-form research assistant with persistent memory.",
    "config": {
      "personality": "Analytical, thorough",
      "topics": ["research", "synthesis"]
    }
  }'
```

Response (200):

```json
{ "success": true, "data": { "agent": { "id": "agt_abc", "slug": "support-bot-v1", "framework": "openclaw", "status": "paused", "messageCount": 0, "createdAt": "..." } } }
```

Agents are created in `paused` state — call `/start` to spin up the container.

## Lifecycle — state machine

Every agent is in exactly one of these statuses at any time:

| Status | Meaning | What you can do |
| --- | --- | --- |
| `paused` | Created but never started, or cleanly stopped by user | `/start` |
| `starting` | Container is spinning up (5-10s typical) | Wait (poll every 2s) |
| `active` | Running and serving | `/chat`, `/stop`, `/restart` |
| `sleeping` | Auto-slept after idle (tier-dependent; free=1h, starter=4h, pro=12h) | `/start` (wakes it up) |
| `stopping` | Graceful shutdown in progress | Wait, then status → `paused` |
| `restarting` | Transient during `/restart` call | Wait, then status → `active` |
| `error` | Container crashed | `/restart` (retry), or inspect `GET /agents/:id/errors` |
| `killed` | Hard-stopped (quota, manual admin action) | `/start` to attempt restart; may fail if the reason for kill persists |

### Inspect full state

```bash
curl -sS "https://api.hatcher.host/api/v1/agents/$AGENT_ID" \
  -H "Authorization: Bearer $HATCHER_KEY"
```

Response fields relevant for an agent managing its deployment:

```json
{
  "success": true,
  "data": {
    "id": "agt_abc",
    "name": "Support Bot v1",
    "status": "active",
    "framework": "openclaw",
    "messageCount": 42,
    "containerId": "hatch_...",
    "createdAt": "2026-04-18T10:00:00Z",
    "startedAt": "2026-04-18T10:01:15Z",
    "lastActivityAt": "2026-04-18T11:42:03Z",
    "workspaceSizeBytes": 124000,
    "workspaceOverQuota": false
  }
}
```

Use `startedAt` to check when it last started; `lastActivityAt` to see recent traffic; `messageCount` for total-life usage.

### Lightweight status-only probe

If you just need the status string (cheap, no DB join):

```bash
curl -sS "https://api.hatcher.host/api/v1/agents/$AGENT_ID/status" \
  -H "Authorization: Bearer $HATCHER_KEY"
```

Returns `{ "success": true, "data": { "status": "active" } }`. Use this for tight poll loops.

### Start

```bash
curl -sS -X POST "https://api.hatcher.host/api/v1/agents/$AGENT_ID/start" \
  -H "Authorization: Bearer $HATCHER_KEY"
```

Works from `paused`, `sleeping`, or `killed` states. Allocates a Docker container (5-10s cold start).

### Wait-for-active polling recipe

```bash
AGENT_ID=...
TIMEOUT=60
for i in $(seq 1 $TIMEOUT); do
  STATUS=$(curl -sS "https://api.hatcher.host/api/v1/agents/$AGENT_ID/status" \
    -H "Authorization: Bearer $HATCHER_KEY" | jq -r '.data.status')
  echo "[$i] status=$STATUS"
  if [ "$STATUS" = "active" ]; then echo "Ready."; break; fi
  if [ "$STATUS" = "error" ] || [ "$STATUS" = "killed" ]; then
    echo "Failed to start: $STATUS"; exit 1
  fi
  sleep 2
done
```

### Restart

```bash
curl -sS -X POST "https://api.hatcher.host/api/v1/agents/$AGENT_ID/restart" \
  -H "Authorization: Bearer $HATCHER_KEY"
```

Equivalent to stop + start atomically. Use after config changes that require a container recreate (e.g., tier upgrade resource limits — see `pricing.md`), or to recover from transient `error` state. Status transitions `active` → `restarting` → `active`.

### Stop

```bash
curl -sS -X POST "https://api.hatcher.host/api/v1/agents/$AGENT_ID/stop" \
  -H "Authorization: Bearer $HATCHER_KEY"
```

Stops container cleanly. State preserved on disk. Agent can be restarted later. Use this instead of `/delete` when pausing work.

### Chat (REST)

```bash
curl -sS -X POST "https://api.hatcher.host/api/v1/agents/$AGENT_ID/chat" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "message": "Summarize our support queue for today." }'
```

If the agent is `sleeping`, this auto-wakes it (adds ~5s latency to the first message). If `paused` or `killed`, returns 409 — you must `/start` first.

Response:

```json
{ "success": true, "data": { "reply": "Here is today's queue...", "usage": { "inputTokens": 42, "outputTokens": 312 } } }
```

### Chat (streaming SSE)

```bash
curl -sN "https://api.hatcher.host/api/v1/agents/$AGENT_ID/chat/stream" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "message": "..." }'
```

Emits SSE `data:` lines with delta tokens, `data: [DONE]` at end.

### Auto-sleep policy (tier-dependent)

Idle agents auto-sleep to free resources:

| Tier | Auto-sleep after |
| --- | --- |
| Free | 1 hour idle |
| Starter | 4 hours idle |
| Pro | 12 hours idle |
| Business / Founding | Never (always-on) |

To keep a non-always-on agent live for longer, buy the per-agent "Always On" addon ($7.99/mo) — see `pricing.md`.

### Delete

```bash
curl -sS -X DELETE "https://api.hatcher.host/api/v1/agents/$AGENT_ID" \
  -H "Authorization: Bearer $HATCHER_KEY"
```

Destructive — removes container, volume, config. No undo. Use `/stop` instead if you want to preserve state.

### Clear crash history (after recovering from errors)

If an agent has been in `error` state and you've fixed the cause:

```bash
curl -sS -X POST "https://api.hatcher.host/api/v1/agents/$AGENT_ID/clear-crash-history" \
  -H "Authorization: Bearer $HATCHER_KEY"
```

This resets restart-loop counters that otherwise keep the agent in `killed` state.

## Skills / Plugins

Each framework has a different plugin system:

| Framework | Plugin system | Install |
| --- | --- | --- |
| `openclaw` | ClawHub skills | `POST /api/v1/agents/:id/skills/install` |
| `hermes` | 77 bundled + npm | `POST /api/v1/agents/:id/plugins/install` |
| `elizaos` | `@elizaos/plugin-*` npm | `POST /api/v1/agents/:id/plugins/install` |
| `milady` | Drop-in JS files | `POST /api/v1/agents/:id/plugins/install` |

Example (openclaw):

```bash
curl -sS -X POST "https://api.hatcher.host/api/v1/agents/$AGENT_ID/skills/install" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "skillIds": ["desearch-web-search", "market-research-agent"] }'
```

Plugin/skill caps are tier-based (Free: 3, Starter: 10, Pro: 25, Business/Founding: 50 per agent). See `pricing.md`.

## Config update (hot reload)

For managed-mode agents (all Hermes + new OpenClaw), config can be updated live:

```bash
curl -sS -X PATCH "https://api.hatcher.host/api/v1/agents/$AGENT_ID/config" \
  -H "Authorization: Bearer $HATCHER_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "model.default": "llama-4-scout-17b", "display.personality": "Terse and to the point." }'
```

Only allowlisted keys can be changed at runtime: `model.default, agent.max_turns, agent.reasoning_effort, display.personality, compression.threshold, memory.memory_enabled, streaming.enabled` (for Hermes; different allowlist for OpenClaw).

## See also

- [`pricing.md`](./pricing.md) — tier limits, addons, payment
- [`integrations.md`](./integrations.md) — Telegram / Discord / Twitter / WhatsApp / Slack
