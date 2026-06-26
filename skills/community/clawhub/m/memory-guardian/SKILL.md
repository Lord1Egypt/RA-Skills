---
name: memory-guardian
version: 1.0.0
description: Memory health monitoring, integrity checks, and 3-layer memory architecture for AI agents. Use when agents need to prevent memory loss, detect context overflow before it happens, manage session-to-permanent memory promotion, and maintain a clean memory state across long-running workflows. Includes automated health checks (file size, staleness, duplicates, orphans), migration triggers for vector stores, and emergency recovery via git history.
---

# Memory Guardian

Prevent memory loss and context overflow. 3-layer architecture with automated health checks.

## Architecture

```
Layer 1: Working Memory (session files, 7-day retention)
    ↓ promote durable facts before deletion
Layer 2: Permanent Memory (never pruned, manual only)
    ↓ migrate to vector store at 5,000+ lines
Layer 3: Archive (batch docs, value stacks — disk forever)
```

## Health Checks

Run `python3 scripts/memory_check.py` on heartbeat or manually. Catches:
- Files over 300 lines (split needed)
- Total memory over 3,000 lines (yellow alert → prune)
- Stale session files (>7 days → promote + delete)
- Duplicate content across files
- MEMORY.md index inconsistency
- Orphan files not referenced anywhere

## Danger Zones

| Total Lines | Risk | Action |
|-------------|------|--------|
| < 2,000 | 🟢 Green | Normal operations |
| 2,000-3,000 | 🟡 Yellow | Prune sessions, compress old entries |
| 3,000-5,000 | 🟠 Orange | Aggressive promotion to permanent, archive sessions |
| 5,000+ | 🔴 Red | Semantic search returns noise → migrate to FAISS |

## Promotion Protocol

Before deleting ANY session file, extract:
1. Credentials/keys → permanent (NEVER lose these)
2. Architecture decisions → permanent/business-strategy.md
3. Infrastructure changes → permanent/outreach-infrastructure.md
4. New project summaries → permanent/projects/[name].md
5. User preferences → permanent/user-system.md

Everything else (debug logs, intermediate results) → delete.

## Migration Triggers

| Trigger | Action |
|---------|--------|
| permanent/ > 5,000 lines | Migrate to FAISS vector store |
| Batch value-stack > 100 items | Add embeddings for semantic retrieval |
| ChatGPT corpus loaded | FAISS mandatory |
| Cross-batch connections > 50 | Consider Neo4j knowledge graph |

## Emergency Recovery

Everything is git-tracked. If memory corrupts:
1. `git log memory/` → find last good state
2. `git checkout <hash> -- memory/` → restore
3. Rebuild MEMORY.md index from `ls memory/permanent/`

## Context Budget

| Component | Tokens | Notes |
|-----------|--------|-------|
| System prompt | ~2,000 | Fixed |
| MEMORY.md | ~1,500 | Keep lean |
| Active session | ~1,000 | Today only |
| memory_search | ~500 | On-demand |
| **Total overhead** | **~5,000** | Of 200K+ available |
