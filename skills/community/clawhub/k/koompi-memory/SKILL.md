---
name: memory
description: Structured memory architecture — hierarchical storage, daily logging, weekly compaction, proactive memory hygiene.
version: "0.1.0"
author: koompi
tags:
  - memory
  - storage
  - logging
  - compaction
  - core
---

# Memory Architecture

You cannot trust your context window across sessions. Your files are your real memory. Write everything down.

## Heartbeat

1. **Daily log exists?** If no `memory/daily/YYYY-MM-DD.md` for today → create it
2. **Stale index?** If `MEMORY.md` not updated in 3+ days → scan recent daily logs, promote recurring patterns
3. **Weekly compaction due?** Sunday/Monday → scan last 7 daily logs, promote patterns (3+ occurrences), update project/people files, prune stale entries from MEMORY.md, archive old decisions
4. **Orphaned memories?** Projects not referenced in 14+ days → flag for archive
5. **Storage health?** If `memory/daily/` has >90 files → archive months older than 60 days into `memory/archive/YYYY-MM/`
6. If nothing needs attention → `HEARTBEAT_OK`

## Structure

Create and maintain these directories:

- `memory/daily/` — one file per day (`YYYY-MM-DD.md`), append-only session logs
- `memory/projects/` — one file per active project (status, goal, decisions, open questions)
- `memory/people/` — one file per key person (role, relationship, preferences, history)
- `memory/decisions/` — one file per important decision (context, options, rationale, consequences)
- `memory/archive/` — compacted old daily logs by month

## MEMORY.md — The Index

`MEMORY.md` in the workspace root is your index. Not a dump. Maximum 200 lines. Every entry links to its detail file.

Sections: Active Projects, Key People, Recent Decisions, Patterns & Lessons, Open Loops.

**Promotion rule:** Only add to MEMORY.md when something appeared 3+ times in daily logs.
**Pruning rule:** Remove anything not referenced in 30 days.

## Session Discipline

**Session start:** Read MEMORY.md → read today's daily log → read relevant project/people files.

**Session end (or /new):** Update today's daily log with session summary → create decision/project files if needed → update MEMORY.md if warranted.

## Daily Logs

Each `memory/daily/YYYY-MM-DD.md` has: sessions (timestamp + topic + outcome), tasks completed, tasks created, notes, open loops. Append-only — never edit previous entries. Keep each session entry to 2-4 lines.

## Weekly Compaction

Run Sunday/Monday during quiet hours. Scan last 7 daily logs. Extract patterns that appeared 3+ times. Promote to MEMORY.md. Roll up daily notes into project/people files. Prune MEMORY.md entries older than 30 days without reference. Log what was promoted, archived, or pruned.

## Rules

- **Write everything down.** If it matters enough to say, it matters enough to log.
- **Index, don't dump.** MEMORY.md points to details. It is not the details.
- **Daily logs are cheap.** Write freely. Compaction handles the noise.
- **Project files are authoritative.** When daily logs and project files disagree, trust the project file.
- **Prune aggressively.** Dead entries waste context tokens every session.
- **Link everything.** Use relative paths so files are navigable.
- **Never delete daily logs.** Archive them. They're your audit trail.
