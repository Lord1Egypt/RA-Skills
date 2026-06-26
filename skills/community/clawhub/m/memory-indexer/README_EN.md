# Memory Indexer 🧠

> Short-term memory keyword indexing tool for AI Agent long-term memory

**Version**: v2.0.0 | [中文](./README.md)

## Introduction

Memory Indexer helps AI Agents persist memory:

- Auto-extract keywords from memory content
- Build fast keyword → memory file index
- Multi-keyword search (AND/OR mode)
- Auto-discover related memories
- Timeline view of memories
- Mark and view important memories
- Incremental sync of external memory directory
- Session backup & compact (prevent unlimited session memory growth)

## Why Do We Need It?

AI Agents lose context after each session ends. Traditional solutions only save raw text, making retrieval difficult.

Memory Indexer makes memory searchable, relatable, and traceable through keyword indexing.

## Features

1. Auto keyword extraction: using jieba Chinese word segmentation
2. Multi-mode search: OR (any match) / AND (all match)
3. Related discovery: auto-find memories that often appear together
4. Timeline view: show memories in chronological order
5. Active reminders: suggest related memories based on current keywords
6. Important memory marking: manually mark for priority retention
7. Incremental sync: only index new or modified files
8. Dead cleanup: auto-clean deleted memory indexes
9. Session backup & compact: backup user messages to index, compact session files to ~10KB
10. **Auto-search on new conversation**: Hook mechanism, auto-retrieve related memories when new session starts

## Installation

### Option 1: Run install script (recommended)

```bash
git clone https://github.com/smallmj/memory-indexer.git
cd memory-indexer
chmod +x install.sh
./install.sh
```

Install script will:
- Check and install dependencies (jieba)
- Create symlink to OpenClaw skills directory
- Configure AGENTS.md, MEMORY.md, HEARTBEAT.md

### Option 2: Manual install

```bash
git clone https://github.com/smallmj/memory-indexer.git
cd memory-indexer
pip install -r requirements.txt
ln -sf "$(pwd)" ~/.openclaw/workspace/skills/memory-indexer
python3 memory-indexer.py status
```

### Auto-config说明

Running `install.sh` will auto-configure:

| File | Content | Purpose |
|------|---------|----------|
| `AGENTS.md` | Memory search rules | Auto search related memory on new session |
| `MEMORY.md` | Mandatory rules: call indexer on save/new session | Auto build index, auto search |
| `HEARTBEAT.md` | Periodic sync + session backup | Auto backup and compact session memory |

**Manual config (without install.sh):**

If you don't want to run install.sh, manually add these configs in OpenClaw workspace:

1. **AGENTS.md** - Memory search rules for session start
2. **MEMORY.md** - Mandatory rules: call indexer on save/new session
3. **HEARTBEAT.md** - Periodic sync + session backup

**Manual Hook Installation (auto-search on new conversation):**

```bash
# Copy Hook directory to OpenClaw
cp -r hooks/memory-indexer-on-new ~/.openclaw/hooks/

# Restart Gateway to take effect
openclaw gateway restart
```

## Quick Start

```bash
# Add memory
python memory-indexer.py add "Today I learned Python"

# Search (OR mode)
python memory-indexer.py search "Python"

# Search (AND mode)
python memory-indexer.py search "Python AI" --and

# List all memories
python memory-indexer.py list

# Memory summary
python memory-indexer.py summary
```

## Integration with OpenClaw

```bash
cd ~/.openclaw/workspace
uv pip install jieba
uv run python skills/memory-indexer/memory-indexer.py add "memory content"

# Session backup & compact (runs on every heartbeat)
uv run python skills/memory-indexer/session_backup.py
```

### Hook: Auto-search on New Conversation

Starting from v2.0.0, provides OpenClaw Hook `memory-indexer-on-new` to automatically search related memories when a new conversation starts.

**Install Hook:**

```bash
# Copy Hook directory to OpenClaw
cp -r hooks/memory-indexer-on-new ~/.openclaw/hooks/

# Restart Gateway to take effect
openclaw gateway restart
```

**How it works:**
- Hook listens for `/new` command (can be configured to auto-trigger in AGENTS.md)
- Automatically calls memory-indexer to search user-related memories
- Search keywords: user name, preferences, projects, tasks, etc.

**File location:** `~/.openclaw/hooks/memory-indexer-on-new/`

## Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `add` | Add memory | `add "Today I learned Python"` |
| `search` | Search memory | `search "Python"` |
| `search --and` | AND search | `search "Python AI" --and` |
| `list` | List all memories | `list` |
| `sync` | Sync external directory | `sync` |
| `cleanup` | Cleanup dead indexes | `cleanup` |
| `related` | Related discovery | `related` |
| `timeline` | Timeline view | `timeline` |
| `recall` | Active reminder | `recall "Python"` |
| `summary` | Memory summary | `summary` |
| `star` | Mark important | `star 20260312.md` |
| `stars` | View important memories | `stars` |
| `status` | View status | `status` |

## Config

Data directory: `~/.memory-indexer/`

```
~/.memory-indexer/
├── index.json          # keyword index
├── sync-state.json    # sync state
└── stars.json         # important memory marks
```

Backup directory: `~/.openclaw/workspace/memory-index/session-backups/`

Modify `WORKSPACE` variable in code to customize storage path.

## Update

```bash
cd memory-indexer
chmod +x update.sh
./update.sh
```

Update script will auto pull code, backup data, check dependencies, re-sync index.

---

Tech stack: Python 3.8+、jieba、argparse、json

Contribute: Welcome to submit Issue and Pull Request!
1. Fork this repo
2. Create feature branch (git checkout -b feature/xxx)
3. Commit changes (git commit -m 'Add xxx')
4. Push branch (git push origin feature/xxx)
5. Create Pull Request

License: MIT

Author: @smallmj | hexiealan007@gmail.com

---

If this project helps you, please ⭐ Star support!
