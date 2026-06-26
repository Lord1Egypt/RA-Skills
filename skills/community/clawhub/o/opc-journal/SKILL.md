---
name: opc-journal
description: "OPC200 Journal - A CLI-style single skill for One Person Company growth tracking. Record entries, analyze patterns from dreams/memory, detect milestones, and generate insights. LOCAL-ONLY: no network calls."
user-invocable: true
command-dispatch: tool
tool: main
command-arg-mode: raw
metadata:
  openclaw:
    emoji: "📔"
    always: false
    requires: {}
---

# opc-journal

**Version**: 2.5.2  
**Type**: Single CLI-style Skill  
**Status**: Active

> A unified CLI entrypoint for journaling, pattern analysis, milestone detection, insights, and task tracking.

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize journal for customer | `/opc-journal init --day 1` |
| `record` | Record a journal entry | `/opc-journal record "Shipped MVP"` |
| `search` | Search entries | `/opc-journal search --query pricing` |
| `export` | Export journal | `/opc-journal export --format markdown` |
| `analyze` | Analyze patterns from memory | `/opc-journal analyze --days 7` |
| `milestones` | Detect milestones | `/opc-journal milestones --content "First sale!"` |
| `insights` | Generate daily/weekly insights | `/opc-journal insights --day 7` |
| `task` | Create async task | `/opc-journal task --description "Research"` |
| `batch-task` | Create multiple async tasks | `/opc-journal batch-task --descriptions "A" "B" "C"` |
| `status` | Show journal status | `/opc-journal status` |
| `delete` | Delete an entry by entry_id | `/opc-journal delete --entry-id JE-20260413-AB12CD` |
| `archive` | Archive all journal data | `/opc-journal archive --clear` |
| `update-meta` | Update metadata and language | `/opc-journal update-meta --language en` |
| `help` | Show help | `/opc-journal help` |

## Architecture

### Directory Structure

```
opc-journal/
├── scripts/
│   ├── main.py           # CLI entry point
│   └── commands/
│       ├── init.py       # Initialize journal with charter
│       ├── record.py     # Append entries with auto ID generation
│       ├── search.py     # Full-text local search
│       ├── export.py     # Markdown/JSON export
│       ├── analyze.py    # Structural signal + keyword fragment extraction
│       ├── milestones.py # Milestone candidate detection
│       ├── insights.py   # Context assembly for LLM interpretation
│       ├── task.py       # Single task creation (persistent)
│       ├── batch_task.py # Bulk task creation
│       ├── status.py     # Statistics and streak calculation
│       ├── delete.py     # Entry removal (requires --force)
│       ├── archive.py    # Backup and clear operations (requires --force)
│       ├── update_meta.py# Metadata and language updates
│       └── _meta.py      # Meta helpers with file locking
├── utils/
│   ├── storage.py        # File I/O with path sanitization
│   ├── parsing.py        # Entry block splitting/joining
│   ├── task_storage.py   # Task CRUD with fcntl locking
│   └── timezone.py       # Asia/Shanghai timezone utilities
├── tests/                # 57 pytest test cases
└── config.yml            # Skill metadata
```

### Data Flow

```
User Input → main.py → Command Router → Command Module → Storage Utils → Local Files
                                              ↓
                                         Return JSON {status, result, message}
```

All commands follow a uniform return pattern:
- `status`: "success" or "error"
- `result`: Structured data (dict, list, or None)
- `message`: Human-readable description

### Security Model

| Layer | Implementation |
|-------|---------------|
| Path Sanitization | `_sanitize_customer_id()` strips `..`, `/`, `\`; empty falls back to "default" |
| File Locking | `fcntl.flock()` with shared (read) / exclusive (write) locks on meta and tasks |
| Backup Strategy | `.bak` files created before any mutation (record, delete, archive) |
| Destructive Ops | `--force` flag required for delete and archive --clear |
| Scope | All I/O constrained to `~/.openclaw/customers/{customer_id}/` |

### LLM-First Design

This skill delegates **interpretation** to the caller (LLM) while providing **structured extraction**:

| Command | What Skill Does | What LLM Does |
|---------|-----------------|---------------|
| `analyze` | Extracts structural signals (punctuation, caps) + keyword fragments | Interprets emotional/psychological state |
| `insights` | Assembles context + signal counts | Generates personalized recommendations |
| `milestones` | Detects structural candidates (first entry, pattern breaks) | Validates and celebrates true milestones |
| `record` | Stores raw text + optional caller-provided emotion | Infers emotion if not provided |

**Key principle**: The skill extracts patterns but never draws conclusions about the user's mental state.

### Concurrency

- **Single-user optimized**: File locking prevents corruption but is not designed for high-concurrency multi-user scenarios
- **POSIX only**: Uses `fcntl` (not available on Windows)
- **Atomic writes**: Metadata writes use `flock(LOCK_EX)` + `fsync()` + `flock(LOCK_UN)`

### Storage Format

**Entry Block Format:**
```markdown
---
type: entry
entry_id: JE-20260413-A1B2C3
date: 13-04-26
day: 1
emotion: excited
language: en
---

Your entry content here.
```

**File Organization:**
- `memory/DD-MM-YY.md`: Daily entry files
- `journal_meta.json`: Goals, language, total count
- `tasks.json`: Persistent task list
- `archive/YYYYMMDD-HHMMSS/`: Timestamped backups

## Development Notes

- `analyze` reads `dreams.md` and `memory/*.md` and returns **structural signals + keyword fragments** for the caller (LLM) to interpret dynamically. Structural signals are purely quantitative (punctuation counts, caps, etc.). Keyword fragments use minimal regex patterns for common action/challenge/achievement words, but no emotional interpretation is baked in.
- `insights` returns **raw memory context and signal counts** for the caller (LLM) to generate recommendations dynamically. Includes keyword-based signal counts but defers semantic interpretation to the caller.
- `milestones` returns a **raw candidate object** for the caller (LLM) to validate and classify. No keyword-based auto-detection.
- `record` defers emotional interpretation to the caller. The `emotion` frontmatter field is only populated if the caller provides it in `metadata`.
- `task` creates a single async task record; `batch-task` creates multiple tasks in one call.
- `delete` removes an entry by `entry_id`, creates a `.bak` before modification, and updates the total count in meta. **Requires `--force` flag for destructive operations.**
- `archive` copies all memory files and `journal_meta.json` to a timestamped `archive/` directory. Use `--clear` to reset the journal after archiving. **Requires `--force` flag when using `--clear`.**
- `update-meta` updates journal metadata (language, goals, preferences). Retroactive translation rules are kept minimal because templates are now English-only by design.
- All data is stored locally under `~/.openclaw/customers/{customer_id}/`.
- No external network calls are made.
