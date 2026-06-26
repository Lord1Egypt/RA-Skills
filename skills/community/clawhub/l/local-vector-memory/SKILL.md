---
name: local-vector-memory
description: Local vector memory with Ollama embeddings + Qdrant. Use when storing, searching, or managing local vector-based memories without cloud APIs. Supports Chinese and English text. Zero cloud dependency. Triggers: vector memory, local embedding, semantic search, memory storage, qdrant, ollama embedding, local RAG.
---

# Local Vector Memory Skill

Zero-cloud vector memory using Ollama embeddings + Qdrant local storage.

## Prerequisites

```bash
# Ollama with embedding model
ollama pull qwen3-embedding:4b

# Install the package
pip install local-vector-memory
```

## Quick Reference

```bash
lvm init                    # Initialize database
lvm add "text to remember"  # Store a memory
lvm search "query"          # Semantic search
lvm search "query" --limit 3 --json  # Structured output
lvm stats                   # Show stats
lvm reindex --dir ~/notes   # Reindex markdown files
lvm delete "source_name"    # Delete by source
```

## Python Library Usage

```python
from local_vector_memory.core import LocalVectorMemory

lvm = LocalVectorMemory()  # uses env defaults
lvm.add("OpenClaw baseUrl must not end with /v1")
results = lvm.search("how to configure ollama")
for r in results:
    print(f"[{r['score']}] {r['source']}: {r['text'][:100]}")
```

## Configuration

| Env Var | Default | Description |
|---------|---------|-------------|
| `LVM_OLLAMA_URL` | `http://localhost:11434` | Must be localhost (SSRF protected) |
| `LVM_MODEL` | `qwen3-embedding:4b` | Embedding model |
| `LVM_DIMS` | `2560` | Vector dimensions |
| `LVM_DB_PATH` | `~/.local-vector-memory/qdrant` | Storage path |
| `LVM_CHUNK_SIZE` | `400` | Chunk size in chars |
| `LVM_CHUNK_OVERLAP` | `50` | Overlap between chunks |

## Embedding Model Selection

| Model | Dims | Size | Chinese Hit Rate | Best For |
|-------|------|------|-----------------|----------|
| `qwen3-embedding:4b` | 2560 | ~2.5GB | **100%** | Chinese/English mixed |
| `bge-m3` | 1024 | ~570MB | 40% | Multilingual, low RAM |
| `nomic-embed-text` | 768 | 274MB | 30% | English-only, minimal RAM |

## Integration Patterns

### With OpenClaw

Add to HEARTBEAT.md or cron for periodic reindexing:
```bash
lvm reindex --dir ~/.openclaw/workspace/memory
```

### As a backup search layer

When `memory_search` doesn't find what you need:
```bash
lvm search "query" --json
```

## Security

- Ollama URL restricted to localhost only (SSRF protection)
- Path traversal blocked in reindex glob patterns
- Input length limits enforced (100K text, 10K query)
- All data stored locally, no network calls except to local Ollama

## Links

- PyPI: https://pypi.org/project/local-vector-memory/
- GitHub: https://github.com/JanCong/local-vector-memory
