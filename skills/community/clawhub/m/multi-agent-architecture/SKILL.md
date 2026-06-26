---
name: multi-agent-architecture
description: Architecture guide for running multiple specialized AI agents on a single OpenClaw server. Covers workspace isolation, agent roles, shared memory, Telegram routing, rate limit management, monitoring, and self-healing. Use when you need more than one agent or want to split responsibilities between specialized bots.
version: 1.0.1
author: mosoonpi-ai
license: MIT
tags: multi-agent, architecture, agents, workspaces, telegram, monitoring, production
---

# Multi-Agent Architecture — Run Multiple AI Agents on One Server

## What You Get

- 💰 **5 agents on one €47/mo VPS** — no need for separate servers
- ⚡ **60% fewer rate limit hits** with multi-token strategy across agents
- 📉 **75% less token burn** with optimized AGENTS.md (target <5KB per agent)
- 🔄 **Self-healing** — crashed services auto-restart in under 5 minutes
- 🧠 **Shared knowledge** — agents access each other's discoveries via knowledge graph
- 🎯 **Specialized agents** — each does one thing well instead of one bot doing everything badly

## When to Use

- You need **more than one agent** with different specializations
- One agent is hitting rate limits and you want to **split the load**
- You want agents for **different tasks**: ops, trading, security, freelancing
- You need **isolated workspaces** so agents don't interfere with each other
- You want to route **different Telegram groups/topics** to different agents

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                 OpenClaw Gateway                  │
│          (single process, multiple agents)        │
├──────────┬──────────┬──────────┬────────────────┤
│  Agent 1 │  Agent 2 │  Agent 3 │   Agent N      │
│  (main)  │  (ops)   │  (trade) │   (custom)     │
├──────────┼──────────┼──────────┼────────────────┤
│workspace │workspace │workspace │  workspace     │
│          │  -ops    │  -trade  │  -custom       │
├──────────┴──────────┴──────────┴────────────────┤
│              Shared Infrastructure               │
│     (Docker, monitoring, LightRAG, backups)      │
└─────────────────────────────────────────────────┘
```

## Quick Start

### Step 1: Plan agents

| Agent | Role | Bot | Workspace |
|-------|------|-----|-----------|
| Main | Coordination | @main_bot | workspace |
| Ops | Monitoring | @ops_bot | workspace-ops |
| Security | Audits | @sec_bot | workspace-security |

### Step 2: Create workspaces

```bash
mkdir -p ~/.openclaw/workspace-ops/{skills,memory,scripts,state}
mkdir -p ~/.openclaw/workspace-security/{skills,memory,scripts,state}
```

### Step 3: Configure openclaw.json

```json
{
  "agents": {
    "main": {
      "name": "Main",
      "model": "anthropic/claude-sonnet-4-6",
      "workspace": "workspace",
      "channels": { "telegram": { "botToken": "TOKEN_1" } }
    },
    "ops": {
      "name": "Ops",
      "model": "anthropic/claude-sonnet-4-6",
      "workspace": "workspace-ops",
      "channels": { "telegram": { "botToken": "TOKEN_2" } }
    }
  }
}
```

### Step 4: Write AGENTS.md per agent

Keep each AGENTS.md **under 5KB**. Every byte loads into context every message. Smaller = cheaper.

### Step 5: Share skills via symlinks

```bash
ln -s ~/.openclaw/workspace/skills/self-improving \
      ~/.openclaw/workspace-ops/skills/self-improving
```

Share utilities. Don't share specialized skills.

## Rate Limit Management

### Multi-token strategy
Split agents across 2+ Claude subscriptions:
```json
{
  "auth-profiles": {
    "primary": { "token": "TOKEN_A" },
    "secondary": { "token": "TOKEN_B" }
  }
}
```

### Model priority
- Critical agents: Opus or Sonnet
- Background agents: Sonnet only
- When approaching limits: downgrade heavy agents mid-week

## Telegram Routing

**Option A: Separate bots** (recommended) — one bot per agent, cleanest.

**Option B: Forum topics** — one supergroup, each topic routes to a different agent.

**Option C: Commands** — `/ops check disk` → ops agent, everything else → main.

## Monitoring & Self-Healing

### Heartbeat per agent
Each agent has a HEARTBEAT.md — minimal checks, alert only on problems.

### Self-healing script (cron every 5 min)
```bash
#!/bin/bash
if ! openclaw gateway status | grep -q "running"; then
    openclaw gateway restart
fi
for svc in langfuse n8n lightrag; do
    if docker compose -f ~/docker/$svc/docker-compose.yml ps | grep -q "Exit"; then
        docker compose -f ~/docker/$svc/docker-compose.yml restart
    fi
done
```

### Agent watchdog
Track last response time per agent. Silent > 15 min → alert.

## Shared Memory

Three-tier architecture:
1. **Hot**: MEMORY.md — in context, instant, free, per-agent
2. **Warm**: memory_search — vector search, instant, free
3. **Deep**: Knowledge graph (LightRAG) — cross-agent, ~3-8 sec, small cost

See `lightrag-knowledge-base` skill for deep memory setup.

## Backup

Back up daily: openclaw.json, auth-profiles, all MEMORY.md, all memory/ dirs.
Back up weekly: skills/, scripts/, docker configs.
Keep 7 days. Automate via cron.

## Production Checklist

- [ ] Each agent: own workspace + AGENTS.md + MEMORY.md
- [ ] AGENTS.md < 5KB per agent
- [ ] Dedicated Telegram bot per agent (or topic routing)
- [ ] allowedChatIds on all bots
- [ ] Rate limits distributed across tokens
- [ ] Heartbeat configured per agent
- [ ] Self-healing cron running
- [ ] Daily backups automated
- [ ] Bot tokens secured (not in git/chat)

## Common Mistakes

1. **Too many agents too fast** — start with 2, add as needed
2. **Giant AGENTS.md** — 20KB = wasted tokens every message
3. **No rate limit plan** — 5 agents, one token = rate limits by Wednesday
4. **Shared workspace** — agents overwrite each other's memory
5. **No monitoring** — agent dies silently, nobody notices for hours
