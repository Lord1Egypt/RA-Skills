# Installing NIMA Core

> **Persistent memory for AI agents running on OpenClaw**
> Zero-config by default. SQLite backend. Local embeddings. No API keys required.

---

## Prerequisites

- **Python 3.9+** (for database and memory processing)
- **Node.js 18+** (for OpenClaw hooks)
- **OpenClaw** running

---

## Quick Install (30 seconds)

```bash
cd /path/to/nima-core
./install.sh
openclaw gateway restart
```

Done. Your bot now has persistent memory.

---

## What Gets Installed

```text
~/.nima/
├── memory/
│   └── graph.sqlite      # SQLite database (10+ tables)
├── affect/
│   └── affect_state.json # Emotional state
└── logs/                 # Debug logs (optional)

~/.openclaw/extensions/
├── nima-memory/          # Captures conversations
├── nima-recall-live/     # Injects relevant memories
└── nima-affect/          # Tracks emotions
```

---

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                        NIMA Memory Flow                              │
└─────────────────────────────────────────────────────────────────────┘

  USER MESSAGE
       │
       ▼
  ┌─────────────┐     message_received
  │ nima-affect │ ───────────────────────► Detect emotion
  └─────────────┘                           Update Panksepp state
       │
       ▼
  ┌──────────────────┐     before_agent_start
  │ nima-recall-live │ ──────────────────────► Query memories
  └──────────────────┘                          Score by relevance
       │                                        Inject as context (3k tokens)
       ▼
  ┌──────────┐
  │  LLM     │ ◄─── Generates response with memory context
  └──────────┘
       │
       ▼
  ┌─────────────┐     agent_end
  │ nima-memory │ ─────────────► 3-layer capture (input/contemplation/output)
  └─────────────┘                 4-phase noise filter
       │                          Store in SQLite
       ▼
  DATABASE (~/.nima/memory/graph.sqlite)
```

### Hook Event Order

| Hook | Event | What It Does |
|------|-------|--------------|
| **nima-affect** | `message_received` | Detects emotions → Updates 7-affect state |
| **nima-recall-live** | `before_agent_start` | Searches memories → Injects context |
| **nima-memory** | `agent_end` | Captures conversation → Stores in DB |

---

## Database Setup

### SQLite (Default — Recommended)

**Why SQLite?**
- Zero configuration
- Single file (`~/.nima/memory/graph.sqlite`)
- Fast enough for most use cases
- No external dependencies

**Tables Created:**

| Table | Purpose |
|-------|---------|
| `memory_nodes` | Core memory entries (text, summary, embeddings, metadata) |
| `memory_edges` | Relationships between memories |
| `memory_turns` | Conversation turn structure |
| `memory_fts` | Full-text search (FTS5 virtual table) |
| `nima_insights` | Dream consolidation insights |
| `nima_patterns` | Detected patterns |
| `nima_dream_runs` | Dream cycle history |
| `nima_suppressed_memories` | Pruned memories |
| `nima_pruner_runs` | Pruner history |
| `nima_lucid_moments` | Spontaneous memory surfacing |

**Location:** `~/.nima/memory/graph.sqlite`

### LadybugDB (Optional Upgrade)

**When to use LadybugDB:**
- High-volume memory (100k+ entries)
- Need native graph queries (Cypher)
- Want HNSW vector search
- Multi-agent shared memory

**Performance comparison:**

| Metric | SQLite | LadybugDB |
|--------|--------|-----------|
| Text Search | 31ms | **9ms** (3.4x faster) |
| Vector Search | External | **Native HNSW** (18ms) |
| Graph Queries | SQL JOINs | **Native Cypher** |
| DB Size | ~91 MB | **~50 MB** (44% smaller) |

**How to install:**

```bash
# Install LadybugDB backend
pip install real-ladybug

# Run installer with LadybugDB (installs plugin + creates SQLite schema)
./install.sh --with-ladybug

# Initialize the LadybugDB graph schema (run once, idempotent)
python scripts/init_ladybug.py

