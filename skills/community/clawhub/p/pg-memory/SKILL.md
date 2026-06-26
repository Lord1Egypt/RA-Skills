---
name: pg-memory
description: PostgreSQL-based structured memory system for OpenClaw agents with pre/post-compaction integration, dual-write capability, and full context preservation. Primary storage with markdown backup. Supports multi-agent deployments.
homepage: https://github.com/pottertech/pg-memory
metadata: {"clawdbot":{"emoji":"🧠","os":["darwin","linux"],"requires":{"bins":["psql","pg_ctl"]},"database":"postgresql"}}
---

# pg-memory v2.7.0 — Agent Memory for OpenClaw

> **Current Version: 2.7.0** | Updated: 2026-03-02
> **What's New:** Multi-instance support, auto-generated UUIDs, agent labeling
> **GitHub:** https://github.com/pottertech/pg-memory
> **Install:** Always use `main` branch — contains latest stable release

PostgreSQL-based memory system designed specifically for OpenClaw agents with **pre-compaction** and **post-compaction** integration.

**Architecture:** PostgreSQL primary + Markdown backup (configurable retention)
**Storage:** Full conversation context (exchanges, tool calls, observations)
**Search:** Full-text + importance ranking + semantic (with pgvector)
**Agents:** Multi-agent support with session isolation

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  OPENCLAW SESSION                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐│
│  │ User asks   │→│ Tools run   │→│  Response generated ││
│  └─────────────┘  └─────────────┘  └─────────────────────┘│
└─────────────────────────────────────────────────────────────┘
             │                           │
             ▼                           ▼
┌─────────────────────────────────────────────────────────────┐
│  PRE-COMPACTION                                             │
│  ├─> Save exchanges with tool results to `raw_exchanges`    │
│  ├─> Capture important observations to `observations`       │
│  ├─> Backup to markdown (7-day retention default)           │
│  └─> Prune old markdown files                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  POSTGRESQL (Primary)                                       │
│  ├─> sessions (conversation metadata)                       │
│  ├─> raw_exchanges (every message + response)             │
│  ├─> tool_executions (all tool calls with params/results) │
│  ├─> observations (curated important points)                │
│  └─> Full-text search indexes                             │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┴───────────────────┐
          ▼                                       ▼
