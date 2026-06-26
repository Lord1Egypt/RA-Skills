---
name: graph-rag-memory
description: >
  Graph-RAG memory system using Graphiti temporal knowledge graph + FalkorDB + local Ollama
  embeddings. Provides persistent, queryable long-term memory for OpenClaw agents via a
  MoE-style (Mixture-of-Experts) multi-embedding router. Use when: setting up persistent
  agent memory, querying past conversations or facts, ingesting documents into the memory
  graph, checking memory system status, or integrating graph-rag memory into an OpenClaw
  agent. Triggers on: "memory system", "graph rag", "graphiti", "persistent memory",
  "ingest memory", "query memory", "what do you remember", "memory upgrade".
---

# Graph-RAG Memory Skill

Persistent, queryable agent memory via a temporal knowledge graph. Facts are extracted from
episodes (conversations, documents, notes), stored as typed entities and relationships in
FalkorDB, and retrieved via hybrid BM25 + cosine similarity search with domain-expert routing.

## Architecture Overview

```
Write path:  content → DomainRouter → expert embedder → Graphiti.add_episode()
                                             ↓
                                      FalkorDB (workspace graph)
                                      39+ nodes, 73+ RELATES_TO edges
                                      fact_embedding: 768-dim cosine index

Read path:   query → DomainRouter → expert embedder → query_vector
                                             ↓
                                    graphiti_search() [BM25 + cosine RRF]
                                             ↓
                                    ranked EntityEdge objects with .fact
```

**Routing layers:**
1. Hard routing (metadata/source_type → domain, confidence=1.0)
2. Centroid routing (cosine similarity to domain centroids, threshold=0.02)
3. Fanout fallback (parallel expert queries + RRF fusion)

**Domains:** `personal`, `episodic`, `project`, `technical`, `research`, `meta`, `general`

## Prerequisites

See `references/setup.md` for full installation and environment details.

**Quick check:**
```python
# Verify services (write to a temp script, don't use python3 -c inline)
import falkordb, httpx
r = falkordb.FalkorDB(host='172.18.0.1', port=6379)
print("FalkorDB OK:", r.list_graphs())
# nomic-embed-text must be loaded on NVIDIA Ollama
```

**Python packages** (reinstall after container restart — ephemeral layer):
```bash
export PATH=$PATH:/home/node/.local/bin
curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
python3 /tmp/get-pip.py --user --break-system-packages
pip3 install --user --break-system-packages graphiti-core falkordb sentence-transformers
```

## File Layout

All skill scripts live at: `memory-upgrade/` (workspace root)

```
memory-upgrade/
  config.py             # Service URLs + model names
  embedder.py           # OllamaEmbedderClient + expert registry
  router.py             # DomainRouter (hard + centroid + fanout)
  setup_graphiti.py     # Graphiti factory (defaults to 'workspace' graph)
  write_path.py         # ingest_memory(), ingest_workspace_memories()
  read_path.py          # query_memory() — hybrid BM25+vector
  phase3_ingest.py      # Seed ingestion (checkpoint-aware, re-runnable)
  phase4_query_test.py  # Read path validation (7 test queries)
  phase6_full_ingest.py # Full workspace ingestion + centroid recalibration
  checkpoints/          # Phase state (JSON, safe to re-run)
  scripts/              # Skill scripts (install, ingest, query, status)
```

## Common Tasks

### Query memory
```python
# Write to a .py file, then run it
import asyncio, sys
sys.path.insert(0, '/path/to/memory-upgrade')
from setup_graphiti import init_graphiti
from read_path import query_memory
from router import DomainRouter

async def main():
    g = await init_graphiti("workspace")
    router = DomainRouter(ollama_base_url="http://172.18.0.1:11436")
    edges, routing = await query_memory(g, router, "your question here",
                                         group_ids=["workspace"], limit=5)
    for e in edges:
        print(e.fact)
    await g.close()

asyncio.run(main())
```

Or use the convenience script:
```bash
python3 memory-upgrade/scripts/query_memory.py "your question here"
```

### Ingest new content
```bash
python3 memory-upgrade/scripts/ingest.py --file path/to/file.md --domain project
python3 memory-upgrade/scripts/ingest.py --text "Jebadiah decided X because Y" --domain personal
```

### Check system status
```bash
python3 memory-upgrade/scripts/status.py
```

### Re-seed from workspace memory files
```bash
python3 memory-upgrade/phase3_ingest.py    # daily notes + MEMORY.md
python3 memory-upgrade/phase6_full_ingest.py  # broader workspace docs
```

## Configuration

Edit `memory-upgrade/config.py` to change endpoints or models:

```python
OLLAMA_URL     = "http://172.18.0.1:11436"   # NVIDIA — embeddings
AMD_OLLAMA_URL = "http://172.18.0.1:11437"   # AMD — LLM (gemma4:e4b)
LLM_MODEL      = "gemma4:e4b"                # entity extraction LLM
EMBED_GENERAL  = "nomic-embed-text"          # 768-dim general embedder
```

## Known Gotchas

- **Data graph name = group_id**: Graphiti names the FalkorDB graph after the `group_id`
  passed to `add_episode()`. Always use `group_id="workspace"` and `init_graphiti("workspace")`.
- **sim_min_score must be 0.0**: The default 0.6 blocks almost all results. Always set to 0.0.
- **No `python3 -c` inline**: OpenClaw's obfuscation detector fires on it. Write to a temp file.
- **Packages reinstall needed**: `/home/node/.local` is ephemeral. Re-run pip install after restart.
- **Vector index**: Created in Phase 5. If the workspace graph is reset, re-run `phase5_vector_index.py`.

## Research Foundations

See `references/research.md` for full citations. Key papers:
- RouterRetriever (Zhuang et al., AAAI 2025) — centroid-based expert routing
- Graphiti (Rasmussen et al., 2024) — temporal knowledge graph for agents
- MoE routing literature — confidence thresholding + fanout fusion

## ClawHub Publishing

See `references/clawhub.md` for packaging and publishing instructions.
