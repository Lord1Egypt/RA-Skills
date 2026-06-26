---
name: super-github
description: "AI-Native GitHub Assistant powered by Embedder+Qdrant+LLM architecture. Index repos, semantic search across issues/PRs/code, proactive monitoring with Feishu alerts. Use when: (1) natural language GitHub queries, (2) tracking issues/PRs/CI across repos, (3) monitoring repos for bugs/keywords, (4) finding related issues without keyword matching."
---

# 🦞 Super GitHub — AI-Native GitHub Assistant

> Powered by the same Embedder + Qdrant + LLM architecture as elite memory systems.
> Index repos, search semantically, monitor proactively — all with natural language.

## Architecture

```
Query → [LLM: understand intent] → [Embedder: vectorize] → [Qdrant: semantic search] → [gh CLI: act]
```

Three-layer system (same as production memory pipelines):

| Layer | Component | Role |
|-------|-----------|------|
| **Embedder** | Ollama `nomic-embed-text` | Converts text → 768-dim vectors |
| **Vector Store** | Qdrant (local) | Stores & searches vectors by similarity |
| **Action Layer** | `gh` CLI | Executes GitHub operations |

## Prerequisites

- `gh` CLI authenticated (`gh auth status`)
- Ollama running with `nomic-embed-text:latest`
- Qdrant running at `localhost:6333`

## Quick Start

```bash
# 1. Initialize Qdrant collection
python scripts/github_indexer.py init

# 2. Index a repo
python scripts/github_indexer.py add owner/repo --all

# 3. Search with natural language
python scripts/github_search.py "memory search failing in agent" --limit 10

# 4. Monitor for keywords
python scripts/github_monitor.py watch owner/repo --events issues,ci --keywords bug,broken,urgent
```

## Scripts

| Script | Purpose |
|--------|---------|
| `github_indexer.py` | Index repos (issues, PRs, metadata) into Qdrant |
| `github_search.py` | Natural language semantic search |
| `github_monitor.py` | Proactive monitoring with keyword alerts |

## Detailed Commands

### Index (github_indexer.py)

```bash
python github_indexer.py init                    # Create Qdrant collection
python github_indexer.py add owner/repo --all     # Index everything
python github_indexer.py add owner/repo --issues # Issues only
python github_indexer.py add owner/repo --prs    # PRs only
python github_indexer.py add owner/repo --repo   # Repo metadata
python github_indexer.py status                   # Show indexed data
python github_indexer.py rm owner/repo           # Remove from index
```

### Search (github_search.py)

```bash
python github_search.py "query"                            # Search all
python github_search.py "query" --repo owner/repo         # Filter by repo
python github_search.py "query" --type issue              # Filter by type
python github_search.py "query" --limit 20               # More results
python github_search.py "query" --repo owner/repo --ci    # Show CI runs
```

### Monitor (github_monitor.py)

```bash
python github_monitor.py watch owner/repo                  # Start watching
python github_monitor.py watch owner/repo --events issues,ci
python github_monitor.py status                            # Show watches
python github_monitor.py check                            # Run checks
python github_monitor.py unwatch owner/repo               # Stop watching
```

## Memory System Analogy

| Component | GitHub Skill | Memory System |
|-----------|-------------|---------------|
| Data | Issues, PRs, code | Conversations |
| Embedder | nomic-embed-text | nomic-embed-text |
| Vector Store | Qdrant | Qdrant |
| Add | github_indexer.py | mem0 add |
| Search | github_search.py | mem0 search |

## Why Vector Search vs Keyword?

| Approach | "memory problems" query |
|----------|--------------------------|
| Keyword | Exact match only |
| **Vector (this)** | "memory leak", "OOM", "out of memory" |

## Setup Checklist

- [ ] `gh auth login` — authenticate GitHub CLI
- [ ] `ollama pull nomic-embed-text:latest` — download embedder
- [ ] Start Qdrant: `qdrant --storage-path ./qdrant-data`
- [ ] `python github_indexer.py init` — create collection