# For existing v3.1.x installs: run the schema migration
python scripts/migrate_to_3_2_0.py
```

**LadybugDB Schema (v3.2.0)**

The complete graph schema includes:

| Node type | Description |
|-----------|-------------|
| `MemoryNode` | Primary memory — text, embedding (FLOAT[512]), affect, hive metadata |
| `Turn` | Conversation turn structure |
| `DreamNode` | Nightly dream consolidation narratives |
| `InsightNode` | Extracted insights from dream runs |
| `PatternNode` | Recurring cross-memory patterns |

| Relationship | Connects |
|-------------|---------|
| `relates_to` | MemoryNode ↔ MemoryNode (with `relation` + `weight`) |
| `has_input / has_contemplation / has_output` | Turn → MemoryNode |
| `derived_from` | InsightNode/DreamNode → source MemoryNodes |

Run `python scripts/init_ladybug.py --dry-run` to preview the full schema.

**⚠️ CRITICAL: LOAD VECTOR Requirement**

LadybugDB requires `LOAD VECTOR` to be called before any vector write operations. If you see `SIGSEGV` or crashes:

1. Ensure `LOAD VECTOR` is called during initialization
2. Check that the LadybugDB binary supports your platform
3. Consider falling back to SQLite if issues persist

**Configuration for LadybugDB:**

```json
{
  "plugins": {
    "entries": {
      "nima-memory": {
        "enabled": true,
        "identity_name": "your_bot_name",
        "database": {
          "backend": "ladybugdb",
          "auto_migrate": false
        }
      }
    }
  }
}
```

---

## Hook Configuration

### Adding to openclaw.json

Add this to `~/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "nima-memory": {
        "enabled": true,
        "identity_name": "your_bot_name"
      },
      "nima-recall-live": {
        "enabled": true
      },
      "nima-affect": {
        "enabled": true,
        "identity_name": "your_bot_name",
        "baseline": "guardian"
      }
    }
  }
}
```

**Replace `your_bot_name`** with your agent's name (e.g., "lilu", "assistant", etc.)

### nima-memory (Captures Memories)

**What it does:**
- Captures 3 layers: input (user), contemplation (thinking), output (response)
- Applies 4-phase noise filtering
- Calculates Free Energy (FE) score for importance
- Stores in SQLite or LadybugDB

**Key config options:**

```json
{
  "nima-memory": {
    "enabled": true,
    "identity_name": "your_bot_name",
    "skip_subagents": true,
    "skip_heartbeats": true,
    "free_energy": {
      "min_threshold": 0.2
    },
    "noise_filtering": {
      "filter_system_noise": true,
      "filter_heartbeat_mechanics": true
    }
  }
}
```

| Option | Default | Description |
|--------|---------|-------------|
| `skip_subagents` | `true` | Don't capture subagent sessions |
| `skip_heartbeats` | `true` | Don't capture heartbeat messages |
| `free_energy.min_threshold` | `0.2` | Minimum score to store (0.0-1.0) |
| `database.backend` | `"sqlite"` | `"sqlite"` or `"ladybugdb"` |

### nima-recall-live (Injects Memories)

**What it does:**
- Fires before every agent response
- Searches memories using hybrid (vector + text) search
- Scores by ecology (relevance + recency + importance)
- Injects top results as context (3000 token budget)

**Key config options:**

```json
{
  "nima-recall-live": {
    "enabled": true,
    "skipSubagents": true
  }
}
```

### nima-affect (Emotion Tracking)

**What it does:**
- Detects emotions from text (VADER sentiment + lexicon)
- Updates Panksepp 7-affect state (SEEKING, RAGE, FEAR, LUST, CARE, PANIC, PLAY)
- Modulates responses based on emotional state
- Supports personality archetypes

**Key config options:**

```json
{
  "nima-affect": {
    "enabled": true,
    "identity_name": "your_bot_name",
    "baseline": "guardian",
    "skipSubagents": true
  }
}
```

**Archetypes:**
- `"guardian"` — Protective, cautious, caring
- `"explorer"` — Curious, adventurous, bold
- `"trickster"` — Playful, mischievous, creative
- `"empath"` — Sensitive, emotional, compassionate
- `"sage"` — Wise, thoughtful, measured

---

## Embedding Providers

Embeddings power the semantic search in memory recall.

### Local (Default — No API Key)

- **Dimensions:** 384
- **Cost:** Free
- **Network:** Zero external calls
- **Setup:** None required

```bash
# Optional: Install for better local embeddings
pip install sentence-transformers
```

### Voyage AI (Best Quality)

- **Dimensions:** 1024
- **Cost:** $0.12/1M tokens
- **Network:** voyage.ai

```bash
export NIMA_EMBEDDER=voyage
export VOYAGE_API_KEY=pa-xxx
```

### OpenAI

- **Dimensions:** 1536
- **Cost:** $0.13/1M tokens
- **Network:** openai.com

```bash
export NIMA_EMBEDDER=openai
export OPENAI_API_KEY=sk-xxx
```

### Ollama (Local GPU)

- **Dimensions:** 768 (varies by model)
- **Cost:** Free
- **Network:** localhost only

```bash
# Start Ollama server
ollama serve

