---
name: pgvector
description: "PostgreSQL vector database skill with pgvector extension. Enables vector similarity search, embeddings storage, RAG (Retrieval-Augmented Generation) pipelines, and hybrid search combining vector and keyword search. Use when: storing/retrieving embeddings, building AI applications with vector search, implementing RAG, similarity matching, semantic search, or any use case requiring vector database functionality."
metadata:
  {
    "openclaw": { "emoji": "🔢" },
    "version": "1.0.0",
  }
---

# pgvector Skill

PostgreSQL + pgvector extension for vector similarity search.

## Quick Connect

```bash
# Connect to pgvector database (default port 5433)
psql -h localhost -p 5433 -U damien -d postgres

# Or use environment variables
export PGHOST=localhost
export PGPORT=5433
export PGUSER=damien
export PGPASSWORD=''
export PGDATABASE=postgres
```

## Environment

- **Host**: localhost
- **Port**: 5433
- **User**: damien
- **Password**: (empty)
- **Database**: postgres

## Core Capabilities

### 1. Create Vector Table

```sql
-- Basic vector table (1536 dimensions for OpenAI embeddings)
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create HNSW index for fast similarity search
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Or use IVFFlat index (faster build, slower search)
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### 2. Insert Embeddings

```sql
-- Manual insert (replace with actual embedding)
INSERT INTO documents (content, embedding)
VALUES ('Your text here', '[0.1, 0.2, ..., 0.1536]');

-- With metadata
INSERT INTO documents (content, embedding, metadata)
VALUES (
    'AI is transforming technology',
    '[0.1, 0.3, ..., 0.5]',
    '{"source": "article", "author": "John"}'::jsonb
);
```

### 3. Vector Similarity Search

```sql
-- Cosine similarity (most common)
SELECT id, content, (1 - (embedding <=> '[query_embedding]')) AS similarity
FROM documents
ORDER BY embedding <=> '[query_embedding]'
LIMIT 5;

-- Euclidean distance
SELECT id, content, (embedding <-> '[query_embedding]') AS distance
FROM documents
ORDER BY embedding <-> '[query_embedding]'
LIMIT 5;

-- Inner product (for normalized vectors)
SELECT id, content, (embedding <#> '[query_embedding]') AS similarity
FROM documents
ORDER BY embedding <#> '[query_embedding]'
LIMIT 5;
```

### 4. Hybrid Search (Vector + Keyword)

```sql
-- Combine vector search with full-text search
SELECT id, content,
    (1 - (embedding <=> '[query_embedding]')) AS vector_score,
    ts_rank(to_tsvector('english', content), plainto_tsquery('english', 'search terms')) AS text_score
FROM documents
WHERE content ILIKE '%search terms%'
ORDER BY (vector_score * 0.7 + text_score * 0.3) DESC
LIMIT 10;
```

### 5. RAG Pipeline Example

```sql
-- Store document chunks with embeddings
CREATE TABLE document_chunks (
    id BIGSERIAL PRIMARY KEY,
    document_id BIGINT REFERENCES documents(id),
    chunk_text TEXT NOT NULL,
    chunk_embedding vector(1536) NOT NULL,
    chunk_index INT NOT NULL
);

-- Retrieve relevant chunks for LLM context
SELECT chunk_text
FROM document_chunks
WHERE document_id = ?
ORDER BY chunk_embedding <=> '[question_embedding]'
LIMIT 5;
```

## Management Commands

### Check pgvector Extension

```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

### Table Info

```sql
-- List all tables with vectors
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Check index sizes
SELECT pg_size_pretty(pg_total_relation_size('documents'));
```

### Monitoring

```sql
-- Check query performance
EXPLAIN ANALYZE
SELECT * FROM documents
ORDER BY embedding <=> '[query_embedding]'
LIMIT 5;

-- Index usage stats
SELECT * FROM pg_stat_user_indexes
WHERE indexname LIKE '%embedding%';
```

## Common Operations

### Update Embedding

```sql
UPDATE documents
SET embedding = '[new_embedding]'
WHERE id = 1;
```

### Delete

```sql
DELETE FROM documents WHERE id = 1;
```

### Batch Insert (Python)

```python
import psycopg2
import numpy as np

conn = psycopg2.connect(
    host="localhost",
    port=5433,
    user="damien",
    password="",
    database="postgres"
)

cur = conn.cursor()
for text, embedding in documents:
    cur.execute(
        "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
        (text, embedding.tolist())
    )
conn.commit()
```

## Distance Operators

| Operator | Description |
|----------|-------------|
| `<->` | Euclidean distance |
| `<=>` | Cosine distance |
| `<#>` | Inner product |
| `<=>` | Cosine distance (1 - cosine_similarity) |

## Use Cases

1. **Semantic Search** - Find documents by meaning, not keywords
2. **RAG** - Retrieve relevant context for LLM prompts  
3. **Recommendations** - Find similar items/products
4. **Anomaly Detection** - Find outliers in embeddings
5. **Image/Video Search** - Store and query visual embeddings

## Notes

- Vector dimensions must match your embedding model
- HNSW is better for accuracy, IVFFlat better for large datasets
- Normalize vectors for cosine similarity
- pgvector supports up to 16,000 dimensions
