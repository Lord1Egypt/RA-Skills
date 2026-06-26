---
name: supermemory
version: 0.2.1
description: Long-term agent memory with atomic fact extraction, relational versioning, semantic search, and entity profiles. Extracts facts from conversations, tracks how knowledge changes over time (updates/contradicts/extends), and provides instant recall across sessions and agents. Local-first (SQLite + on-device embeddings).
tags: memory, knowledge-graph, semantic-search, multi-agent, local-first
---

# Supermemory

Long-term memory for AI agents. Extracts atomic facts from text, tracks relations between memories (updates, contradicts, extends), embeds locally for semantic search, and auto-builds entity profiles.

## Setup

```bash
pip install openclaw-supermemory[local]
supermemory init        # creates ~/.supermemory/memory.db
supermemory serve       # starts API on :8642
```

Requires an LLM API key for fact extraction (default: Anthropic Haiku).

```bash
export ANTHROPIC_API_KEY=sk-...
# or configure via ~/.supermemory/config.yaml
```

## Commands

### Ingest (extract facts from text)

```bash
supermemory ingest "The project deadline moved to April 15. Sarah replaced Tom as lead." \
  --session meeting-notes --agent kit
```

LLM extracts atomic facts, categorizes them (person, decision, event, insight, preference, project), detects entities, and finds relations to existing memories. When a fact updates an existing one, the old memory is marked `superseded`.

### Search

```bash
supermemory search "project deadline" --top-k 10
supermemory search "project deadline" --all          # include superseded
supermemory search "project deadline" --as-of 2026-03-01  # time travel
```

### Entity operations

```bash
supermemory stats                # counts, categories
supermemory history Sarah        # version timeline
supermemory profile Sarah        # auto-built entity profile
```

### API

```
GET  /api/health                 # status + memory count
POST /api/search                 # {"query": "...", "top_k": 10}
POST /api/ingest                 # {"text": "...", "session_id": "..."}
GET  /api/entities               # all known entities
GET  /api/entity/{name}          # entity memories + profile
POST /api/search_entities        # entity-aware cross-session search
POST /api/aggregate              # count/sum queries over event clusters
```

Search latency: ~32ms warm, ~8s cold start (embedding model load).

## Agent integration

### Recall at session start

Inject relevant context before the agent processes a message:

```bash
supermemory search "current projects and priorities" --top-k 5
```

### Auto-ingest from responses

After meaningful agent turns, extract and store facts:

```bash
supermemory ingest "$RESPONSE_TEXT" --session $SESSION --agent $AGENT_ID
```

### OpenClaw plugin (zero-config)

Install the [supermemory-claw plugin](https://github.com/jared-goering/openclaw-supermemory/tree/main/plugin) for automatic memory injection and extraction with no agent code changes.

## Architecture

- **Storage:** SQLite with WAL mode (concurrent reads, single writer)
- **Embeddings:** Local sentence-transformers (free, on-device) or API (OpenAI/Cohere/Voyage via litellm)
- **Extraction:** LLM-based atomic fact extraction with relation detection (default: Haiku)
- **Entity system:** Join tables, aliases, auto-merged profiles across sources
- **Multi-agent:** Single DB with agent_id tagging, cross-agent semantic search

## Cost

~$0.01-0.02 per ingest (3 LLM calls: extract, relate, profile). Search is free (local embeddings).

## Links

- [PyPI](https://pypi.org/project/openclaw-supermemory/)
- [GitHub](https://github.com/jared-goering/openclaw-supermemory)
- [Plugin](https://github.com/jared-goering/openclaw-supermemory/tree/main/plugin)
