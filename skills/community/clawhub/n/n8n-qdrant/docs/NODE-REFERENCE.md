# n8n Qdrant Node Reference

## Official Qdrant Node (`n8n-nodes-qdrant`)

Install via: n8n Settings → Community Nodes → `n8n-nodes-qdrant`

Compatible with Qdrant 1.14.0+

---

## Collection Operations

### Create Collection
**When to use**: First-time setup or automated provisioning before ingestion.

```json
{
  "resource": "collection",
  "operation": "createCollection",
  "collectionName": "my-collection",
  "vectorsConfig": {
    "size": 3072,
    "distance": "Cosine"
  }
}
```

**Vector sizes by model**:
| Model | Size |
|-------|------|
| text-embedding-3-large | 3072 |
| text-embedding-3-small | 1536 |
| text-embedding-ada-002 | 1536 |
| Gemini text-embedding-004 | 768 |
| nomic-embed-text | 768 |

**Distance metrics**:
- `Cosine` — Best for normalized text embeddings (most common)
- `Dot` — Use when vectors are not normalized (faster)
- `Euclid` — Use for geometric/spatial data

### Collection Exists
**When to use**: Guard before Create Collection in automated workflows.

```json
{
  "resource": "collection",
  "operation": "collectionExists",
  "collectionName": "={{ $json.collection_name }}"
}
```
Returns `{ exists: true/false }` — branch with IF node.

### List Collections
**When to use**: Audit, UI dropdowns, dynamic routing.

### Delete Collection
**When to use**: Full reset / re-ingestion. Always gate with approval workflow.

### Get Collection
**When to use**: Check vector count, config, status before operations.

---

## Point Operations

### Upsert Points
**When to use**: Raw ingestion when you pre-compute embeddings outside n8n, or need full control over payload structure.

```json
{
  "resource": "point",
  "operation": "upsertPoints",
  "collectionName": "my-collection",
  "points": [
    {
      "id": "={{ $json.point_id }}",
      "vector": "={{ $json.embedding }}",
      "payload": {
        "text": "={{ $json.chunk_text }}",
        "source_id": "={{ $json.source_id }}",
        "doc_id": "={{ $json.doc_id }}",
        "chunk_index": "={{ $json.chunk_index }}",
        "source_type": "slack",
        "created_at": "={{ $json.timestamp }}",
        "keywords": "={{ $json.keywords }}"
      }
    }
  ]
}
```

**ID formats**: UUID string or unsigned integer. Use UUID for distributed systems.

### Delete Points
**When to use**: Remove all chunks belonging to a document when source is updated or deleted.

```json
{
  "resource": "point",
  "operation": "deletePoints",
  "collectionName": "my-collection",
  "filter": {
    "must": [
      {
        "key": "doc_id",
        "match": { "value": "={{ $json.doc_id }}" }
      }
    ]
  }
}
```

**Filter operators**: `must` (AND), `should` (OR), `must_not` (NOT)
**Match types**: `match.value` (exact), `range` (numeric), `match.any` (array membership)

### Scroll Points
**When to use**: Iterate all points for export, audit, re-embedding, or bulk update.

```json
{
  "resource": "point",
  "operation": "scrollPoints",
  "collectionName": "my-collection",
  "limit": 100,
  "withPayload": true,
  "withVector": false,
  "filter": {
    "must": [{ "key": "source_type", "match": { "value": "slack" } }]
  }
}
```

Use `offset` parameter with Loop to paginate through full collection.

### Count Points
**When to use**: Check ingestion progress, collection health monitoring.

### Retrieve Points
**When to use**: Fetch specific points by ID for lookup, deduplication checks.

### Batch Update Points
**When to use**: High-throughput ingestion — combine multiple upsert/delete/payload operations in one API call. Reduces round trips significantly for bulk loads.

---

## Search Operations

### Query Points (Core search operation)
**When to use**: All retrieval — dense, sparse, or hybrid.

#### Dense (semantic) search
```json
{
  "resource": "search",
  "operation": "queryPoints",
  "collectionName": "my-collection",
  "query": "={{ $json.query_embedding }}",
  "limit": 10,
  "withPayload": true,
  "scoreThreshold": 0.7
}
```

#### Sparse (keyword/BM25) search
Requires collection created with sparse vector config. Uses keyword-frequency vectors.
```json
{
  "resource": "search",
  "operation": "queryPoints",
  "collectionName": "my-collection",
  "using": "sparse",
  "query": {
    "indices": [102, 5843, 921],
    "values": [0.82, 0.61, 0.44]
  },
  "limit": 10
}
```
Sparse vectors must be computed via a sparse encoder model (e.g. SPLADE, BM25). In n8n, use an HTTP Request node to call a sparse encoder API, or use Code node to compute BM25 weights.