# Pull embedding model
ollama pull nomic-embed-text

# Configure NIMA
export NIMA_EMBEDDER=ollama
export NIMA_OLLAMA_MODEL=nomic-embed-text
```

---

## Troubleshooting

### "No memories being captured"

**Symptoms:** Database stays empty, no context injection

**Check:**
1. Is `nima-memory` enabled in `openclaw.json`?
2. Did you run `openclaw gateway restart`?
3. Check logs: `tail -f ~/.nima/logs/nima-*.log`
4. Is the database writable?
   ```bash
   python3 -c "import sqlite3, os; c=sqlite3.connect(os.path.expanduser('~/.nima/memory/graph.sqlite')); c.execute('SELECT 1'); print('OK')"
   ```

### "Recall not injecting context"

**Symptoms:** Agent doesn't reference past conversations

**Check:**
1. Is `nima-recall-live` enabled?
2. Are there memories in the database?
   ```bash
   sqlite3 ~/.nima/memory/graph.sqlite "SELECT COUNT(*) FROM memory_nodes"
   ```
3. Is the hook firing? Check for `[NIMA RECALL]` in logs

### "LadybugDB SIGSEGV / crash"

**Symptoms:** Segmentation fault when using LadybugDB

**Cause:** `LOAD VECTOR` not called before vector write

**Fix:**
1. Ensure you're using the latest `real-ladybug` package
2. Check initialization calls `LOAD VECTOR`
3. **Fallback:** Use SQLite instead (remove `database.backend: "ladybugdb"`)

### "Database locked"

**Symptoms:** `database is locked` errors

**Cause:** Multiple processes accessing SQLite without WAL mode

**Fix:**
```bash
# Check WAL mode is enabled
sqlite3 ~/.nima/memory/graph.sqlite "PRAGMA journal_mode"
# Should return: wal

# If not, enable it
sqlite3 ~/.nima/memory/graph.sqlite "PRAGMA journal_mode=WAL"
```

### "Hook not loading"

**Symptoms:** No `[NIMA]` messages in logs, hooks don't fire

**Check:**
1. Hooks exist at `~/.openclaw/extensions/nima-*/`
2. Each hook has `openclaw.plugin.json`
3. `openclaw.json` has correct plugin entries
4. Run `openclaw gateway restart`

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NIMA_DATA_DIR` | `~/.nima` | Data directory override |
| `NIMA_EMBEDDER` | `local` | Embedding provider: `local`, `voyage`, `openai`, `ollama` |
| `VOYAGE_API_KEY` | — | Required if `NIMA_EMBEDDER=voyage` |
| `OPENAI_API_KEY` | — | Required if `NIMA_EMBEDDER=openai` |
| `NIMA_OLLAMA_MODEL` | — | Model name for Ollama embeddings |
| `NIMA_LOG_LEVEL` | `INFO` | Logging verbosity |
| `NIMA_DEBUG_RECALL` | — | Set to `1` for recall debugging |

---

## Advanced: Full Schema Reference

### SQLite Tables

