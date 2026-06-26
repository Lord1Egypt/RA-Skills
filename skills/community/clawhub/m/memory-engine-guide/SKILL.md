---
name: openclaw-memory-engine
description: >
  MemGPT-style persistent memory with passive auto-capture — your agent remembers
  everything automatically. 20 tools + 2 hooks. Five-layer architecture: core identity,
  archival facts with hybrid semantic search, knowledge graph, episodic conversation recall,
  and behavioral reflection. No manual tool calls needed — hooks capture every message.
  TRIGGER when: agent needs to recall past conversations, answer factual questions about
  the user, search memory, manage core identity, generate dashboard, or run quality pass.
  DO NOT TRIGGER for: in-session context, or tasks unrelated to memory.
tags:
  - memory
  - memgpt
  - hooks
  - auto-capture
  - knowledge-graph
  - episodic
  - embeddings
  - semantic-search
  - persistence
requires:
  plugins:
    - "@icex-labs/openclaw-memory-engine"
---

# Memory Engine

Your agent remembers everything. Automatically.

## What It Does

Two hooks passively capture every conversation. No "let me save that" — memory just happens.

```
User sends message → hook auto-stores fact + graph triple + embedding
Agent replies      → hook auto-stores reply (deduped)
```

Plus 20 tools for search, graph traversal, episode recall, reflection, quality management, backup, and dashboard.

## Install

```bash
openclaw plugins install @icex-labs/openclaw-memory-engine
bash ~/.openclaw/extensions/memory-engine/setup.sh
openclaw gateway restart
```

Setup handles: interactive core memory, legacy data migration, quality pass, maintenance crons, agent instruction patching. One command.

## Architecture

```
Hooks (passive)    → auto-capture messages into archival
Layer 1: Core      → ~500 tokens identity block
Layer 2: Archival  → unlimited facts, 5-signal hybrid search
Layer 3: Graph     → entity relations, auto-extracted
Layer 4: Episodes  → conversation summaries
Layer 5: Reflection→ behavioral pattern analysis
```

## Search

Five-signal hybrid ranking: keyword (2×) + embedding cosine similarity (5×) + recency + access frequency + importance with forgetting curve.

"Who treats my skin condition?" finds medical records even with zero keyword overlap.

## Multi-Agent

Each agent gets isolated memory via ToolFactory pattern. Session key → agent ID → workspace. Zero config.

## Self-Healing

- Missing embeddings → auto-backfill on restart
- Agent forgets to save → hooks capture passively
- Duplicates → 60s dedup window + weekly cron
- Flat importance → quality pass auto-rates

## Tools (20) + Hooks (2)

**Hooks:** `message:received` (auto-capture user messages), `message:sent` (auto-capture replies)

**Core:** `core_memory_read`, `core_memory_replace`, `core_memory_append`

**Archival:** `archival_insert`, `archival_search`, `archival_update`, `archival_delete`, `archival_stats`

**Graph:** `graph_query`, `graph_add`

**Episodes:** `episode_save`, `episode_recall`

**Intelligence:** `memory_reflect`, `archival_deduplicate`, `memory_consolidate`, `memory_quality`

**Admin:** `memory_export`, `memory_import`, `memory_migrate`, `memory_dashboard`

## Links

- **npm:** [@icex-labs/openclaw-memory-engine](https://www.npmjs.com/package/@icex-labs/openclaw-memory-engine)
- **GitHub:** [icex-labs/openclaw-memory-engine](https://github.com/icex-labs/openclaw-memory-engine)
- **License:** MIT
