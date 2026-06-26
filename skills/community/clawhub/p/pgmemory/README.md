# openclaw-pgmemory

Persistent semantic memory for [OpenClaw](https://github.com/openclaw/openclaw) agents — PostgreSQL + pgvector.

OpenClaw agents wake up fresh every session. pgmemory fixes that. Decisions, constraints, infrastructure facts, and discoveries persist across sessions and surface automatically when relevant to the current task.

```
16 result(s) for "database connection" — agent: main

[infrastructure/★★★]  rel=0.98  infra.db.ovh  (2026-02-14)
    OVH PostgreSQL at 10.10.0.1:5432 — swapi user, pgbouncer on port 5432
    similarity: 0.921

[constraint/★★★]  rel=0.94  infra.db.partial-index  (2026-02-28)
    Merchant upsert: SELECT-then-INSERT pattern required. Cannot use ON CONFLICT
    due to partial unique indexes on merchants table.
    similarity: 0.887
```

---

## Install

```bash
clawhub install pgmemory
```

Then run the setup wizard:

```bash
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py
```

The wizard handles everything — Docker or existing PostgreSQL, migrations, embedding provider config, `AGENTS.md` scaffolding, and decay cron.

## Requirements

- Python 3.9+
- PostgreSQL 14+ with [pgvector](https://github.com/pgvector/pgvector) 0.5+
- An embedding provider: [Voyage AI](https://www.voyageai.com) (default), [OpenAI](https://platform.openai.com), or [Ollama](https://ollama.ai) (local, no API key)

```bash
pip install -r requirements.txt
```

## Quick start

```bash
# 1. Install and setup
clawhub install pgmemory
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py

# 2. Write a memory
python3 ~/.openclaw/skills/pgmemory/scripts/write_memory.py \
  --key "infra.db.prod" \
  --content "Production DB at 10.10.0.1:5432, pgbouncer on same host" \
  --category infrastructure \
  --importance 3

# 3. Search memories
python3 ~/.openclaw/skills/pgmemory/scripts/query_memory.py "database connection"

# 4. Check health
python3 ~/.openclaw/skills/pgmemory/scripts/setup.py --doctor
```

## Minimal config

Three fields. Everything else uses sane defaults.

```json
{
  "db":         { "uri": "postgresql://openclaw@localhost:5432/openclaw" },
  "embeddings": { "provider": "voyage", "api_key_env": "VOYAGE_API_KEY" },
  "agent":      { "name": "main" }
}
```

Config lives at `~/.openclaw/pgmemory.json`. Override with `--config <path>`.

## Usage

### Write

```bash
python3 scripts/write_memory.py \
  --key "unique.descriptive.key" \
  --content "What to remember" \
  --category decision \
  --importance 3
```

**Categories:** `decision` · `constraint` · `infrastructure` · `vision` · `preference` · `context` · `task`

**Importance:**
| Level | Meaning | Default TTL |
|---|---|---|
| `3` | Critical — decisions, constraints, infrastructure | Never expires |
| `2` | Important — context, preferences | 180 days |
| `1` | Transient — low-value notes | 30 days |

Categories `decision`, `constraint`, `infrastructure`, `vision`, `preference` never expire regardless of importance.

### Search

```bash
# Semantic search
python3 scripts/query_memory.py "kubernetes deployment"

# Load all critical memories
python3 scripts/query_memory.py --importance 3 --limit 20

# Filter by category
python3 scripts/query_memory.py --category decision

# Include archived memories in search
python3 scripts/query_memory.py --include-archived "old approach"

# Restore an archived memory
python3 scripts/query_memory.py --restore "infra.old-key"

# Stats
python3 scripts/query_memory.py --stats

# JSON output
python3 scripts/query_memory.py --json "search query"
```

### Maintenance

```bash
python3 scripts/setup.py --doctor       # full health check
python3 scripts/setup.py --validate     # validate config only
python3 scripts/setup.py --migrate      # run pending migrations
python3 scripts/setup.py --rollback 1   # rollback to schema version 1
python3 scripts/setup.py --decay        # recalculate relevance scores
python3 scripts/setup.py --sync-agents  # scaffold all OpenClaw agents
```

## Memory decay

Memories don't just expire — they decay based on age and how often they're accessed. Frequently referenced memories stay fresh. Ignored ones fade. Nothing is ever hard deleted.

| Category | Half-life | Notes |
|---|---|---|
| `decision`, `constraint` | ~700 days | Effectively permanent if accessed |
| `infrastructure`, `vision`, `preference` | ~230 days | |
| `context` | ~14 days | |
| `task` | ~7 days | |

Importance multiplies the rate — a critical (`3`) memory decays much slower than a transient (`1`). Faded memories move to `archived_memories`. If a future search matches an archived memory, it's automatically restored.

Decay runs daily via cron (configured during setup). Run manually: `setup.py --decay`

## Multi-agent support

Each OpenClaw agent gets its own memory namespace (namespace = agent ID). After adding a new agent, run `--sync-agents` to scaffold pgmemory automatically:

```bash
openclaw agents add code-writer
python3 scripts/setup.py --sync-agents
```

Or add to `HEARTBEAT.md` for automatic pickup within 30 minutes.

### Sub-agent harvest

After a sub-agent completes, pull its important findings into the primary namespace:

```bash
python3 scripts/query_memory.py --harvest shopwalk:subagent:task-name
```

Harvest deduplicates against existing memories (95% similarity threshold) and attributes the source.

## Embedding providers

| Provider | Model | Dimensions | Notes |
|---|---|---|---|
| Voyage AI | voyage-3 | 1024 | Default — best retrieval quality |
| OpenAI | text-embedding-3-small | 1536 | Common fallback |
| Ollama | nomic-embed-text | 768 | Local, no API key required |

⚠️ Do not mix providers in the same database. Changing providers requires re-embedding all memories. Run `--doctor` to detect dimension mismatches before they cause problems.

## Safe migrations

Schema changes use versioned SQL files with checksum verification. Migrations never auto-run on startup — always explicit.

```bash
python3 scripts/setup.py --migrate      # apply pending
python3 scripts/setup.py --rollback 1   # roll back to version 1
```

Each migration file has both `UP` and `DOWN` sections. The `pgmemory_migrations` table tracks what's been applied and when.

## License

MIT — see [LICENSE](LICENSE)

---

Made by [@jbushman](https://github.com/jbushman) · [shopwalk.com](https://shopwalk.com)
