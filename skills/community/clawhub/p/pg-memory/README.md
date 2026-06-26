# pg-memory v2.7.0

PostgreSQL-based structured memory system for OpenClaw.

> **Current Version: 2.7.0** (Updated 2026-03-02)
> **Previous:** v2.6.0  
> Install: Always use `main` branch — contains latest stable release

## Quick Install (New in v2.6.0)

```bash
# Clone and install
git clone https://github.com/pottertech/pg-memory.git
cd pg-memory
./install.sh              # Fresh install
./install.sh --reset      # Reset database (DESTROYS data)
```

**Requirements:** PostgreSQL 18+, Python 3.10+

## What's New in v2.7.0

### Multi-Instance Support
Deploy multiple OpenClaw instances sharing one PostgreSQL database:

- **Auto-Generated Instance IDs** — Unique UUID per machine
- **Agent Labeling** — Human-readable names (e.g., "arty", "brodie")
- **Concurrent Access Safety** — UPSERT patterns prevent conflicts
- **Instance Statistics** — Query data by machine/agent

**See:** `README-MULTI-INSTANCE.md` for full deployment guide

### Migration from Local to Remote
Move from local PostgreSQL to shared server:

```bash
# Export local database
pg_dump -h localhost -U postgres -d openclaw_memory > migration.sql

# Import to shared server
psql -h [remote-host] -U [user] -d openclaw_memory < migration.sql
```

**See:** `MIGRATION.md` for complete migration guide

---

## What's New in v2.6.0

### 1. Backup & Restore
Full database backup and restore capabilities:

```bash
# Create backup (compressed by default)
pg-memory backup                          # → ~/.pg-memory/backups/
pg-memory backup --no-compress           # Uncompressed SQL

# List backups
pg-memory backup --list

# Restore (interactive)
pg-memory restore --latest               # Most recent
pg-memory restore --file backup.sql.gz   # Specific file
pg-memory restore --latest --drop        # Drop first (WARNING: destroys data)
```

**Python API:**
```python
from pg_memory import backup, restore, list_backups

# Create backup
backup_path = backup(output_dir="./backups/", compress=True)

# List available backups
backups = list_backups()

# Restore
restore(backup_path, drop_existing=True)
```

### 2. JSON Export/Import
Machine-readable export for migrations:

```bash
# Export to JSON
pg-memory export --format json --output backup.json

# Import from JSON
pg-memory import --format json --file backup.json
```

**Python API:**
```python
from pg_memory import export_json, import_json

# Export
export_json("backup.json", since=datetime(2026, 3, 1))

# Import with duplicate detection
import_json("backup.json", skip_duplicates=True)
```

### 3. Duplicate Detection
Automatically detect similar observations before inserting:

```python
mem.capture_observation(
    content="New observation",
    check_duplicates=True,        # Enable duplicate check
    duplicate_threshold=0.85      # 0.0-1.0 similarity threshold
)
```

CLI:
```bash
pg-memory duplicate "Content to check" --threshold 0.85
```

### 4. Tag Autocomplete
Suggest tags based on content or existing tags:

```python
mem.suggest_tags("Netflix streaming merger")  # Returns: ['streaming', 'merger']
mem.suggest_tags_from_existing("pro")          # Returns: ['project', 'protocol']
```

CLI:
```bash
pg-memory tags --content "AI and streaming" --limit 5
pg-memory tags --partial "stre"              # Autocomplete
```

### 5. Full Install Script
One-command install for new OpenClaw runs:
- Checks PostgreSQL
- Installs dependencies
- Creates database
- Initializes schema
- Sets up configuration

## Previous Features (v2.5.0)

### Related Observations
- Link observations to each other bidirectionally
- Find related content by tags, content similarity

### Templates
Pre-built structures for:
- **Bug Report**, **Decision Record**, **Project Kickoff**, **Milestone**

### Summaries
Auto-generate from recent observations (ADDITIONAL data — originals preserved)

### Conflict Detection
Find potentially contradictory observations

