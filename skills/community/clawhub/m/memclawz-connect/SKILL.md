---
name: memclawz-connect
description: "Connect any AI agent to the MemClawz shared memory bus. Gives agents read-before-act and write-after-complete patterns via a simple HTTP API. Use when an agent needs fleet memory, shared memory, cross-agent memory, or long-term recall across sessions. Triggers on: 'connect to memory', 'fleet memory', 'shared memory', 'memclawz', 'remember this across sessions', 'search memory'."
---

# MemClawz Connect

> One skill. Any agent. Shared memory.

## Setup

```bash
export MEMCLAWZ_URL="http://localhost:3500"   # or remote: http://YOUR_SERVER:3500
export MEMCLAWZ_AGENT_ID="my-agent"           # unique per agent
```

No API key required for default installs. If auth is enabled, also set `MEMCLAWZ_API_KEY`.

## Health Check

```bash
curl -s "$MEMCLAWZ_URL/health"
# {"status":"ok","version":"...","qdrant":"connected"}
```

## Agent Protocol

### Before ANY Task — Search First

```bash
curl -s "$MEMCLAWZ_URL/api/v1/search?q=TOPIC&limit=5"
```

Response:

```json
{"results": [{"content": "...", "agent_id": "quant-dev", "memory_type": "decision", "score": 0.92}]}
```

Use results as context before starting work. Avoids re-discovering what's already known.

### After Completing Work — Write Back

```bash
curl -s -X POST "$MEMCLAWZ_URL/api/v1/add" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Deployed v2.0 — fixed auth race condition with mutex on refresh",
    "agent_id": "'"$MEMCLAWZ_AGENT_ID"'",
    "memory_type": "event"
  }'
```

### Memory Types

| Type | When |
|------|------|
| `fact` | Discovered info (endpoints, versions, configs) |
| `decision` | Choices made (architecture, approach, tool selection) |
| `procedure` | How something was done (deploy steps, build process) |
| `event` | What happened (deployed X, fixed Y, shipped Z) |
| `insight` | Lessons learned (what worked, what didn't) |
| `intention` | Planned actions |
| `commitment` | Promises made |
| `action` | Actions taken |
| `outcome` | Results of actions |

### Stats

```bash
curl -s "$MEMCLAWZ_URL/api/v1/stats"
```

### List Agents

```bash
curl -s "$MEMCLAWZ_URL/api/v1/agents"
```

### Get Memories

```bash
curl -s "$MEMCLAWZ_URL/api/v1/memories?agent_id=$MEMCLAWZ_AGENT_ID&limit=50"
```

## AGENTS.md Integration

Append to your agent's `AGENTS.md`:

```markdown
## MemClawz Shared Memory

Fleet memory API: $MEMCLAWZ_URL/api/v1

### Before ANY task:
Search shared memory for relevant context:
curl -s "$MEMCLAWZ_URL/api/v1/search?q=<task keywords>&limit=5"

### After completing ANY significant work:
Write results to shared memory:
curl -s -X POST $MEMCLAWZ_URL/api/v1/add \
  -H "Content-Type: application/json" \
  -d '{"content": "<what was done>", "agent_id": "$MEMCLAWZ_AGENT_ID", "memory_type": "<type>"}'
```

## Remote Agents

For agents on a different server, just change `MEMCLAWZ_URL` from `localhost:3500` to the master's IP/hostname:

```bash
export MEMCLAWZ_URL="http://76.13.154.71:3500"
```

Everything else stays the same.