┌─────────────────────┐              ┌─────────────────────┐
│  MARKDOWN BACKUP    │              │  POST-COMPACTION    │
│  (7-day default)    │              │  └─> Query recent   │
│  For safety net     │              │      observations   │
│  if pgdb down       │              │  └─> Restore context│
└─────────────────────┘              └─────────────────────┘
```

---

## 📋 Table Schema

### `sessions` - Conversation containers
```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    session_key VARCHAR(255) UNIQUE,  -- OpenClaw session UUID
    agent_id VARCHAR(100),            -- 'arty', 'brodie', etc.
    provider VARCHAR(50),             -- discord, telegram, web
    channel_id, user_id, user_label,
    summary TEXT,                     -- Brief description
    metadata JSONB,                   -- Additional context
    started_at, ended_at              -- Session lifecycle
);
```

### `raw_exchanges` - Every exchange (the "full context")
```sql
CREATE TABLE raw_exchanges (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions,
    exchange_number INTEGER,          -- Sequential: 1, 2, 3...

    user_message TEXT,              -- What user asked
    user_message_timestamp TIMESTAMP,
    user_metadata JSONB,

    assistant_thinking TEXT,        -- Internal reasoning
    assistant_response TEXT,        -- Final response
    response_timestamp TIMESTAMP,

    context_window_tokens INTEGER,    -- Conversation size
    model_version VARCHAR(100),     -- Which AI model used
    full_context_snapshot JSONB,    -- Complete exchange envelope

    -- Full-text search index on message + response
    tsvector_idx INDEX
);
```

### `tool_executions` - Every tool call
```sql
CREATE TABLE tool_executions (
    id UUID PRIMARY KEY,
    exchange_id UUID REFERENCES raw_exchanges,
    session_id UUID REFERENCES sessions,

    tool_name VARCHAR(100),         -- exec, read, write, etc.
    tool_params JSONB,              -- Full parameters
    tool_result JSONB,              -- Complete result
    execution_status VARCHAR(20),   -- success, error, timeout
    error_message TEXT,

    started_at, ended_at,           -- Duration tracking
    duration_ms INTEGER
);
```

### `observations` - Curated important points
```sql
CREATE TABLE observations (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions,

    obs_type VARCHAR(50),           -- decision, milestone, error, config, file_created, note, ongoing
    title TEXT,                     -- Short summary
    content TEXT,                   -- Full description

    importance_score DECIMAL(3,2),  -- 0.0 to 1.0
    tags TEXT[],                    -- ['rasa', 'deployment', 'critical']
    related_files TEXT[],           -- Files mentioned
    related_urls TEXT[],            -- URLs referenced

    derived_from_exchange_ids UUID[],  -- Which exchanges contributed
    user_requested BOOLEAN,         -- Did user say "remember this"?

    -- Temporal tracking (multi-day work support)
    status VARCHAR(20),           -- active, ongoing, resolved, superseded
    started_at TIMESTAMP,          -- When work began (can backdate)
    resolved_at TIMESTAMP,        -- When work completed

    created_at, updated_at
);
```

---

## 🚀 Quick Start

### 1. Install PostgreSQL

> **Note**: PostgreSQL 18+ recommended for best pgvector performance.

```bash
brew install postgresql@18
brew services start postgresql@18
```

> Install pgvector extension:
> ```bash
> brew install pgvector
> ```

### 2. Initialize Database
```bash
# Create database
createdb openclaw_memory

# Initialize schema
psql -d openclaw_memory -f scripts/init_memory_schema.sql
```

### 3. Configure OpenClaw Agent
```yaml
# ~/.openclaw/workspace/config/memory.yaml

memory:
  primary_backend: "postgresql"
  markdown_backup: true
  retention_days: 7
  agent_id: "arty"
  fallback_on_pgdb_down: true

postgresql:
  host: "localhost"
  port: 5432
  database: "openclaw_memory"
  user: "postgres"
```

### 4. Use in Agent Code
```python
from pg_memory_v2 import AgentMemory

# Initialize
mem = AgentMemory()

# Pre-compaction: Save exchange
mem.save_exchange(
    session_key=session_id,
    user_message="What port is Rasa on?",
    assistant_response="Rasa is on port 5006",
    tool_calls=[
        {
            'name': 'exec',
            'params': {'command': 'docker ps | grep rasa'},
            'result': {'stdout': 'rasa-server...port 5006'},
            'status': 'success'
        }
    ]
)

# Capture important observation
mem.capture_observation(
    session_key=session_id,
    obs_type="decision",
    title="Rasa deployed on port 5006",
    content="After resolving AVX compatibility issues...",
    importance=0.9,
    tags=["rasa", "deployment", "docker"]
)

# Post-compaction: Query memory
results = mem.search("Rasa port", days=7, min_importance=0.5)
# Returns: [{id, obs_type, title, importance_score, content, ...}]

mem.close()
```

---

## 🔧 Pre/Post-Compaction Integration

### Pre-Compaction Handler
```bash
# Called before OpenClaw context reset
python3 memory_handler.py pre-compaction < context.json

# context.json format:
{
  "session_key": "uuid",
  "exchanges": [...],
  "observations": [...],
  "metadata": {...}
}
```

**What it does:**
1. Saves all exchanges to `raw_exchanges` table
2. Saves all tool calls to `tool_executions` table
3. Captures curated observations to `observations` table
4. Backs up to markdown (retention_days)
5. Prunes old markdown files

### Post-Compaction Handler
```bash
# Called after OpenClaw context reset
python3 memory_handler.py post-compaction [session_key]
```

**What it returns:**
```json
{
  "session_key": "...",
  "recent_exchanges": [...],
  "observations": [...],  // High importance observations
  "stats": {...},
  "status": "ok"
}
```

### Proactive Search During Chat
```python
# When user asks about past work
results = mem.search("Rasa", days=7, min_importance=0.6)

