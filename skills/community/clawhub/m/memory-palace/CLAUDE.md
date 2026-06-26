# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Version

Current: **v1.7.0** (see package.json)

## Build & Test Commands

```bash
# Build TypeScript
npm run build

# Run core tests
npm test

# Run all tests (including integration)
npm run test:all

# Run a specific test file (after build)
node --test dist/src/tests/manager.test.js
node --test dist/src/tests/experience.test.js
node --test dist/src/tests/llm.test.js
```

## Architecture Overview

Memory Palace is an OpenClaw Skill providing persistent memory management for AI agents.

### Core Layer (`src/`)

| Module | Purpose |
|--------|---------|
| `manager.ts` | Main orchestrator - CRUD, search, stats |
| `storage.ts` | File-based storage (Markdown + YAML frontmatter) |
| `experience-manager.ts` | Experience recording, verification, retrieval |
| `types.ts` | Core type definitions |

### Cognitive Modules (`src/cognitive/`)

- `cluster.ts` - Topic clustering via TF-IDF
- `entity.ts` - Entity tracking and co-occurrence analysis
- `graph.ts` - Knowledge graph construction

### Background Tasks (`src/background/`)

- `vector-search.ts` - Local vector search (BGE-small-zh-v1.5, optional)
- `time-reasoning.ts` - Parse temporal expressions (明天, 下周三, etc.)
- `concept-expansion.ts` - Expand queries with related concepts
- `conflict.ts` - Detect contradictory memories
- `compress.ts` - Memory compression strategies

### LLM Integration (`src/llm/`)

- `subagent-client.ts` - Subagent call framework with timeout/fallback
- `summarizer.ts` - AI-powered memory summarization
- Other LLM modules have been deprecated in favor of rule-based engines

## Storage Format

Memories stored as Markdown files in `{workspaceDir}/memory/palace/`:

```markdown
---
id: "uuid"
tags: ["tag1", "tag2"]
importance: 0.8
status: "active"
createdAt: "2026-03-18T10:00:00Z"
updatedAt: "2026-03-18T10:00:00Z"
source: "conversation"
location: "projects"
type: "fact"  # or experience, lesson, preference, decision
---

Memory content here...
```

## Vector Search (Optional)

- Requires Python 3.8+ and `sentence-transformers`
- Model: BGE-small-zh-v1.5 (~100MB, auto-downloaded)
- Starts via `python scripts/vector-service.py`
- Graceful fallback to text search when unavailable

## Key Patterns

### Ebbinghaus Forgetting Curve

- `decayScore` (0-1) tracks memory freshness
- Each access: `decayScore = min(1, decayScore × 0.9 + 0.2)`
- Auto-archives when `decayScore < 0.1`
- Environment variables: `MEMORY_DECAY_ENABLED`, `MEMORY_DECAY_ARCHIVE_THRESHOLD`

### Experience Effectiveness Scoring

- Initial score: 0.1
- Each query use: +0.1
- Each verification (effective): +0.3
- Each verification (ineffective): -0.1
- Requires 2+ verifications to mark as "verified"

### API Style

Methods support object-style params with backward compatibility:
```typescript
// Both styles work:
manager.get(id)
manager.get({ id })
manager.recall(query, options)
manager.recall({ query, ...options })
```

## Module Dependencies

```
manager.ts
    → storage.ts (file I/O)
    → vector-search.ts (optional, semantic search)
    → time-reasoning.ts (temporal parsing)
    → concept-expansion.ts (query expansion)
    → experience-manager.ts (experience lifecycle)
```

## Recent Changes (v1.7.0)

- CLI supports `key=value` format arguments (e.g., `id=abc tags='["a","b"]'`)
- Added `deleteBatch(ids, permanent?)` for bulk deletion
- `storeBatch` vector indexing parallelized with `Promise.all`