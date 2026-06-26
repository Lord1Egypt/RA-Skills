---
name: lightrag-memory
description: >-
  LightRAG-based semantic memory system for AI agents. Provides efficient long-term
  knowledge storage and retrieval using vector embeddings and knowledge graphs.
  Use when: (1) semantic search over agent memory files is needed, (2) reducing token
  usage by avoiding full-file re-reading, (3) building a knowledge graph from text
  documents, (4) querying memory with natural language instead of keyword matching.
  Supports naive, local, global, and hybrid query modes.
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["python3", "pip"],
            "env": ["OPENAI_API_KEY"],
          },
        "install":
          [
            {
              "id": "lightrag-memory-deps",
              "kind": "pip",
              "requirements": "requirements.txt",
              "label": "Install LightRAG dependencies",
            },
          ],
      },
  }
---

# LightRAG Memory

Semantic memory system with vector search + knowledge graph. Replaces reading entire
memory files on every request with targeted retrieval (~1-3K tokens vs 30K+).

## Quick Setup

```bash
cd skills/lightrag-memory
pip install -r requirements.txt
```

Set environment variables:

```bash
export OPENAI_API_KEY="your-key"
export OPENAI_BASE_URL="https://your-api-endpoint/v1"  # optional, defaults to OpenAI
```

Or create a `.env` file in the skill directory.

## Commands

### Index memory files

Index `MEMORY.md` and `memory/*.md` from workspace:

```bash
python3 scripts/rag.py index
```

### Insert content

```bash
# From file
python3 scripts/rag.py insert --file /path/to/file.md --source "filename"

# From text
python3 scripts/rag.py insert --text "Important fact" --source "manual"

# From stdin
echo "Some text" | python3 scripts/rag.py insert --source "stdin"
```

### Query

```bash
# Hybrid search (best results, costs more API calls)
python3 scripts/rag.py query "What do I know about the user?" --mode hybrid

# Local search (entities + relationships, balanced)
python3 scripts/rag.py query "What projects were discussed?" --mode local

# Naive search (simple vector lookup, cheapest)
python3 scripts/rag.py query "Any notes about deployment?" --mode naive

# Global search (broad context, expensive)
python3 scripts/rag.py query "Summarize everything" --mode global
```

## Query Modes

| Mode | What it searches | Cost | Best for |
|------|-----------------|------|----------|
| naive | Vector embeddings only | Lowest | Quick fact lookup |
| local | Entities + relationships | Low | Specific entities |
| global | Community-level context | High | Broad understanding |
| hybrid | Local + global | Highest | Comprehensive answers |

## Storage

Data stored in `~/.openclaw/workspace/lightrag_storage/` by default.
Override with `LIGHTARG_WORKING_DIR` env var.

## Integration Pattern

For agent memory systems, index files on change and query on demand:

```bash
# Check if reindex needed (files modified since last index)
find MEMORY.md memory/ -name '*.md' -newer memory/lightrag-last-index.txt

# Reindex if needed
python3 scripts/rag.py index
touch memory/lightrag-last-index.txt

# Query when context needed
python3 scripts/rag.py query "user preferences" --mode naive
```

## Architecture

- **Embeddings**: `text-embedding-3-small` (1536 dim) via OpenAI-compatible API
- **LLM**: `gpt-4o-mini` for entity extraction and answer generation
- **Storage**: JSON-based vector DB + GraphML knowledge graph
- **Batching**: 8 items per embedding batch, 4 concurrent async requests

## Troubleshooting

**OPENAI_API_KEY not set**: Ensure env vars are exported or `.env` exists.

**numpy RuntimeError (X86_V2)**: On older CPUs lacking AVX2, install `pip install "numpy<2.0"`.

**Slow first index**: Initial indexing processes all files. Subsequent updates are incremental.

**Reset storage**: `rm -rf <storage_dir>/* && python3 scripts/rag.py index`