# Full-text search on raw exchanges
exchanges = mem.search_exchanges("Docker error", days=1)

# Recent high-importance observations
obs = mem.get_recent_observations(hours=24, min_importance=0.8)
```

---

## 🗣️ Natural Language Query Builder (v2.4)

Ask questions in plain English - no SQL required!

> ⚠️ **Ollama Required**: Natural Language queries require a local Ollama instance. Install with: `brew install ollama && ollama serve`

> 📋 **Recommended Models** (tested): `ollama/mistral:latest`, `ollama/qwen2.5-coder:latest`

### CLI Usage

```bash
# Simple queries
pg-memory query "show me high-importance unresolved projects from last week"
pg-memory query "what did I work on yesterday"
pg-memory query "find all observations tagged with docker and error"
pg-memory query "list active projects from this month"

# With options
pg-memory query "top 10 recent decisions" --sql          # Show the SQL
pg-memory query "errors with high importance" --explain  # Preview without executing
```

### Python API

```python
from pg_memory import ask, query_nl

# Quick query
result = ask("show me high-importance unresolved projects from last week")
print(f"Found {result.result_count} observations")
for obs in result.results:
    print(f"  - {obs['title']} ({obs['status']})")

# Get explanation
explanation = ask("errors from yesterday", explain=True)
print(explanation)  # Shows SQL translation

# Access results
print(result.sql_query)           # Generated SQL
print(result.params)              # Query parameters
print(result.execution_time_ms)   # Performance metric
print(result.interpretation)      # What was understood
```

### Supported Query Patterns

| Pattern | Example | Result |
|---------|---------|--------|
| **Time** | "today", "yesterday", "last week", "last 7 days", "this month" | Date range filter |
| **Status** | "active", "ongoing", "resolved", "unresolved", "in progress" | Status filter |
| **Importance** | "high-importance", "critical", "medium importance", "low importance" | Score range |
| **Tags** | "tagged with docker", "tagged with #error,bug" | Array contains |
| **Content** | "about API", "containing error", "mentioning database" | Full-text search |
| **Type** | "projects", "tasks", "decisions", "errors" | obs_type filter |
| **Limit** | "top 10", "first 5", "limit 20" | Result limit |
| **Order** | "recent", "latest", "oldest" | Sort direction |

### Examples

```bash
# Time-based
"show me what I captured yesterday"
"find all observations from last 30 days"
"high-importance items from this week"

# Status-based
"list all unresolved projects"
"show ongoing tasks"
"recently resolved observations"

# Combined
"high-importance errors from last week"
"active projects tagged with urgent"
"top 5 unresolved decisions from this month"
"oldest ongoing observations"
```

### Query Interpretation

The system returns a human-readable interpretation:

```
Query: show me high-importance unresolved projects from last week
Interpretation: Search: from last week; with status: active, ongoing; importance: 70-100%; type: project
Results: 3 (in 12.3ms)
```

---

## 📊 Search Capabilities

### Types of Search

| Method | Use Case | Speed |
|--------|----------|-------|
| `search()` | Find curated observations | Instant (GIN indexes) |
| `search_exchanges()` | Search raw conversation | Fast (tsvector) |
| `get_recent_observations()` | Recent important items | Instant |
| `vsearch()` | Semantic similarity | Slow (requires pgvector) |

### Example Queries

```sql
-- Find important decisions
SELECT * FROM observations
WHERE obs_type = 'decision'
AND importance_score > 0.8
AND created_at > NOW() - INTERVAL '7 days';