#### `memory_nodes`
Core memory storage.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto-increment ID |
| `timestamp` | INTEGER | Unix timestamp |
| `layer` | TEXT | Layer: `input`, `contemplation`, `output` |
| `text` | TEXT | Original text |
| `summary` | TEXT | Summarized version |
| `who` | TEXT | Speaker identifier |
| `affect_json` | TEXT | JSON of emotional state |
| `session_key` | TEXT | Session identifier |
| `conversation_id` | TEXT | Conversation identifier |
| `turn_id` | TEXT | Turn identifier |
| `embedding` | BLOB | Vector embedding |
| `fe_score` | REAL | Free Energy score (0.0-1.0) |
| `strength` | REAL | Memory strength |
| `decay_rate` | REAL | Decay rate |
| `last_accessed` | INTEGER | Last access timestamp |
| `is_ghost` | INTEGER | Ghosted (duplicate) flag |
| `dismissal_count` | INTEGER | Times dismissed |

#### `memory_edges`
Relationships between memories.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto-increment ID |
| `source_id` | INTEGER | Source node ID |
| `target_id` | INTEGER | Target node ID |
| `relation` | TEXT | Relation type |
| `weight` | REAL | Edge weight |

#### `memory_turns`
Conversation turn structure.

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PK | Auto-increment ID |
| `turn_id` | TEXT | Unique turn ID |
| `input_node_id` | INTEGER | Input node FK |
| `contemplation_node_id` | INTEGER | Contemplation node FK |
| `output_node_id` | INTEGER | Output node FK |
| `timestamp` | INTEGER | Unix timestamp |
| `affect_json` | TEXT | Emotional state |

#### `memory_fts`
FTS5 virtual table for full-text search.

### Dream Consolidation Tables

- `nima_insights` — Extracted insights
- `nima_patterns` — Detected patterns
- `nima_dream_runs` — Dream cycle history
- `nima_suppressed_memories` — Pruned memories
- `nima_pruner_runs` — Pruner history
- `nima_lucid_moments` — Spontaneous surfacing

---

## Cron Jobs

NIMA requires a set of scheduled cron jobs to run its full cognitive lifecycle — memory pruning, dream consolidation, embedding indexing, and precognitive context prep. These are **OpenClaw cron jobs** stored in `~/.openclaw/cron/jobs.json`.

All jobs use the standard naming convention below. Running `./scripts/doctor.sh` will tell you which ones are missing.

### Standard NIMA Cron Jobs

| Job Name | Schedule | Priority | Purpose |
|----------|----------|----------|---------|
| `nima-dream-consolidation` | daily 2AM | **critical** | dream-consolidates memories → insights & patterns |
| `nima-memory-pruner` | daily 2AM | **critical** | prunes low-value memories to keep DB lean |
| `nima-embedding-index` | daily 3AM | **critical** | rebuilds FAISS/embedding index for semantic search |
| `nima-precognition-miner` | daily 6AM | **critical** | mines patterns → generates precognitions |
| `nima-precognitive-actions` | every 4h | **critical** | pre-warms context cache for session injection |
| `nima-delta-scorer` | daily 3:30AM | recommended | scores memory deltas for importance/novelty |
| `nima-deduplication` | weekly Sunday 4AM | recommended | deduplicates near-duplicate memories |
| `lucid-memory-moments` | 4x/day (10AM/2PM/6PM/8PM) | recommended | spontaneous memory surfacing during active hours |

### Adding All Cron Jobs

Add the following to `~/.openclaw/cron/jobs.json` under the `"jobs"` array. Replace:
- `YOUR_NIMA_REPO` → path to your nima-core clone (e.g. `~/.nima/repo`)
- `YOUR_PYTHON` → path to your venv Python (e.g. `~/.nima/venv/bin/python3`)
- `YOUR_TELEGRAM_ID` → your Telegram user ID for delivery notifications

> **Windows (Jac-style):** Use forward-slash paths for Python and set `PYTHONPATH` explicitly:
> `C:/Users/YourUser/.openclaw/workspace/.venv/Scripts/python.exe`

