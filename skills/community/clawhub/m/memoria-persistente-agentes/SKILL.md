---
name: memoria-persistente-openclaw
description: "Persistent memory system for AI agents inspired by Letta/MemGPT. Three-layer memory architecture (Core, Archival, Recall) that lets agents remember across sessions. Use when: (1) agent needs to recall user preferences, context, or decisions from past conversations, (2) starting a new session and needing context continuity, (3) user says 'remember this', 'you should know', or 'like last time', (4) agent detects important information worth persisting, (5) periodic memory maintenance during heartbeats. NOT for: simple Q&A with no persistence need."
---

# Letta Memory

Three-layer persistent memory for agents. No more starting from zero every session.

## Architecture

| Layer | What | Where | When |
|-------|------|-------|------|
| **Core** | Always in context | `memory/core.md` | Every session, auto-loaded |
| **Archival** | Searchable storage | `memory/archival/*.md` | On demand, semantic search |
| **Recall** | Session transcripts | OpenClaw session files | When needed via memory_search |

## Core Memory (`memory/core.md`)

Compact (~500-1000 words), always loaded. The agent's "working memory".

### Structure

```markdown
# Core Memory

## Identity
- Agent name, personality, role

## User
- Name, preferences, communication style, key facts

## Active Context
- Current projects, recent events, pending tasks

## Quick Reference
- Frequently needed info (medications, schedule, credentials refs)
```

### Rules
- Keep under 1000 words — trim when it grows
- Edit directly when learning something new about user or context
- Move stale items to archival (don't delete, archive)

## Archival Memory (`memory/archival/`)

Long-term storage organized by topic. Searched, not loaded.

### Structure

```
memory/archival/
├── people/          # People and relationships
├── projects/        # Project details and decisions
├── decisions/       # Important decisions made
├── learnings/       # Lessons learned
└── reference/       # Facts, procedures, how-tos
```

### Writing archival entries

```markdown
# [Topic] — YYYY-MM-DD

## Summary
One-line description

## Details
Full context

## Tags
comma, separated, tags
```

### Reading archival
Use `memory_search` to find relevant archival entries. Never load all archival files at once.

## Automatic Behaviors

### On session start
1. Read `memory/core.md`
2. Read today's `memory/YYYY-MM-DD.md` if exists
3. If user context seems incomplete, search archival for relevant info
4. Never ask questions that core memory already answers

### During conversation
- When user shares new personal info → update core immediately
- When important decision made → write to archival
- When user says "remember this" → write to appropriate layer
- When correcting a mistake → update core or archival

### On heartbeat
- Review recent `memory/YYYY-MM-DD.md` files
- Promote repeated archival entries to core
- Trim core when >1000 words
- Consolidate duplicate archival entries

## Memory Operations

### Core → Archival (demotion)
When core grows too large or items become stale:
1. Move item to appropriate archival file
2. Replace in core with brief reference (e.g., "See archival: projects/locatering")
3. Keep core scannable

### Archival → Core (promotion)
When archival info is needed repeatedly:
1. Move or copy key facts to core
2. Keep archival entry with cross-reference
3. Promotion triggers: mentioned 3+ times in a week, needed at session start

### Session → Archival (consolidation)
At natural breakpoints or heartbeat:
1. Read today's daily notes
2. Extract decisions, new info, lessons
3. Write to archival with proper tags
4. Update core if warranted

## Initialization

First run? Set up the structure:

```bash
mkdir -p memory/archival/{people,projects,decisions,learnings,reference}
```

Create `memory/core.md` if it doesn't exist:

```markdown
# Core Memory

## Identity
- [Agent fills this in]

## User
- [Agent fills this in]

## Active Context
- [Agent fills this in]

## Quick Reference
- [Agent fills this in]
```

## Scripts

### `scripts/consolidate.py`
Consolidates daily notes into archival entries. Run during heartbeats or manually.

```
python3 scripts/consolidate.py --days 7 --workspace /path/to/workspace
```

Options:
- `--days N` — look back N days of daily notes (default: 7)
- `--workspace PATH` — workspace root (default: current dir)
- `--dry-run` — show what would be written without writing

### `scripts/core-trim.py`
Trims core.md when it exceeds the word limit.

```
python3 scripts/core-trim.py --max-words 1000 --workspace /path/to/workspace
```

Options:
- `--max-words N` — maximum words for core.md (default: 1000)
- `--workspace PATH` — workspace root
- `--dry-run` — show what would be demoted without editing

## Anti-Patterns

- **Don't duplicate** — same info in core AND archival = waste. Core has summary, archival has detail.
- **Don't skip archival** — dumping everything in core defeats the purpose.
- **Don't forget to consolidate** — daily notes pile up. Run consolidation regularly.
- **Don't ask what you already know** — if core says "Renate takes Desvenlafaxina", never ask about medications.
- **Don't store secrets in core** — use archival/reference at minimum, prefer TOOLS.md for credentials.