-- Search raw exchanges
SELECT * FROM search_exchanges('Rasa port', 'arty', 7);

-- Recent activity across sessions
SELECT * FROM recent_activity;

-- Session summary with metrics
SELECT * FROM session_summary;
```

---

## ⏱️ Temporal Observations (Multi-Day Work)

PostgreSQL Agent Memory v2.1 adds **temporal observation tracking** - observations that span multiple days.

### The Problem

**Before:** Single-point-in-time observations:
- Day 1: "Starting caption tests"
- Day 2: Different observation, no link to Day 1
- No concept of ongoing work

**After:** Time-spanning observations:
- Day 1: Create with `status='ongoing'`, `started_at=2 days ago`
- Day N: Resolve with `status='resolved'`, `resolved_at=now`
- Duration tracked automatically

### Creating Multi-Day Work

```python
from pg_memory_v2 import AgentMemory
from datetime import datetime, timedelta

mem = AgentMemory()

# Day 1: Start work
obs_id = mem.capture_observation(
    session_key="caption_day1",
    obs_type="ongoing",              # Mark as work-in-progress
    title="[WIP] Caption System",
    content="Starting Y position tests...",
    importance=0.9,
    tags=["caption", "video", "wip"],
    status="ongoing",                # Not yet complete
    started_at=datetime.now() - timedelta(days=1)
)
# Returns UUID: '97d3f2ee-319b-44dd-9c84-e8d1f90cac73'
```

### Tracking Progress

```python
# Get all active/ongoing work
active = mem.get_active_observations(min_importance=0.5)
# Returns with duration_hours calculated automatically

# Get timeline view
timeline = mem.get_observation_timeline(days=30)
# Returns observations with status and duration
```

### Completing Work

```python
# Day N: Mark complete
mem.resolve_observation(
    observation_id='97d3f2ee-319b-44dd-9c84-e8d1f90cac73',
    final_title="Caption System Complete",
    final_content="Final: Y=1360, green #00FF00, 58px font"
)
# Sets status='resolved', resolved_at=NOW(), calculates duration
```

### Status Values

| Status | Meaning | When to Use |
|--------|---------|-------------|
| `active` | Default, newly created | Single-day tasks |
| `ongoing` | Work in progress | Multi-day features |
| `resolved` | Work completed | After resolve_observation() |
| `superseded` | Replaced by newer | Outdated observations |

### Database Columns

```sql
ALTER TABLE observations ADD COLUMN:
    status VARCHAR(20) DEFAULT 'active',     -- active, ongoing, resolved, superseded
    started_at TIMESTAMP WITH TIME ZONE,     -- When work began
    resolved_at TIMESTAMP WITH TIME ZONE;   -- When work completed (NULL if ongoing)
```

### Temporal Views

```sql
-- Active work (daily standup view)
SELECT * FROM active_observations;

-- Completed work with duration (weekly review)
SELECT * FROM completed_observations
WHERE resolved_at > NOW() - INTERVAL '7 days';
```

---

---

## 🔄 Dual-Write Strategy

### Why Dual-Write?

**PostgreSQL** = Primary (fast, queryable, structured)
**Markdown** = Safety net (human-readable, works if pgdb down)

### Configurable Retention

```yaml
# Keep 7 days of markdown backup
retention_days: 7

# After 7 days, markdown files are auto-deleted
# PostgreSQL retention: Indefinite (disk limited)
```

### Fallback Behavior

**If PostgreSQL is down:**
1. Write to markdown only (emergency mode)
2. Set status flag
3. Recover when pgdb back up

**If both fail:**
1. Context is lost (rare edge case)
2. Agent starts fresh

---

## 👥 Multi-Agent Support

```sql
-- Each agent has isolated sessions
SELECT * FROM sessions
WHERE agent_id = 'arty'
AND started_at > NOW() - INTERVAL '24 hours';

