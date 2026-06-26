# Collection Setup & Management Workflows

## One-Time Collection Provisioning Workflow

Run this ONCE before starting any ingestion. Idempotent — safe to re-run.

```
[Manual Trigger]
    → [Set: collection config]
    → [Qdrant: Collection Exists?]
    → [IF: exists == false]
         → [Qdrant: Create Collection]
         → [Create 5 Payload Indexes in parallel]
              - doc_id (keyword)
              - source_type (keyword)  
              - source_context (keyword)
              - created_at (datetime)
              - author (keyword)
         → [Notification: "Collection ready"]
    → [IF: exists == true]
         → [Notification: "Collection already exists, skipping"]
```

## Collection Config Reference

### Dense-Only Collection (Simple Setup)
Best for: single-language text, when you don't need keyword precision
```json
{
  "vectors": {
    "size": 3072,
    "distance": "Cosine",
    "on_disk": false,
    "hnsw_config": {
      "m": 16,
      "ef_construct": 100
    }
  },
  "optimizers_config": {
    "default_segment_number": 5
  }
}
```

### Hybrid Collection (Dense + Sparse)
Best for: production, mixed content, technical terminology
```json
{
  "vectors": {
    "dense": {
      "size": 3072,
      "distance": "Cosine"
    }
  },
  "sparse_vectors": {
    "sparse": {
      "index": {
        "on_disk": false,
        "full_scan_threshold": 5000
      }
    }
  }
}
```

### Multi-Vector Collection (Dense + Small Dense)
Best for: when you want fast approximate search + precise rerank
```json
{
  "vectors": {
    "dense-large": { "size": 3072, "distance": "Cosine" },
    "dense-small": { "size": 1536, "distance": "Cosine" }
  }
}
```

## Payload Index Creation (Official Qdrant Node)

Run after collection creation. Each is a separate node execution:

```json
[
  { "fieldName": "doc_id", "fieldSchema": "keyword" },
  { "fieldName": "source_type", "fieldSchema": "keyword" },
  { "fieldName": "source_context", "fieldSchema": "keyword" },
  { "fieldName": "created_at", "fieldSchema": "datetime" },
  { "fieldName": "author", "fieldSchema": "keyword" },
  { "fieldName": "chunk_index", "fieldSchema": "integer" },
  { "fieldName": "meta_topics", "fieldSchema": "keyword" },
  { "fieldName": "meta_sentiment", "fieldSchema": "keyword" }
]
```

## Collection Health Check Workflow

Use on schedule (daily) to monitor collection state:

```
[Schedule: daily]
    → [Qdrant: Get Collection]
    → [Code: parse stats]
    → [IF: vector_count > expected_minimum]
         → [Notification: "✅ Collection healthy: X vectors"]
    → [IF: status != "green"]
         → [Alert: "⚠️ Collection status: {{ $json.status }}"]
```

Parse from Get Collection response:
- `result.vectors_count` — total vector count
- `result.status` — `green`, `yellow`, `red`
- `result.optimizer_status` — optimization state

## Backup / Export Workflow

Periodically export collection for backup:

```
[Schedule: weekly]
    → [Qdrant: Scroll Points, limit=100, withPayload=true]
    → [Loop until offset is null]
    → [Aggregate: collect all points]
    → [Google Drive: Write JSON backup file]
```

Scroll pagination pattern:
```javascript
// Code node: handle scroll pagination
const response = $input.first().json;
const points = response.result?.points || [];
const nextOffset = response.result?.next_page_offset;

return [{
  json: {
    points,
    next_offset: nextOffset,
    has_more: nextOffset !== null
  }
}];
```

Connect `has_more == true` back to Scroll Points with `offset: ={{ $json.next_offset }}`.
