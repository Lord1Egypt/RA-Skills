---
name: hybrid-retrieval
description: Design and build a hybrid retrieval system combining BM25 keyword search, vector embeddings, and knowledge graph traversal for AI agent memory. Use when building agent memory, designing RAG systems, or improving recall quality. Triggers on "hybrid search", "RAG architecture", "agent memory design", "build memory system", "BM25 + vector", "knowledge graph search".
---

You are an expert in information retrieval systems, specifically hybrid approaches that combine multiple search paradigms. Help the user design and build a retrieval system inspired by the [BlackRock/NVIDIA HybridRAG paper](https://arxiv.org/abs/2408.04948).

## Core Insight

No single retrieval method works for everything:

| Method | Strength | Weakness |
|--------|----------|----------|
| **BM25 (keyword)** | Exact matches, names, IDs, codes | Misses synonyms and semantic meaning |
| **Vector (embedding)** | Semantic similarity, paraphrases | Struggles with exact terms, numbers, names |
| **Graph (knowledge graph)** | Relationships, multi-hop reasoning | Requires structured extraction, maintenance |

**The hybrid approach:** Run all three in parallel, then fuse results with weighted scoring. Each method catches what the others miss.

## Architecture Pattern

```
User Query
    │
    ├──→ BM25 Keyword Search (fastest, sub-ms)
    │         SQLite FTS5 or Elasticsearch
    │
    ├──→ Vector Search (fast, ~100ms)
    │         Embedding model → ANN index (Qdrant, Milvus, FAISS, sqlite-vec)
    │
    └──→ Graph Search (medium, ~200ms)
              Entity extraction → Graph DB traversal (Neo4j, etc.)
    │
    └──→ Fusion Layer
              Weighted merge → Deduplication → Reranking → Top-K results
```

## Step-by-Step Design

### Step 1: Choose Your Document Store

Your chunks need to live somewhere. Options:

- **SQLite + FTS5 + vec0** — Single file, zero infrastructure, good up to ~100K chunks
- **PostgreSQL + pgvector** — Production-ready, handles millions
- **Qdrant / Milvus** — Purpose-built vector DBs, best for scale
- **Elasticsearch** — If you already use it, it does BM25 + vector natively

**Recommendation for most projects:** Start with SQLite (FTS5 for keywords, vec0 for vectors). Migrate when you hit performance limits.

### Step 2: Choose Your Embedding Model

| Model | Dimensions | Quality | Speed | Cost |
|-------|-----------|---------|-------|------|
| OpenAI text-embedding-3-small | 1536 | Good | Fast | $0.02/1M tokens |
| Voyage AI voyage-3 | 1024 | Very good | Fast | $0.06/1M tokens |
| NV-Embed-v2 (self-hosted) | 4096 | Excellent | Medium | Free (GPU needed) |
| nomic-embed-text (Ollama) | 768 | Good | Fast | Free (CPU ok) |

**Key decision:** Self-hosted = free but needs GPU. Cloud = easy but recurring cost. For production agent memory, self-hosted pays for itself quickly.

### Step 3: Chunking Strategy

Bad chunking ruins everything. Rules:

1. **Chunk by semantic unit** — sections, paragraphs, conversations. NOT fixed-size windows.
2. **Include metadata** — file path, date, source type. You'll filter on this later.
3. **Overlap sparingly** — 10-20% overlap prevents losing context at boundaries.
4. **Keep chunks 200-600 tokens** — too small = no context, too large = noise.

### Step 4: BM25 Layer

```sql
-- SQLite FTS5 example
CREATE VIRTUAL TABLE chunks_fts USING fts5(path, text, source);

-- Search
SELECT path, text, rank
FROM chunks_fts
WHERE chunks_fts MATCH 'query terms'
ORDER BY rank
LIMIT 20;
```

BM25 handles: exact names, error codes, file paths, dates, IDs — anything where the exact string matters.

### Step 5: Vector Layer

```python
# Embed query
query_vec = embed("What is the deployment status?")

# ANN search (sqlite-vec example)
results = db.execute(
    "SELECT id, distance FROM chunks_vec "
    "WHERE embedding MATCH ? AND k = ? ORDER BY distance",
    (query_vec_blob, 20)
)
```

Vector handles: semantic questions, paraphrases, "find things related to X" — meaning over matching.

### Step 6: Graph Layer (Optional but Powerful)

```cypher
// Neo4j: Find entity and its connections
MATCH (n) WHERE n.name CONTAINS $entity
OPTIONAL MATCH (n)-[r]-(connected)
RETURN n, r, connected
ORDER BY coalesce(r.weight, 1.0) DESC
LIMIT 10
```

Graph handles: "Who works with X?", "What's related to Y?", multi-hop reasoning — relationships that flat search can't find.

### Step 7: Fusion

The critical part — merging results from all three methods:

```python
def fuse_results(bm25_results, vector_results, graph_results,
                 bm25_weight=0.3, vector_weight=0.5, graph_weight=0.8):
    all_results = {}

    for r in bm25_results:
        key = r["path"] + ":" + r["text"][:100]
        all_results[key] = {**r, "score": r["score"] * bm25_weight}

    for r in vector_results:
        key = r["path"] + ":" + r["text"][:100]
        if key in all_results:
            all_results[key]["score"] += r["score"] * vector_weight
        else:
            all_results[key] = {**r, "score": r["score"] * vector_weight}

    for r in graph_results:
        key = r["path"] + ":" + r["text"][:100]
        if key in all_results:
            all_results[key]["score"] += r["score"] * graph_weight
        else:
            all_results[key] = {**r, "score": r["score"] * graph_weight}

    return sorted(all_results.values(), key=lambda x: x["score"], reverse=True)
```

**Weight tuning:**
- Graph results get highest weight — if the KG found a relevant entity, it's almost certainly right
- Vector gets medium weight — good general recall
- BM25 gets lowest weight — precise but narrow

### Step 8: Deduplication and Reranking

After fusion:
1. **Deduplicate** by text content (not path — same file can have multiple relevant chunks)
2. **MMR reranking** (optional) — Maximal Marginal Relevance reduces redundancy by penalising results too similar to already-selected ones
3. **Score threshold** — drop anything below 0.3 (tune this for your data)

## Common Mistakes

1. **Using only vector search** — Misses exact matches. "Port 8034" won't match semantically.
2. **Fixed-size chunking** — Splitting mid-sentence destroys context.
3. **No graph layer** — You'll hit a ceiling where flat retrieval can't answer relationship questions.
4. **Reranking with the same model** — If you rerank with the same embeddings you searched with, you're just re-sorting the same biases.
5. **Ignoring BM25** — It's the fastest layer and catches what vectors miss. Always include it.

## When to Add Complexity

| If you have... | You need... |
|----------------|-------------|
| < 1K chunks | BM25 only (SQLite FTS5) |
| 1K - 50K chunks | BM25 + Vector |
| 50K+ chunks | BM25 + Vector + Graph |
| Multiple data sources (chats, emails, docs) | Separate collections with routing |
| Real-time requirements | Parallel search with timeouts |

## Output

Help the user:
1. Assess their data volume and types
2. Choose appropriate layers (BM25, vector, graph)
3. Select embedding model and storage backend
4. Design their chunking strategy
5. Implement fusion with appropriate weights
6. Set up a simple evaluation (test queries → expected results)

## Further Reading

- [BlackRock/NVIDIA HybridRAG Paper](https://arxiv.org/abs/2408.04948) — the research foundation
- [Qdrant](https://qdrant.tech/) — production vector DB
- [sqlite-vec](https://github.com/asg017/sqlite-vec) — lightweight vector search
- [Neo4j](https://neo4j.com/) — graph database for knowledge graphs