-- Cross-agent search (if needed)
SELECT * FROM observations
WHERE tags @> ARRAY['shared-project'];
```

---

## 📈 Migration from Markdown

### Existing Files
```python
from pg_memory_v2 import AgentMemory

mem = AgentMemory()

# Import existing markdown memories
mem.import_legacy_markdown(
    glob_pattern="~/.openclaw/workspace/memory/2026-02-*.md",
    parse_strategy="auto"  # Extract headers, bullet lists
)

# Track imports
SELECT * FROM memory_imports
WHERE import_status = 'success';
```

### Archive After Import
```bash
# Archive imported files to safe location
mv ~/.openclaw/workspace/memory/archive/
```

---

## ⚡ Performance Tips

### Indexes
- `sessions(agent_id, started_at DESC)` - Fast agent queries
- `observations(to_tsvector('english', content))` - Full-text search
- `observations(tags)` - Tag filtering
- `raw_exchanges(session_id, exchange_number)` - Pagination

### Connection Pooling
```python
# AgentMemory uses connection pooling by default
mem = AgentMemory(max_connections=10)

# Auto-reconnect if connection drops
if not mem._ensure_connection():
    # Retries in background
```

### Pruning Strategy

**pg_memory_prune.py** provides automated retention management:

#### Retention Policies (Configurable)

| Table | Retention | Archive | Rationale |
|-------|-----------|---------|-----------|
| **raw_exchanges** | 30 days | ✅ Yes | Full context ages out fast |
| **tool_executions** | 14 days | ❌ No | Tool results lose value quickly |
| **sessions** | 90 days | ✅ Yes | Session metadata retained longer |
| **observations** | **Forever** | ❌ No | Curated knowledge never deleted |

#### Storage Projections

**Without Pruning (Linear Growth):**

| Time | raw_exchanges | tool_executions | Total | Growth |
|------|---------------|-------------------|-------|--------|
| 30 days | ~1.5 GB | ~500 MB | **~2.1 GB** | Baseline |
| 90 days | ~4.5 GB | ~1.5 GB | **~6.1 GB** | +190% |
| 180 days | ~9 GB | ~3 GB | **~12 GB** | +471% |
| 1 year | ~18 GB | ~6 GB | **~24 GB** | +1043% |

**With Pruning Applied (Stable):**

| Time | Storage Used | Vs No Pruning | Savings |
|------|--------------|---------------|---------|
| 30 days | ~2.1 GB | Same | Baseline |
| 90 days | **~1.8 GB** | -70% | **~4.3 GB saved** |
| 180 days | **~2.0 GB** | -83% | **~10 GB saved** |
| 1 year | **~2.5 GB** | -89% | **~21.5 GB saved** |

#### Automated Pruning

```bash
# Daily at 3:00 AM via cron
0 3 * * * /path/to/pg_memory_prune.py --exec

# Manual execution
python3 pg_memory_prune.py --dry-run   # Preview deletions
python3 pg_memory_prune.py --exec      # Execute pruning

# Check stats
python3 pg_memory_prune.py --stats
```

#### Archive Strategy

- **Location:** `/Volumes/SharedData/postgres_archive/`
- **Format:** Gzipped JSONL
- **Retention:** 2 years before deletion
- **Restoration:** Manual import if needed

---

## 🚨 Troubleshooting

### PostgreSQL won't start
```bash
# Check logs
cat /opt/homebrew/var/log/postgresql@16.log

# Re-initialize (WARNING: loses data!)
rm -rf /opt/homebrew/var/postgresql@16
initdb --locale=en_US.UTF-8 -E UTF8 /opt/homebrew/var/postgresql@16
```

### Connection refused
```bash
# Ensure service is running
brew services start postgresql@16

# Check port
lsof -i :5432
```

### Import failures
```bash
# Check schema version
psql -d openclaw_memory -c "\dt"

