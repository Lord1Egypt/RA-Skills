---
name: memory-semantic-search
description: "Semantic search over workspace markdown files using embedding API + SQLite vector store. Use when: (1) searching workspace notes/memory by meaning rather than exact keywords, (2) finding related markdown content across files, (3) recalling past decisions, context, or notes semantically. Requires an OpenAI-compatible embedding API. NOT for: searching non-markdown files, web search, or code search."
---

# Memory Semantic Search

Standalone semantic search over workspace `.md` files. Uses an OpenAI-compatible embedding API and SQLite for vector storage. No external dependencies beyond Python 3 stdlib + the embedding API.

## Setup

Set these environment variables (or pass as CLI args):

```bash
export EMBEDDING_API_KEY="sk-xxx"
export EMBEDDING_API_BASE="https://api.openai.com/v1"   # any OpenAI-compatible endpoint
export EMBEDDING_MODEL="text-embedding-3-small"          # optional, this is the default
```

## Usage

### Index workspace

```bash
python3 scripts/index.py /path/to/workspace
```

Options:
- `--force` — full reindex (clear existing data)
- `--db PATH` — custom SQLite path (default: `memory_search.sqlite` in skill dir)
- `--api-base`, `--api-key`, `--model` — override env vars

Incremental: only new/changed chunks are embedded. Deleted files are cleaned up automatically.

### Search

```bash
python3 scripts/search.py "your query here"
```

Options:
- `--top-k N` — number of results (default: 5)
- `--min-score F` — minimum cosine similarity threshold (default: 0.3)
- `--json` — output as JSON
- `--db`, `--api-base`, `--api-key`, `--model` — same as index

### Typical agent workflow

1. Run `index.py` on the workspace (once, or after file changes)
2. Run `search.py "query"` to find relevant snippets
3. Use `read` tool to load full context from the returned file paths and line numbers
