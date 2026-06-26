---
name: ops-deck-lite
version: 1.0.0
description: "Lightweight agent productivity toolkit: semantic code search with embeddings and a categorized prompt library. Two services, ~200MB RAM, zero cloud dependencies. Your agent searches code by meaning (not grep) and reuses proven prompts instead of writing from scratch every time."
tags:
  - code-search
  - prompt-library
  - embeddings
  - productivity
  - semantic-search
  - agent-tools
category: tools
---

# Ops Deck Lite — Code Search + Prompt Library

Two high-impact services that make any AI agent dramatically more efficient: semantic code search and a categorized prompt library. Lightweight (~200MB RAM), local-only, zero cloud costs.

For the full operational stack (agent intel, social pipeline, dev journal, monitoring), see `ops-deck`.

## What You Get

### 1. Semantic Code Search (:5204)

Search your entire codebase by meaning, not just text matching. Ask "authentication middleware" and find the actual auth code even if it's called `verifyToken` or `checkSession`.

- **Hybrid search**: vector similarity + keyword matching
- **Local embeddings**: qwen3-embedding:8b via Ollama (free, private)
- **Code summaries**: each chunk gets a natural language summary for better semantic matching
- **Fast**: <100ms search across 96K+ code chunks
- **Nightly re-index**: cron at 4am keeps the index fresh

```bash
# Search
curl -s -X POST http://localhost:5204/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"database connection pooling","mode":"hybrid","limit":10}'

# Health check
curl -s http://localhost:5204/api/health

# Re-index (with summaries)
curl -X POST http://localhost:5204/api/index?summarize=true

# Filter by project
curl -s -X POST http://localhost:5204/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"error handling","mode":"hybrid","project":"my-api","limit":5}'
```

**Modes:**
- `hybrid` (default, best) — combines vector similarity with text matching
- `code` — raw code matching only
- `summary` — search against natural language summaries

### 2. Prompt Library (:5202)

Categorized, searchable prompt templates. Stop writing the same prompts from scratch every session.

```bash
# List all prompts
curl -s http://localhost:5202/api/prompts | python3 -c "
import sys,json
[print(f'{p[\"id\"]}: {p[\"title\"]} [{p[\"category\"]}]') for p in json.load(sys.stdin)]
"

# Get a specific prompt
curl -s http://localhost:5202/api/prompts/<id>

# Create a prompt
curl -s -X POST http://localhost:5202/api/prompts \
  -H "Content-Type: application/json" \
  -d '{"title":"Code Review","category":"coding","content":"Review this code for..."}'
```

## Prerequisites

- Node.js 18+ (for prompt library)
- Python 3.10+ with FastAPI and uvicorn (for code search)
- Ollama with `qwen3-embedding:8b` model
- PM2 for process management
- SQLite (for code search index, no external DB)

## Setup

### 1. Install dependencies

```bash
npm install -g pm2
pip install fastapi uvicorn aiofiles

# Ollama embedding model
ollama pull qwen3-embedding:8b
```

### 2. Create the Code Search service

```bash
mkdir -p pipeline/work/code-search
cd pipeline/work/code-search

# The server needs:
# - server.py (FastAPI app)
# - code_index.db (SQLite, auto-created on first index)
# - Ollama running locally for embeddings
```

Key code search server features:
- Walks your project directories, splits code into chunks
- Generates embeddings via Ollama API (localhost:11434)
- Stores chunks + embeddings + summaries in SQLite
- FastAPI with POST /api/search, GET /api/health, POST /api/index

### 3. Create the Prompt Library

```bash
mkdir -p pipeline/work/prompt-library/backend
cd pipeline/work/prompt-library/backend

# Express server with:
# - GET /api/prompts (list all)
# - GET /api/prompts/:id (get one)
# - POST /api/prompts (create)
# - PUT /api/prompts/:id (update)
# - DELETE /api/prompts/:id (delete)
# - SQLite or JSON file storage
```

### 4. PM2 config

```javascript
// ecosystem.config.cjs
module.exports = {
  apps: [
    {
      name: 'code-search',
      cwd: './pipeline/work/code-search',
      script: 'server.py',
      interpreter: 'python3',
      autorestart: true,
    },
    {
      name: 'prompt-library-api',
      cwd: './pipeline/work/prompt-library/backend',
      script: 'server.js',
      autorestart: true,
    },
  ]
};
```

### 5. Start and index

```bash
pm2 start ecosystem.config.cjs
pm2 save

# Initial code index (takes a few minutes depending on codebase size)
curl -X POST http://localhost:5204/api/index?summarize=true

# Set up nightly re-index
(crontab -l 2>/dev/null; echo "0 4 * * * curl -s -X POST http://localhost:5204/api/index?summarize=true > /dev/null") | crontab -
```

## Agent Integration

Add to your AGENTS.md or TOOLS.md:

```markdown
## Code Search API (USE THIS FIRST)

Before you grep, before you spawn a sub-agent, before you read 10 files: HIT THIS API.

curl -s -X POST http://localhost:5204/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"your search here","mode":"hybrid","limit":10}'

## Prompt Library

Before writing a prompt from scratch, check if one exists:

curl -s http://localhost:5202/api/prompts
```

## Resource Usage

| Service | RAM | CPU | Disk |
|---------|-----|-----|------|
| Code Search | ~150MB | <1% idle | ~50MB index per 100K chunks |
| Prompt Library | ~50MB | <1% idle | <1MB |
| Ollama (embedding model) | ~4GB | Spikes during indexing | ~4GB model |

Total: ~200MB for the services (Ollama runs independently and is shared with other tools).

## Why Not Just Grep?

Grep finds exact text matches. Code search finds **meaning**:

| Query | Grep finds | Code Search finds |
|-------|-----------|-------------------|
| "auth middleware" | Files containing "auth middleware" | `verifyToken()`, `checkSession()`, `requireAuth()` |
| "database pooling" | Files containing "database pooling" | `createPool()`, `getConnection()`, `pg.Pool` config |
| "error handling" | Files containing "error handling" | try/catch blocks, error middleware, custom Error classes |

The embeddings understand code semantics. That's the whole point.