# Verify column names match pg_memory_v2.py expectations
psql -d openclaw_memory -c "\d observations"
```

---

## 🎯 Observation Protocol (Auto-Creation)

**Priority**: ⛔ CRITICAL - REMEMBER FOREVER
**Directive**: "All new projects or tasks assigned should have an observation created if one does not exist."

### Why This Matters

**The Problem:**
- Agent receives new task/project
- Doesn't document it immediately
- Context gets compacted
- Agent forgets the work existed
- User thinks agent dropped the ball

**The Solution:**
- Every new assignment gets automatic observation
- Check existing → Create if missing → Return
- High importance (0.9) by default
- Tagged for easy filtering
- Never rely on "mental notes"

### Auto-Creation Methods

#### Method 1: `ensure_observation_exists()`

```python
from pg_memory_v2 import AgentMemory

mem = AgentMemory()

# Check if observation exists, create if not
result = mem.ensure_observation_exists(
    project_name="Gaming Trends Article",
    project_location="content/posts/gaming/",
    assigned_by="Skip",
    key_details="Write gaming trends for Feb 27",
    next_steps="Research Steam, PC Gamer"
)

print(result["was_created"])  # True = created, False = already exists
print(result["message"])
# "Observation created per protocol for 'Gaming Trends Article'"
```

**Template Applied:**
```markdown
## Gaming Trends Article
**Assigned**: 2026-02-27 18:14 EST
**Status**: Active
**Location**: content/posts/gaming/
**Key Details**: Write gaming trends for Feb 27
**Next Steps**: Research Steam, PC Gamer

*Observation created per protocol*
```

#### Method 2: `auto_capture_project()`

```python
from pg_memory_v2 import AgentMemory

mem = AgentMemory()

# Auto-extract project name from task description
result = mem.auto_capture_project(
    task_description="""Gaming Trends - Feb 27
Write article about Baldur's Gate patch, Marathon, Space Marine 2.
Make it Gen X tone.""",
    project_location="content/posts/gaming/",
    assigned_by="Skip"
)

# Automatically creates:
# - Project name: "Gaming Trends - Feb 27"
# - Key details: "Write article about..."
# - Tags: ['project:Gaming Trends', 'observation', 'assigned', 'active']
```

#### Method 3: `check_observation_exists()`

```python
# Just check if project already has observation
exists = mem.check_observation_exists("Gaming Trends Article")
# Returns: True or False
```

### Quick Convenience Functions

```python
from skills.pg_memory.scripts.pg_memory import (
    ensure_observation,
    check_observation,
    auto_capture
)

# One-liner convenience
result = ensure_observation(
    "Gaming Trends Article",
    "content/posts/gaming/",
    key_details="Write about Baldur's Gate patch",
    next_steps="Research PC Gamer, Steam"
)

# Quick check
if check_observation("Gaming Trends Article"):
    print("Already documented")
else:
    print("Needs observation")

# Auto-detection
result = auto_capture("""New task:
Build YouTube channel @PlotTwist
Create profile, banner, thumbnails
Upload first video""")
```

### Observation Protocol - Rules

1. **Every new assignment** gets an observation
2. **Check first** - don't create duplicates
3. **High importance** (0.9) - assignments are always important
4. **Include metadata** - location, assigner, key details, next steps
5. **Tag properly** - `project:name`, `observation`, `assigned`, `active`
6. **Never assume** - write it down even if it seems obvious

### Database Schema

```sql
-- Observations are created with:
-- - content_type = 'observation'
-- - importance_score = 0.9
-- - tags = ARRAY['project:Name', 'observation', 'assigned', 'active']
-- - metadata includes project_location, assigned_by, etc.

