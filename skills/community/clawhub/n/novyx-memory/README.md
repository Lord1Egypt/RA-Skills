# Novyx Memory

> Your AI agent remembers everything. When it's wrong, you rewind time.

The only OpenClaw memory skill with **time-travel rollback** and **tamper-proof audit trails**. Auto-saves conversations, auto-recalls relevant context, and lets you undo mistakes — including rewinding all memory to any point in time.

## 30-Second Demo

```
You:     My project uses Postgres and deploys to AWS.
Agent:   Got it, saved.
         [auto-saved to Novyx]

         --- next day ---

You:     What's our database?
Agent:   You're using Postgres, deployed to AWS.
         [auto-recalled from Novyx]

You:     !search deployment
Agent:   Search: "deployment"
         1. 92% My project uses Postgres and deploys to AWS.

         --- oops, bad info got saved ---

Agent:   Actually your database is MongoDB on Azure.
         [auto-saved — now memory is wrong]

You:     !rollback 1h
Agent:   Rolled back to 2026-03-05T14:00:00Z
         2 memories restored, 3 operations undone.

You:     What's our database?
Agent:   You're using Postgres, deployed to AWS.
         [correct again]

You:     !audit
Agent:   Recent Operations:
         3:01 PM POST /v1/rollback → 201 [f8a2c3d1]
         2:45 PM POST /v1/memories → 201 [b7e4a9f0]
         2:30 PM GET  /v1/memories/search → 200 [a3f8c2d1]
```

## Why Novyx?

| Feature | Novyx | Mem0 | Zep | Raw Context |
|---------|:-----:|:----:|:---:|:-----------:|
| Persistent memory | Yes | Yes | Yes | No |
| Semantic search | Yes | Yes | Yes | No |
| Time-travel rollback | **Yes** | No | No | No |
| Tamper-proof audit trail | **Yes** | No | No | No |
| Undo individual writes | **Yes** | No | No | No |
| Topic-based forget | **Yes** | No | No | No |
| Free tier | 5K memories | 1K | Paid only | N/A |

## Install

```bash
# ClawHub (recommended)
clawhub install novyx-memory

# Or manual
git clone https://github.com/novyxlabs/novyx-memory-skill.git skills/novyx-memory
cd skills/novyx-memory && npm install
```

## Quick Start

**1.** Get a free API key at [novyxlabs.com](https://novyxlabs.com) (5,000 memories, no credit card)

**2.** Configure your key — pick one:

```bash
# Option A: Environment variable
echo "NOVYX_API_KEY=nram_your_key_here" >> .env
```

```json
// Option B: openclaw.json
{
  "skills": {
    "novyx-memory": {
      "env": {
        "NOVYX_API_KEY": "nram_your_key_here"
      }
    }
  }
}
```

**3.** Start chatting. Memory works automatically.

## Commands

| Command | What it does | Example |
|---------|-------------|---------|
| `!remember <text>` | Save a specific fact | `!remember We use Python 3.11` |
| `!search <query>` | Semantic search with scores | `!search what database do we use` |
| `!rollback <time>` | Rewind memory to a point in time | `!rollback 1h` or `!rollback 2 days ago` |
| `!forget <topic>` | Delete memories matching a topic | `!forget old deployment config` |
| `!undo [N]` | Delete last N saved memories | `!undo` or `!undo 3` |
| `!audit [N]` | Show operations with integrity hashes | `!audit 5` |
| `!status` | Usage, tier, rollbacks remaining | `!status` |
| `!help` | List all commands | `!help` |

## How It Works

```
User message
    │
    ├─ Command? ──→ Execute (!rollback, !search, !undo, etc.)
    │
    ├─ Too short (<15 chars)? ──→ Pass through (saves API calls)
    │
    └─ Normal message
         ├─ recall(message) ──→ Inject relevant memories as context
         └─ remember(message) ──→ Auto-save (fire and forget)

Agent response
    │
    ├─ Too short (<20 chars)? ──→ Skip
    ├─ Too long (>500 chars)? ──→ Truncate, then save
    └─ remember(response) ──→ Auto-save (fire and forget)
```

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `apiKey` | `NOVYX_API_KEY` env var | Your Novyx API key |
| `apiUrl` | `https://novyx-ram-api.fly.dev` | API base URL |
| `autoSave` | `true` | Auto-save messages to memory |
| `autoRecall` | `true` | Auto-recall context before responses |
| `recallLimit` | `5` | Max memories to recall per query |

```javascript
const NovyxMemory = require('./skills/novyx-memory');
const memory = new NovyxMemory({
  autoSave: true,
  autoRecall: true,
  recallLimit: 5,
});

// In your agent loop:
const enrichedMessage = await memory.onMessage(userMessage, sessionId);
// ... send enrichedMessage to your LLM ...
await memory.onResponse(agentResponse, sessionId);
```

## What Novyx Features This Uses

| Endpoint | Purpose |
|----------|---------|
| `POST /v1/memories` | Save conversation turns |
| `GET /v1/memories/search` | Semantic recall |
| `DELETE /v1/memories/{id}` | Undo / forget |
| `POST /v1/rollback` | Time-travel rollback |
| `GET /v1/audit` | Tamper-proof operation log |
| `GET /v1/usage` | Tier and usage stats |

## Free Tier

| Resource | Limit |
|----------|-------|
| Memories | 5,000 |
| API calls | 500 / day |
| Rollbacks | 10 / month |
| Audit retention | 7 days |

No credit card required. [Get your key](https://novyxlabs.com)

## Run Tests

```bash
NOVYX_API_KEY=your_key npm test
```

## License

MIT
