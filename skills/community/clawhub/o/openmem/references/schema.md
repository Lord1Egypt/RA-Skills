# OpenMem Database Schema

Default path: `~/.openclaw/workspace/memory/openmem.db`
Override with `OPENMEM_DB` env var.

## Table: memories

The primary store. Every row is one discrete memory.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `content` | TEXT UNIQUE | The memory text. Duplicate content is silently deduplicated. |
| `category` | TEXT | One of: `fact`, `insight`, `preference`, `correction`, `event`, `general` |
| `source` | TEXT | Where it came from: `manual`, `session:<id>`, `hook`, etc. |
| `importance` | REAL | 0.0–1.0. Higher = more likely to surface in search/bootstrap. |
| `session_id` | TEXT | OpenClaw session ID this came from (nullable) |
| `created_at` | INTEGER | Unix timestamp |
| `updated_at` | INTEGER | Unix timestamp |
| `access_count` | INTEGER | Incremented on every read. Used for future LRU eviction. |

## Table: memories_fts

FTS5 virtual table mirroring `memories.content`. Uses Porter stemmer.
Kept in sync automatically via triggers on INSERT/UPDATE/DELETE.

Search uses `bm25()` ranking combined with importance and recency:

```
score = bm25_rank - (importance × 2.0) - (age_in_days × 0.05)
```

Lower score = better match (bm25 returns negative values).

## Table: compressed_sessions

Tracks which OpenClaw sessions have been compressed into memories.

| Column | Type | Description |
|---|---|---|
| `session_id` | TEXT PK | OpenClaw session UUID |
| `session_file` | TEXT | Filename |
| `compressed_at` | INTEGER | Unix timestamp |
| `memory_count` | INTEGER | How many memories were extracted |

## Category Guide

| Category | Use for |
|---|---|
| `fact` | Objective facts about the world, system, or codebase |
| `insight` | Learned patterns, conclusions, or non-obvious observations |
| `preference` | User preferences, style choices, or stated desires |
| `correction` | Mistakes made and the correct approach |
| `event` | Things that happened (deployments, incidents, milestones) |
| `general` | Anything that doesn't fit above |