SELECT * FROM observations
WHERE tags @> ARRAY['observation', 'assigned']
AND importance_score >= 0.9
AND created_at > NOW() - INTERVAL '30 days';
```

### Enforcement

**This is the default behavior for OpenClaw agents.**

When you receive:
- "Can you write an article about gaming?"
- "Set up the newsletter landing page"
- "Create graphics for YouTube"

**The agent should immediately:**
1. Acknowledge receipt
2. Create observation (via `ensure_observation_exists()`)
3. Begin work
4. Update observation as work progresses

**No exceptions. No "I'll remember it."**

**Text > Brain. File > Memory. Always.**

---## 🔮 Future Enhancements

- [ ] **pgvector support** - Semantic embedding search
- [ ] **Web dashboard** - Browse/edit memories
- [ ] **Export to Notion/Airtable** - Sync to external tools
- [ ] **Memory compression** - Archive old sessions efficiently
- [ ] **Multi-node replication** - High availability

---

## 🔧 Multi-Instance Configuration

### Config File Locations (By OS)

pg-memory uses platform-appropriate config directories:

| OS | Config Directory | Full Path |
|:---|:-----------------|:---------|
| **macOS** | `~/Library/Application Support/pg-memory/` | `/Users/you/Library/Application Support/pg-memory/` |
| **Linux** | `~/.config/pg-memory/` | `/home/you/.config/pg-memory/` |
| **Windows** | `%APPDATA%\pg-memory\` | `C:\Users\you\AppData\Roaming\pg-memory\` |

### The Config File: `config.env`

Create this file in your platform's config directory:

```bash
# Database Connection
PG_MEMORY_HOST=localhost
PG_MEMORY_PORT=5432
PG_MEMORY_DB=openclaw_memory
PG_MEMORY_USER=your_username
PG_MEMORY_PASSWORD=your_password

# Agent Identity (REQUIRED for multi-instance)
OPENCLAW_NAME=arty
```

### The Instance File: `instance.json`

**Auto-generated on first run.** Contains your unique instance ID:

```json
{
  "instance_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "created_at": "2026-03-02T10:30:00",
  "platform": "Darwin",
  "hostname": "Kevins-Mac-mini"
}
```

**⚠️ CRITICAL:**
- **Never delete `instance.json`** — you'll lose your instance identity
- **Copy to new machines** if you want the same ID (usually not recommended)
- **Each machine gets unique ID** by default (correct for multi-instance)

### One-Time Setup Script

```bash
# Quick setup for macOS
mkdir -p ~/Library/Application\ Support/pg-memory/
cat > ~/Library/Application\ Support/pg-memory/config.env << 'EOF'
OPENCLAW_NAME=arty
PG_MEMORY_HOST=localhost
PG_MEMORY_PORT=5432
PG_MEMORY_DB=openclaw_memory
EOF

# Quick setup for Linux
mkdir -p ~/.config/pg-memory/
cat > ~/.config/pg-memory/config.env << 'EOF'
OPENCLAW_NAME=arty
PG_MEMORY_HOST=localhost
PG_MEMORY_PORT=5432
PG_MEMORY_DB=openclaw_memory
EOF
```

### Troubleshooting: "unknown" Agent Label

If you see `agent_label='unknown'`, your config file is:
1. ❌ In the wrong location (e.g., `~/.config/pg-memory/` on macOS)
2. ❌ Missing `OPENCLAW_NAME`
3. ❌ Not readable

**Fix:** Move to correct OS path (see table above).

---

## 📚 Reference

### Schema Files
- `scripts/init_memory_schema.sql` - Full PostgreSQL schema
- `scripts/pg_memory_v2.py` - Python integration module
- `scripts/memory_handler.py` - OpenClaw compaction handlers

### Configuration
- `~/.openclaw/workspace/config/memory.yaml` - Agent config
- Environment variables: `PGHOST`, `PGUSER`, `PGPASSWORD`

### Database Location
- **Default:** `/opt/homebrew/var/postgresql@16`
- **External disk:** `/Volumes/YourDisk/postgresql_data`

---

*Part of OpenClaw Agent Memory v2.0
Designed for context preservation across compaction cycles*