#### Hybrid search (dense + sparse with RRF fusion)
```json
{
  "resource": "search",
  "operation": "queryPoints",
  "collectionName": "my-collection",
  "prefetch": [
    {
      "query": "={{ $json.dense_embedding }}",
      "using": "dense",
      "limit": 20
    },
    {
      "query": {
        "indices": "={{ $json.sparse_indices }}",
        "values": "={{ $json.sparse_values }}"
      },
      "using": "sparse",
      "limit": 20
    }
  ],
  "query": { "fusion": "rrf" },
  "limit": 10,
  "withPayload": true
}
```

#### Filtered search
Add `filter` to any search to narrow results:
```json
{
  "filter": {
    "must": [
      { "key": "source_type", "match": { "value": "slack" } },
      { "key": "created_at", "range": { "gte": "2024-01-01T00:00:00Z" } }
    ]
  }
}
```

### Query Points In Batch
**When to use**: When an AI agent needs to run multiple searches simultaneously (e.g. multiple sub-questions). More efficient than sequential calls.

### Query Points Groups
**When to use**: When you want top-K results per document (avoid returning 5 chunks from the same doc). Set `groupBy: "doc_id"`, `groupSize: 2`.

---

## Payload Operations

### Set Payload
**When to use**: Enrich existing points post-ingestion (e.g. add classification labels, tags).

### Create Payload Index
**When to use**: Speed up filtered searches. Create indexes on frequently-filtered fields.

```json
{
  "resource": "payload",
  "operation": "createPayloadIndex",
  "collectionName": "my-collection",
  "fieldName": "source_type",
  "fieldSchema": "keyword"
}
```

**Schema types**: `keyword`, `integer`, `float`, `bool`, `text`, `datetime`, `uuid`

Always index: `doc_id`, `source_id`, `source_type`, `created_at`, `chunk_index`

---

## LangChain Vector Store Node (`@n8n/n8n-nodes-langchain.vectorStoreQdrant`)

### Mode: insert
Receives documents from upstream Document Loaders/Text Splitters and upserts into Qdrant.

**Required sub-nodes**:
- Embeddings node (connected via `ai_embedding` port)
- Text Splitter (connected via `ai_textSplitter` port on the Data Loader)
- Data Loader (connected via `ai_document` port)

**Key settings**:
- `qdrantCollection`: collection name or expression
- `mode`: `insert`
- `options.metadata`: add custom metadata fields to every chunk

**Always set**:
- `onError: continueRegularOutput` — prevents failures from stopping the batch
- `retryOnFail: true` — retry transient errors
- `executeOnce: false` — process each item individually

### Mode: retrieve
Direct similarity search, returns documents. Used in pure chain workflows (no agent).

### Mode: retrieve-as-tool
Exposes the vector store as a callable tool for AI Agent nodes.

**Key settings**:
- `toolName`: snake_case name the LLM will reference (e.g. `slack_messages`)
- `toolDescription`: natural language description for the LLM
- `topK`: number of results to return (10–30 for most use cases)

**Required sub-node**: Embeddings node (same model used at ingest time)

---

## Embeddings Nodes

| Node | Model | Best For |
|------|-------|---------|
| OpenAI Embeddings | text-embedding-3-large (3072d) | Best quality, production default |
| OpenAI Embeddings | text-embedding-3-small (1536d) | Cost-efficient, good quality |
| Google Gemini Embeddings | text-embedding-004 (768d) | When Gemini is primary LLM |
| Ollama Embeddings | nomic-embed-text | Fully local, no API cost |

**Critical**: Use the **exact same embedding model** at ingest time and retrieval time. Mismatches produce nonsense results.

---

## Text Splitter Nodes

### Token Splitter (`@n8n/n8n-nodes-langchain.textSplitterTokenSplitter`)
Splits by token count. Most reliable for LLM context windows.

| Use Case | chunkSize | chunkOverlap |
|----------|-----------|--------------|
| Slack messages | 256–512 | 50 |
| Meeting transcripts | 1000–2000 | 200 |
| Documents/PDFs | 512–1500 | 100–200 |
| Code files | 512 | 100 |
| Short records | 128–256 | 25 |

### Recursive Character Splitter
Splits on natural boundaries (paragraphs → sentences → words). Better for structured prose.

**Rule**: chunk overlap should be 10–15% of chunk size.

---

## Information Extractor Node (`@n8n/n8n-nodes-langchain.informationExtractor`)
Use this to generate rich metadata from full document text before chunking.

**Pattern**:
1. Extract full document text (Extract From File node or HTTP response)
2. Run through Information Extractor with structured attributes
3. Store output, pass into Data Loader metadata fields
4. Then chunk + embed + ingest

See `docs/CHUNKING-METADATA.md` for full metadata schema templates.
