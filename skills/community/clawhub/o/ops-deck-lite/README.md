# ops-deck-lite

Lightweight agent productivity toolkit: semantic code search with local embeddings and a categorized prompt library. Two services, ~200MB RAM, zero cloud dependencies.

## Why

- **Code Search**: Your agent searches code by meaning, not grep. Ask "authentication middleware" and find `verifyToken()` even though the word "middleware" never appears in that file.
- **Prompt Library**: Stop writing the same prompts from scratch every session. Categorized, searchable, versioned.

## Stack

- **Code Search** (:5204) — FastAPI + SQLite + qwen3-embedding:8b via Ollama
- **Prompt Library** (:5202) — Express/Node + SQLite or JSON

Both managed by PM2. Total ~200MB RAM.

## Quick Start

```bash
ollama pull qwen3-embedding:8b
npm install -g pm2
pm2 start ecosystem.config.cjs
curl -X POST http://localhost:5204/api/index?summarize=true
```

## For the full stack, see `ops-deck`

Adds agent intel, social pipeline, dev journal, variant gallery, and system monitoring.

## Tags

code-search, prompt-library, embeddings, productivity, semantic-search, agent-tools
