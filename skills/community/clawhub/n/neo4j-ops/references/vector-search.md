# Vector & full-text search (verified live on 2026.10.2)

Extracted from the `neo4j` skill body 2026-11-16. Load when creating/querying vector or full-text indexes.

## Create (2026.01+ syntax — always set `vector.dimensions`; declare filterable props with `WITH`)

```cypher
CREATE VECTOR INDEX emb_idx IF NOT EXISTS FOR (n:Doc) ON n.embedding
WITH [n.category, n.year]
OPTIONS { indexConfig: { `vector.dimensions`: 1536, `vector.similarity_function`: 'cosine' } };
CREATE FULLTEXT INDEX doc_fts FOR (n:Doc) ON EACH [n.title, n.body];
```

- One vector property per node/relationship; multi-label OK (`FOR (n:Movie|Actor)`). `WITH` filter props must be scalar (INTEGER/FLOAT/STRING/BOOLEAN/DATE/...); missing or other types index as null.
- **Search indexes are NOT used automatically** — query them explicitly or they are just storage.

## Query — the `SEARCH` clause (preferred on 2026.x; vector 2026.01+, full-text 2026.09+)

```cypher
MATCH (n:Doc)
SEARCH n IN (VECTOR INDEX emb_idx FOR $qv WHERE n.category = $cat LIMIT 10) SCORE AS score
RETURN n.title, score ORDER BY score DESC;
MATCH (n:Doc) SEARCH n IN (FULLTEXT INDEX doc_fts FOR $term LIMIT 20) SCORE AS score RETURN n.title, score;
```

- `SEARCH` is a subclause of `MATCH`/`OPTIONAL MATCH`: vector = `FOR <vector expr> [WHERE ...] LIMIT top_k [SCORE AS s]`.
- `WHERE` INSIDE `SEARCH` = in-index filtering (efficient); `WHERE` on the MATCH = post-filter. In-index predicates only cover props declared via `WITH` at creation (verified: undeclared prop → `PropertyNotFound` 22ND3).
- Legacy (works, deprecated in 2026.x): `CALL db.index.vector.queryNodes('idx', k, $qv) YIELD node, score`, `CALL db.index.fulltext.queryNodes('idx', 'term') YIELD node, score`.
- Inline similarity (no index needed): `vector.similarity.cosine(a,b)`, `vector.similarity.euclidean(a,b)`, `vector_distance`, `vector_norm`, `vector_dimension_count`.
- Indexes build in the background: `SHOW INDEXES` state `POPULATING` → `ONLINE` (track `populationPercent`).
