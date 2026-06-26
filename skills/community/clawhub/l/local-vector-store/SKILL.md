---
name: local-vector-store
description: Implements semantic search using local vector embeddings for knowledge base indexing and similarity matching. Use when you need to search documents by meaning rather than keywords, or build a searchable knowledge base.
---

# Local Vector Store

A lightweight semantic search engine that indexes documents as vectors and enables similarity-based retrieval without external APIs.

## Features

- Document indexing with vector embeddings
- Semantic similarity search
- Local storage (no external dependencies)
- Batch indexing support
- Configurable embedding dimensions
- Cosine similarity matching

## Usage

```javascript
const vectorStore = require('./local-vector-store');

// Initialize store
const store = await vectorStore.create({
  dimension: 384,
  storePath: '/tmp/vector-store'
});

// Index documents
await store.index({
  id: 'doc1',
  content: 'Machine learning is a subset of artificial intelligence',
  metadata: { source: 'wiki' }
});

// Search by semantic similarity
const results = await store.search({
  query: 'AI and deep learning',
  topK: 5,
  threshold: 0.7
});

// Batch operations
await store.indexBatch([
  { id: 'doc2', content: 'Neural networks process data' },
  { id: 'doc3', content: 'Algorithms solve computational problems' }
]);
```

## Configuration

Set environment variables:
- `VECTOR_DIMENSION`: Embedding dimension (default: 384)
- `STORE_PATH`: Local storage directory (default: /tmp/vector-store)
- `SIMILARITY_THRESHOLD`: Minimum similarity score (default: 0.5)

## Output Format

```json
{
  "query": "semantic search",
  "results": [
    {
      "id": "doc1",
      "content": "...",
      "similarity": 0.92,
      "metadata": {}
    }
  ],
  "searchTime": 45
}
```
