---
name: memory-ebbinghaus
description: Ebbinghaus forgetting curve memory lifecycle manager for AI agents. Automatically calculates memory strength decay, supports review reinforcement, archiving, and deletion. Use when managing agent memory files, cleaning up stale knowledge, or implementing spaced repetition for long-term memory. Triggers on "memory management", "forgetting curve", "clean up memory", "which memories are fading", "review memory", "add memory item", "记忆管理", "遗忘曲线", "清理记忆", "哪些记忆快忘了", "复习记忆".
---

# Memory Ebbinghaus

Ebbinghaus forgetting curve-based memory lifecycle manager. Tracks memory items with strength decay, review reinforcement, and archiving.

## Setup

First run — initialize the database:
```bash
python3 scripts/ebbinghaus.py status
# Auto-creates memory_db.json in current directory if not found
```

To use a custom path:
```bash
EBBINGHAUS_DB=/path/to/memory_db.json \
EBBINGHAUS_ARCHIVE=/path/to/MEMORY.md \
python3 scripts/ebbinghaus.py status
```

**Environment variables:**
| Variable | Default | Description |
|----------|---------|-------------|
| `EBBINGHAUS_DB` | `./memory_db.json` | Path to the JSON database |
| `EBBINGHAUS_ARCHIVE` | `./MEMORY.md` | File to append archived memories |

## Core Concept

**Strength formula**: `strength = e^(-days_elapsed / stability)`

| Status | Strength | Meaning |
|--------|----------|---------|
| 🟢 Active | ≥ 0.7 | Recently used, clear memory |
| 🟡 Decaying | 0.3–0.7 | Not used for a while |
| 🔴 Fading | < 0.3 | Needs review or cleanup |

**Stability**: starts at 1.0, multiplied by 1.5 on each review (the more you review, the slower it fades).

## Commands

```bash
# View all memory items and their current strength
python3 scripts/ebbinghaus.py status

# Recalculate all strength values (run daily)
python3 scripts/ebbinghaus.py decay

# Add a new memory item
python3 scripts/ebbinghaus.py add "content description" --category <cat> --source <origin>

# Review and reinforce (resets strength to 1.0, stability ×1.5)
python3 scripts/ebbinghaus.py review <id>

# Delete a memory item
python3 scripts/ebbinghaus.py forget <id>

# Archive to MEMORY.md (removes from active list, appends to archive file)
python3 scripts/ebbinghaus.py archive <id>

# Heartbeat mode — print items needing attention
python3 scripts/ebbinghaus.py heartbeat
```

## Heartbeat Integration

Add to your heartbeat config:
```
- Memory decay check: python3 /path/to/scripts/ebbinghaus.py heartbeat
```

Heartbeat output rules:
- 🔴 items exist → alert user, ask "review or forget?"
- Only 🟡 items → log silently, no interruption
- All 🟢 → output `HEARTBEAT_OK`

## Categories

| category | Meaning |
|----------|---------|
| `project` | Project/task completion |
| `tech` | Technical findings/solutions |
| `person` | Memory about someone |
| `event` | Important events |
| `general` | Other |

## Typical Workflows

**"Clean up old memories"**:
1. Run `decay` then `status`
2. List 🔴 items, ask user: review / forget / archive?
3. Execute chosen action

**"Remember this: XXX"**:
1. Run `add "XXX"`
2. Confirm added

**"Which memories are fading?"**:
1. Run `decay` to update strengths
2. Run `status`, highlight 🔴 items
