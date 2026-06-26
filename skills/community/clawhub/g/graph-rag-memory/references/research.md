# Research Foundations & Citations

This skill's architecture draws on several research threads, synthesized into a novel
multi-embedding retrieval system purpose-built for personal agent memory.

---

## Core Papers

### RouterRetriever — Expert Routing via Centroids
**Zhuang et al. (2025). "RouterRetriever: Exploring the Benefits of Routing over Multiple Expert Embedding Models." AAAI 2025.**
- arXiv: https://arxiv.org/abs/2409.02685

Key insight used: **Centroid-based routing outperforms learned classifier routing** for retrieval
tasks. Given domain-specialized embedding models, compute a centroid embedding for each domain
from sample documents, then route queries by cosine similarity to the nearest centroid.

This paper validated that you don't need a learned router (which requires training data and
adds complexity) — the geometric centroid of domain embeddings is a sufficient signal.

Our adaptation: Instead of LoRA adapters sharing a base encoder (RouterRetriever's setup),
we route between fully separate Ollama-hosted models. The centroid computation and routing
logic are structurally identical but applied across independent model endpoints.

---

### Graphiti — Temporal Knowledge Graph for Agents
**Rasmussen et al. (2024). "Graphiti: Temporally-Aware Knowledge Graphs for AI Agents."**
- GitHub: https://github.com/getzep/graphiti
- Blog: https://www.getzep.com/graphiti

Graphiti provides the temporal knowledge graph substrate: episode ingestion, entity/relationship
extraction (via LLM), bi-temporal edge validity, and hybrid BM25+vector search.

Our adaptation: We use Graphiti's `graphiti_search()` lower-level API to inject a
`query_vector` from our domain-routed expert embedder, bypassing Graphiti's default
single-model embedding with our MoE routing output.

---

### FalkorDB — Graph Database with Vector Index
**FalkorDB (2024). RedisGraph fork with extended vector and temporal query support.**
- GitHub: https://github.com/FalkorDB/FalkorDB

Used as the persistence and query layer. Key capabilities:
- Property graphs with Cypher query language
- FULLTEXT indexes on relationship properties (`fact`, `name`)
- VECTOR index on `fact_embedding` (768-dim cosine similarity)
- Fast in-memory execution with optional persistence

---

## Novel Contributions of This Implementation

The graph-rag-memory skill introduces several design decisions not present in existing
open-source memory systems:

### 1. MoE-Style Multi-Embedding Routing (Primary Novelty)
Most RAG systems use a single embedding model for all content. This system routes queries
and documents to **domain-specialized embedding experts** based on content type:

- `personal` / `episodic` → `nomic-embed-text` (768-dim, general conversation)
- `project` → `mxbai-embed-large` (1024-dim, structured/precise facts)
- `technical` → `nomic-embed-code` (768-dim, code and architecture)
- `research` → `specter2` (768-dim, scientific literature)

**Inspiration:** RouterRetriever's finding that domain-specialized embedders outperform
general embedders on domain-specific retrieval, even when the specialized model is smaller.

**Our extension:** Applied to personal agent memory domains (personal/episodic/project/technical/research/meta)
rather than academic IR benchmark domains. No specialist memory embedding models exist —
we repurpose code and scientific embedders for proxy domain separation.

### 2. Three-Stage Cascaded Routing
```
Hard routing (metadata)  →  Centroid routing (cosine)  →  Fanout + RRF
     confidence=1.0           confidence=delta≥0.02      low-confidence
```
Each stage adds compute but increases routing precision. Fanout runs parallel expert
queries and fuses results via Reciprocal Rank Fusion (RRF), gracefully handling
ambiguous queries that span multiple domains.

### 3. Temporal Knowledge Graph as Memory Substrate
Unlike flat vector stores (Chroma, Qdrant, pgvector) or key-value memory systems:
- Facts have **bi-temporal validity** (when they were true vs. when recorded)
- Entities are **deduplicated** across episodes (Jebadiah = same node across all sessions)
- **Relationship edges** carry semantic facts, not just document chunks
- **Graph traversal** enables connected reasoning (HostLink → Jebadiah → Telegram)

### 4. `query_vector` Passthrough Without Forking Graphiti
Graphiti's high-level `search()` API uses its configured embedder for query vectorization.
To inject our domain-routed expert vector, we drop to the lower-level `graphiti_search()`
which accepts an explicit `query_vector` parameter — letting us swap the embedding model
per-query without modifying Graphiti's source code.

This is the key leverage point identified during architecture design.

---

## Related Work

### Retrieval-Augmented Generation (RAG)
- Lewis et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." NeurIPS 2020.
- https://arxiv.org/abs/2005.11401

### Mixture of Experts
- Shazeer et al. (2017). "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer." ICLR 2017.
- https://arxiv.org/abs/1701.06538

### Reciprocal Rank Fusion
- Cormack et al. (2009). "Reciprocal Rank Fusion outperforms Condorcet and individual Rank Learning Methods." SIGIR 2009.

### Tri-Modal Fusion (reranking inspiration)
- Research showing smaller embeddings + LLM reranking often beats larger embeddings alone.
- Applied here: BM25 + cosine_similarity fused via RRF before optional cross-encoder reranking.

---

## Potential Future Improvements

1. **Specialized personal memory embedder** — No model currently exists for personal/episodic memory.
   Fine-tuning `nomic-embed-text` on conversation pairs would improve personal domain retrieval.

2. **Online centroid updates** — Currently centroids are batch-computed. Online updates (EMA)
   as new content arrives would adapt routing without full recomputation.

3. **Graphiti fork for multi-vector storage** — Currently all domains use a single 768-dim
   vector index (nomic space). A Graphiti fork adding per-domain vector fields and indexes
   would enable full MoE retrieval. `mxbai-embed-large` (1024-dim) can't currently be used
   for vector search without this fork.

4. **Community graph** — Graphiti's community detection groups related entities. Not yet
   enabled — would improve "summarize everything about HostLink" style queries.