### Natural Language Queries
Ollama-powered SQL generation:
```bash
pg-memory ask "What are the critical observations from last week?"
```

## Installation on Other OpenClaw Machines

**Always use v2.6.0 — latest stable release.**

```bash
# Clone the repository
git clone https://github.com/pottertech/pg-memory.git
cd pg-memory

# Verify version
cat package.json | grep '"version"'
# Should show: "version": "2.6.0"

# Install (new!)
./install.sh
```

### 6. Bulk Markdown Import
Import existing notes:

```bash
pg-memory import ~/memory/  --recursive
pg-memory import ./note.md --importance 0.9
```

### 7. Observation Chains
Track projects/workflows as linked sequences:

```bash
pg-memory chains                         # List all chains
pg-memory new-chain "Video Project"
pg-memory add-step <chain_id> -o <obs_id>
pg-memory finish-chain <chain_id>
```

## Complete Feature Set (v2.3.0)

| Feature | Status |
|---------|--------|
| Connection pooling | ✅ |
| Rate limiting | ✅ |
| Input validation | ✅ |
| Query caching | ✅ |
| Observation Protocol | ✅ |
| Status management | ✅ |
| Exchange ID tracking | ✅ |
| **Related observations** | ✅ NEW |
| **Templates** | ✅ NEW |
| **Summaries** | ✅ NEW |
| **Conflict detection** | ✅ NEW |
| **Follow-up reminders** | ✅ NEW |
| **Bulk markdown import** | ✅ NEW |
| **Observation chains** | ✅ NEW |

## Python API

### Basic
```python
from pg_memory import capture, search

obs_id = capture("Important", tags=["project"], importance_score=0.8)
results = search("postgres")
```

### Templates
```python
from pg_memory import use_template

obs_id = use_template("Bug Report", {
    "brief_description": "Audio sync issue",
    "detailed_description": "..."
})
```

### Summaries (Originals Safe)
```python
from pg_memory import summarize, search_summaries

summary_id = summarize(tags=["project"], days=7)
results = search_summaries("video")
```

### Chains
```python
from pg_memory import create_chain, add_step, finish_chain

chain_id = create_chain("Video Project", chain_type="project")
add_step(chain_id, observation_id=obs_1_id)
finish_chain(chain_id)
```

### Status Management
```python
from pg_memory import update_status, complete_project

update_status(obs_id, "resolved", notes="Video uploaded")
complete_project("warner-bros", notes="All done")
```

## Files

- `scripts/pg_memory.py` — Python client library
- `scripts/pg-memory-cli` — Command-line tool
- `scripts/init_memory_schema.sql` — Database schema
- `scripts/schema_v2_3_migration.sql` — Migration from v2.2

## Natural Language Queries (Optional)

Ask questions in plain English — no SQL required!

⚠️ **Requires Ollama**: Install with `brew install ollama && ollama serve`

### Recommended Models

| Model | Size | Best For |
|-------|------|----------|
| `mistral:latest` | ~4GB | General NL to SQL |
| `qwen2.5-coder:latest` | ~8GB | Complex SQL generation |
| `gemma2:9b` | ~5GB | Fast queries |

### Install Models
```bash
ollama pull mistral
ollama pull qwen2.5-coder
```

### Usage
```bash
# Search using natural language
pg-memory query "show me high-importance projects from this week"
pg-memory query "find observations tagged with docker"

# Python API
from pg_memory import ask
result = ask("what was I working on yesterday")
```

**Note:** Core pg-memory works without Ollama. NL queries are an optional feature.

## Requirements

| Component | Required | Install | Optional Feature |
|-----------|----------|---------|------------------|
| PostgreSQL 18+ | ✅ | `brew install postgresql@18` | — |
| Python 3.10+ | ✅ | Built-in | — |
| psycopg2-binary | ✅ | `pip3 install psycopg2-binary` | — |
| Ollama | ❌ | `brew install ollama` | NL Queries |

## License

MIT

---
Part of Proactive Agent v3.0 🦞