```json
[
  {
    "id": "nima-dream-consolidation",
    "agentId": "main",
    "name": "nima-dream-consolidation",
    "enabled": true,
    "schedule": { "kind": "cron", "expr": "0 2 * * *", "tz": "America/New_York" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "Run NIMA dream consolidation. Execute: PYTHONPATH=YOUR_NIMA_REPO YOUR_PYTHON -c \"import sys; sys.path.insert(0,'YOUR_NIMA_REPO'); from nima_core.dream_consolidation import consolidate; r=consolidate(hours=24); print(f'Dreams: {r.get(\\\"memories_in\\\",0)} memories, {r.get(\\\"patterns\\\",0)} patterns, {r.get(\\\"insights\\\",0)} insights')\". Report the results.",
      "model": "anthropic/claude-sonnet-4-6",
      "timeoutSeconds": 600
    },
    "delivery": { "mode": "announce", "channel": "telegram", "to": "YOUR_TELEGRAM_ID" }
  },
  {
    "id": "nima-memory-pruner",
    "agentId": "main",
    "name": "nima-memory-pruner",
    "enabled": true,
    "schedule": { "kind": "cron", "expr": "0 2 * * *", "tz": "America/New_York" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "Run NIMA memory pruning. Execute: PYTHONPATH=YOUR_NIMA_REPO YOUR_PYTHON -m nima_core.memory_pruner prune --hours 24. Report the results.",
      "model": "anthropic/claude-sonnet-4-6",
      "timeoutSeconds": 300
    },
    "delivery": { "mode": "announce", "channel": "telegram", "to": "YOUR_TELEGRAM_ID" }
  },
  {
    "id": "nima-embedding-index",
    "agentId": "main",
    "name": "nima-embedding-index",
    "enabled": true,
    "schedule": { "kind": "cron", "expr": "0 3 * * *", "tz": "America/New_York" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "Run NIMA embedding index rebuild. Execute: PYTHONPATH=YOUR_NIMA_REPO YOUR_PYTHON -m nima_core.build_embedding_index. Report the results.",
      "model": "anthropic/claude-sonnet-4-6",
      "timeoutSeconds": 300
    },
    "delivery": { "mode": "announce", "channel": "telegram", "to": "YOUR_TELEGRAM_ID" }
  },
  {
    "id": "nima-delta-scorer",
    "agentId": "main",
    "name": "nima-delta-scorer",
    "enabled": true,
    "schedule": { "kind": "cron", "expr": "30 3 * * *", "tz": "America/New_York" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "Run NIMA delta scoring. Execute: PYTHONPATH=YOUR_NIMA_REPO YOUR_PYTHON -m nima_core.delta_scorer score. Report the results.",
      "model": "anthropic/claude-sonnet-4-6",
      "timeoutSeconds": 120
    },
    "delivery": { "mode": "announce", "channel": "telegram", "to": "YOUR_TELEGRAM_ID" }
  },
  {
    "id": "nima-precognition-miner",
    "agentId": "main",
    "name": "nima-precognition-miner",
    "enabled": true,
    "schedule": { "kind": "cron", "expr": "0 6 * * *", "tz": "America/New_York" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "Run NIMA precognition mining. Execute: PYTHONPATH=YOUR_NIMA_REPO YOUR_PYTHON -m nima_core.precognition mine. Report how many patterns and precognitions were generated.",
      "model": "anthropic/claude-sonnet-4-6",
      "timeoutSeconds": 120
    },
    "delivery": { "mode": "announce", "channel": "telegram", "to": "YOUR_TELEGRAM_ID" }
  },
  {
    "id": "nima-precognitive-actions",
    "agentId": "main",
    "name": "nima-precognitive-actions",
    "enabled": true,
    "schedule": { "kind": "cron", "expr": "0 */4 * * *", "tz": "America/New_York", "staggerMs": 300000 },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "Run NIMA precognitive actions preparation. Execute: PYTHONPATH=YOUR_NIMA_REPO YOUR_PYTHON -m nima_core.cognition.precog_actions prepare. Report winning tier, recommended model, mood, and actions completed.",
      "model": "anthropic/claude-sonnet-4-6",
      "timeoutSeconds": 60
    },
    "delivery": { "mode": "announce", "channel": "telegram", "to": "YOUR_TELEGRAM_ID" }
  },
  {
    "id": "nima-deduplication",
    "agentId": "main",
    "name": "nima-deduplication",
    "enabled": true,
    "schedule": { "kind": "cron", "expr": "0 4 * * 0", "tz": "America/New_York" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "Run NIMA memory deduplication. Execute: PYTHONPATH=YOUR_NIMA_REPO YOUR_PYTHON -m nima_core.deduplication deduplicate. Report the results.",
      "model": "anthropic/claude-sonnet-4-6",
      "timeoutSeconds": 300
    },
    "delivery": { "mode": "announce", "channel": "telegram", "to": "YOUR_TELEGRAM_ID" }
  },
  {
    "id": "lucid-memory-moments",
    "agentId": "main",
    "name": "lucid-memory-moments",
    "enabled": true,
    "schedule": { "kind": "cron", "expr": "0 10,14,18,20 * * *", "tz": "America/New_York" },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
      "kind": "agentTurn",
      "message": "Run NIMA lucid memory moments. Execute: PYTHONPATH=YOUR_NIMA_REPO YOUR_PYTHON -m nima_core.lucid_moments surface. Report any memories surfaced.",
      "model": "anthropic/claude-sonnet-4-6",
      "timeoutSeconds": 60
    },
    "delivery": { "mode": "announce", "channel": "telegram", "to": "YOUR_TELEGRAM_ID" }
  }
]
```

