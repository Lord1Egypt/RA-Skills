---
name: pgmemory
version: 1.2.0
description: Persistent semantic memory for OpenClaw agents — PostgreSQL + pgvector
author: jbushman
tags: [memory, postgresql, pgvector, embeddings, agents]
---

# pgmemory

Gives OpenClaw agents persistent semantic memory backed by PostgreSQL + pgvector.

Agents wake up fresh every session. pgmemory fixes that — decisions, constraints,
infrastructure facts, and discoveries persist across sessions and surface automatically
when relevant.

## Setup

Run once after installing:

```bash
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py
```

The wizard handles everything: Docker/PostgreSQL, migrations, embedding provider,
AGENTS.md scaffolding, and decay cron.

## When to use this skill

Read this SKILL.md when:
- Setting up pgmemory for the first time
- Adding a new OpenClaw agent and want it to have persistent memory
- Diagnosing memory issues (run `--doctor`)
- Switching embedding providers
- Understanding how memory decay or archiving works

## Core commands

### Write a memory

```bash
python3 ~/.openclaw/skills/pgmemory/scripts/write_memory.py \
  --key "unique.descriptive.key" \
  --content "What to remember" \
  --category decision \
  --importance 3
```

**Categories:** `decision` · `constraint` · `infrastructure` · `vision` · `preference` · `context` · `task`

**Importance:**
- `3` = critical — decisions, constraints, infrastructure. Never expires. Always loaded.
- `2` = important — context, preferences. Expires after 180 days if unused.
- `1` = transient — low-value notes. Expires after 30 days.

### Search memories

```bash
# Semantic search
python3 ~/.openclaw/skills/pgmemory/scripts/query_memory.py "database connection"

# Load all critical memories (importance 3)
python3 ~/.openclaw/skills/pgmemory/scripts/query_memory.py --importance 3 --limit 20

# Stats
python3 ~/.openclaw/skills/pgmemory/scripts/query_memory.py --stats

# List all keys
python3 ~/.openclaw/skills/pgmemory/scripts/query_memory.py --list
```

### Maintenance

```bash
# Full health check
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --doctor

# Validate config
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --validate

# Run pending migrations
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --migrate

# Sync pgmemory into all OpenClaw agent workspaces
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --sync-agents

# Run decay cycle manually
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --decay
```

## What to write to memory

Write immediately when:
- You make a **decision** about architecture, tooling, or approach
- You discover a **constraint** — something that will bite you if forgotten
- You complete **infrastructure** work (migrations, deployments, config changes)
- You identify a **preference** or **vision** that should guide future work
- A sub-agent completes — harvest its important findings

Skip writing for:
- Casual conversation
- Things already in MEMORY.md or other workspace files
- Anything you'd classify as importance 1 unless it's genuinely useful

## Multi-agent setup

Each OpenClaw agent gets its own namespace (= agent ID). Run `--sync-agents` after
adding a new agent to scaffold pgmemory automatically:

```bash
openclaw agents add code-writer
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --sync-agents
```

Or add `--sync-agents` to HEARTBEAT.md for automatic pickup within 30 minutes.

### Harvest from sub-agents

After a sub-agent completes, pull its important findings into the primary namespace:

```bash
python3 ~/.openclaw/skills/pgmemory/scripts/query_memory.py \
  --harvest shopwalk:subagent:task-label
```

## Memory decay

Memories decay based on age and category. Frequently accessed memories stay fresh.
Decayed memories move to archive (never deleted). Restored automatically if matched
in a future search.

Decay runs daily via cron (configured during setup). Run manually anytime:

```bash
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --decay
```

## Switching embedding providers

Changing providers after setup requires re-embedding all memories — you cannot mix
dimensions in the same database. Run `--doctor` first to check for mismatches.

⚠️ Provider migration (`--re-embed`) is planned for v1.1. For now: set up a fresh
database if you need to switch providers.

## Config reference

Minimal (all that's required):
```json
{
  "db":         { "uri": "postgresql://openclaw@localhost:5432/openclaw" },
  "embeddings": { "provider": "voyage", "api_key_env": "VOYAGE_API_KEY" },
  "agent":      { "name": "main" }
}
```

Default config is at `~/.openclaw/pgmemory.json`. Override with `--config <path>`.

Full config reference: see `references/schema.sql` and `CHANGELOG.md`.

## Requirements

- Python 3.9+
- PostgreSQL 14+ with pgvector 0.5+
- `psycopg2-binary`, `numpy` — install via `pip install -r requirements.txt`
- Embedding provider API key (or Ollama for local)
