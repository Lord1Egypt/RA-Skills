# Backend Storage Evaluation: SQLite vs FalkorDB

> **Updated 2026-05-07 — FalkorDB is the live backend.** The original v1 plan evaluated SQLite; in practice FalkorDB was chosen from day one and has been running since. This doc captures the tradeoffs for historical reference.

## Evaluation Context

- **Requirement**: Queryable store for ~6500 document chunks from ~380 documents across 8 projects
- **Constraints**: Zero infrastructure tax, sub-second queries, must work at session warmup
- **Our expertise**: Deep FalkorDB knowledge from Cruising Intelligence (57 clan nodes, 1K+ CABIN_FIT edges, 9-pass Cypher projections)

## SQLite

**Setup**: `import sqlite3` — stdlib, always available
**Memory**: File on disk, ~5MB for the full corpus
**Startup**: Instant
**Query**: Simhash distance + TF-IDF ranking — approximate semantic search
**Portability**: Any machine with Python 3.9+
**Durability**: ACID, survives crashes

**The tradeoff**: No graph traversal. "Show me the dependency chain from concept X" requires multiple queries and client-side join logic. Simhash is less accurate than embeddings for paraphrased queries.

## FalkorDB (chosen)

**Setup**: `docker run falkordb/falkordb:latest` + `pip install falkordb==1.6.1`
**Memory**: ~200MB RSS idle, Docker volume for persistence
**Startup**: ~1s (container running) or ~3s on cold start
**Query**: Cypher CONTAINS (fast primary filter) + TF-IDF re-ranking (relevance scoring)
**Portability**: Requires Docker on the host machine. Not available on Railway workers or machines without Docker.
**Durability**: Docker volume (`-v knowledge-graph-data:/data`) — survival across restarts, full purge via `docker volume rm`

**Why FalkorDB won:**
- **Cypher CONTAINS** — exact-match primary filter is faster and more predictable than simhash for our use case
- **Native graph model** — cross-project queries are `MATCH (c:Chunk {project:'MyApp'}) RETURN c`, no JOINs needed
- **Schema-free** — add new node types and edges on the fly without migrations
- **Deep expertise** — we already know FalkorDB well from CI's production pipeline
- **No API calls** — zero LLM embeddings, no external services, entirely local
- **Sub-second queries** — even with 6500+ chunks, results return in <100ms

## Migration Notes

If someone wants to migrate from SQLite to FalkorDB (or vice versa):
- The indexer produces the same chunked data regardless of backend — just swap the `MERGE`/`INSERT`
- Both stores use content-hash-based change detection for incremental indexing
- FalkorDB uses `CONTAINS` as primary filter (case-sensitive); SQLite depends on simhash (fuzzy but imprecise)
