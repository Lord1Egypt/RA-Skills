# milvus-skill

An agent skill that teaches LLMs how to use [pymilvus](https://github.com/milvus-io/pymilvus) to operate [Milvus](https://milvus.io/) vector database.

## What's Included

- **SKILL.md** — Main skill definition with connection, collection management, vector operations, and index management
- **references/** — Detailed reference docs for each feature area:
  - `collection.md` — Data types, schema fields, collection operations
  - `vector.md` — Insert, search, hybrid search, full-text search, iterators, filters
  - `index.md` — Index types, metric types, create/manage indexes
  - `partition.md` — Partition CRUD
  - `database.md` — Database management
  - `user-role.md` — RBAC: users, roles, privileges
  - `patterns.md` — Common patterns (RAG, semantic search, hybrid search, full-text search)

## Install as Claude Code Skill

```bash
claude skill add --url https://github.com/zilliztech/milvus-skill
```

## Capabilities

- Connect to Milvus Lite, Standalone, Cluster, or Zilliz Cloud
- Create collections with quick or custom schemas
- Insert, upsert, search, query, get, delete vectors
- Hybrid search with RRF/Weighted reranking
- Full-text search with BM25
- Paginated iteration over large result sets
- Index management (AUTOINDEX, HNSW, IVF_FLAT, etc.)
- Partition, database, and RBAC management

## Requirements

- Python 3.8+
- `pymilvus` (`pip install pymilvus`)