After editing `jobs.json`, restart the gateway: `openclaw gateway restart`

---

## Precognitive Actions (detail)

NIMA can pre-warm context *before* your sessions start by predicting what topics are likely and preparing relevant data (model tier, git status, recent memories, mood). This is called **precognitive actions**.

### How It Works

```text
Every 4 hours (cron):
  1. Read active precognitions from precognitions.sqlite
  2. Classify predictions into domains (coding, business, research, etc.)
  3. Resolve best model tier (deep/fast/balanced/vision) from openclaw.json
  4. Run preparation actions (git status, open PRs, memory recall, etc.)
  5. Write ~/.nima/precog_prep/latest.json (TTL: 4 hours)

At session start (before_agent_start hook):
  6. get_prep_context() reads the cache → injects "🔮 Prep: ..." context
```

> See the **Cron Jobs** section above for the full set of required jobs including these two.
> The precog jobs are already included in the complete job list.

### Checking Precog Status

```bash
# Check what's cached
python3 -m nima_core.cognition.precog_actions status

# Run manually
PYTHONPATH=~/.nima/repo python3 -m nima_core.cognition.precog_actions prepare

# Get the context string that gets injected at session start
python3 -m nima_core.cognition.precog_actions context

# Clear the cache
python3 -m nima_core.cognition.precog_actions clear
```

### Model Tiers

Instead of hardcoding model names, precog resolves **capability tiers** from your `openclaw.json` providers:

| Tier | Best for | Resolved by |
|------|----------|-------------|
| `deep` | Research, synthesis, architecture | Keywords: opus, o1, o3, pro, r1; prefers reasoning=true |
| `fast` | Coding sprints, quick tasks | Keywords: haiku, flash, mini, nano, lite |
| `balanced` | General work, marketing | Keywords: sonnet, gpt-4, gemini, qwen |
| `vision` | Image-needed tasks | Requires image in model input |

The winning tier is determined by vote across all active precognitions' detected domains.

### Supported Domains

`coding` · `architecture` · `debugging` · `research` · `learning` · `marketing` · `content` · `creative` · `business` · `finance` · `sales` · `ops` · `security` · `data` · `communication` · `personal` · `philosophy` · `general`

---

## Next Steps

1. **Configure your bot name** in `openclaw.json`
2. **Restart OpenClaw**: `openclaw gateway restart`
3. **Test memory**: Have a conversation, then ask "what do you remember?"
4. **Set up NIMA cron jobs** (see [Cron Jobs](#cron-jobs) above) for full cognitive lifecycle
5. **Check the dashboard**: `python3 -m nima_core.dashboard` (optional)

---

## Support

- **Docs:** https://nima-core.ai
- **GitHub:** https://github.com/lilubot/nima-core
- **Issues:** https://github.com/lilubot/nima-core/issues
