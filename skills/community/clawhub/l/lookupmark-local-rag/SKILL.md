---
name: local-rag
description: >
    Semantic search over local files using all-MiniLM-L6-v2 embeddings and
    ms-marco-MiniLM-L-6-v2 cross-encoder reranking with ChromaDB and
    parent-child chunking. Optimized for low-RAM ARM devices (Raspberry Pi).
    Use when the user asks questions about their documents, wants to find
    information in their files without specifying exact paths, or needs to
    search across PDFs, DOCX, TXT, MD, TEX files.
    Triggers on "cerca nei miei file", "find in my files", "search documents",
    "trova nel computer", "what does my thesis say about", "search notes".
    NOT for exact file path requests, web search, or sending files.
---

# Local RAG

Semantic search over indexed local files with parent-child chunking for precise retrieval with full context.

## Architecture

| Component | Model | Size |
|-----------|-------|------|
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` | ~80MB |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` | ~80MB |
| Vector DB | ChromaDB (persistent, cosine similarity, HNSW) | varies |
| Chunking | Parent-child | — |

**Memory strategy**: Embedding model loaded first → freed with `gc.collect()` → reranker loaded → freed after scoring. This keeps peak RAM ~400MB on ARM.

## Chunking Strategy

- **Child chunks**: 128 words, 24 overlap → embedded for semantic search
- **Parent chunks**: 768 words → stored as full context, returned to user
- When a child matches → its parent is returned, giving surrounding context

## Running

All scripts must use the venv Python:

```bash
VENV=~/.local/share/local-rag/venv/bin/python
```

### Indexing

```bash
# Incremental index (default — skips unchanged files via SHA-256 hash)
$VENV ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/index.py

# Re-index from scratch
$VENV ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/index.py --reindex

# Custom paths
$VENV ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/index.py --paths ~/Documenti ~/Progetti

# Batch indexing (per-subfolder with git checkpoints, for low-RAM systems)
bash ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/index-batch.sh
```

### Querying

```bash
# Basic query
$VENV ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/query.py "what are the termination clauses?"

# More results
$VENV ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/query.py "Falcon LLM" --top-k 30 --top-n 5

# JSON output for programmatic use
$VENV ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/query.py "transformer architecture" --json

# With timeout
$VENV ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/query.py "deep learning" --timeout 60
```

Options:
- `--top-k N` — Child candidates from vector search (default: 20)
- `--top-n N` — Final parent results after reranking (default: 3)
- `--json` — JSON output
- `--timeout N` — Max seconds per query (default: 120)

### Monitoring

```bash
$VENV ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/monitor.py              # Status
$VENV ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/monitor.py --watch      # Auto-refresh
$VENV ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/monitor.py --log        # Logs
$VENV ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/monitor.py --errors     # Errors only
$VENV ~/.openclaw/workspace/skills/lookupmark-local-rag/scripts/monitor.py --git        # Git checkpoints
```

## Supported Formats

**Documents only** (no code files):
- Text: `.txt`, `.md`, `.csv`, `.json`, `.yaml`, `.yml`, `.toml`, `.tex`, `.bib`
- Documents: `.pdf` (pdfminer.six), `.docx` (python-docx), `.pptx`

**Excluded**: `.py`, `.js`, `.sh`, `.ipynb`, `.html`, `.css` and all code files.

## Limits (for 4GB ARM)

- PDF max size: 5MB (larger PDFs cause OOM with pdfminer)
- Max file size: 30MB
- Embedding batch size: 1 (conservative)
- Excluded dirs: `.git`, `.venv`, `node_modules`, `__pycache__`, `labs`, `exercises`, `src`, `scripts`, `ablation`, `test*`, `fixtures`

## Storage

| Path | Purpose |
|------|---------|
| `~/.local/share/local-rag/chromadb/` | ChromaDB data (git repo for rollback) |
| `~/.local/share/local-rag/venv/` | Python venv with dependencies |
| `~/.local/share/local-rag/index.lock` | Prevents concurrent indexing |
| `~/.local/share/local-rag/index-batch.log` | Batch indexing log |
| `~/.local/share/local-rag/queries.log` | Query history log |

## Security

- **ALLOWED_ROOTS**: Only `~/Documenti/github/thesis`, `~/Documenti/github/polito`, `~/Documenti`, `~/Scaricati`
- **BLOCKED_PATTERNS**: `.ssh`, `.gnupg`, `.env`, `credentials`, `tokens`, `.config/openclaw`
- Credentials directory is blacklisted — never indexed

## Workflow

1. Run `index.py` — builds/rebuilds the index (incremental via SHA-256 hash check)
2. Run periodically to pick up new/changed files (daily cron recommended)
3. Use `query.py` to search with natural language
4. Results include: file path, relevance score, matched snippet, full parent context
5. Check `monitor.py` for stats and `queries.log` for query history
