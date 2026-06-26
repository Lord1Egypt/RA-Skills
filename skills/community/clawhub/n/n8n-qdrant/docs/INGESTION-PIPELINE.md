# Ingestion Pipeline Architecture

## Overview

This document covers the step-by-step architecture for building production ingestion pipelines that take large datasets (Slack channels, Fireflies transcripts, Google Drive folders, databases, APIs) and reliably ingest every record into Qdrant.

---

## Phase 1: Collection Setup (Run Once)

Before ingesting, ensure the collection exists with the correct configuration.

### Node Sequence
```
[Manual Trigger or Webhook]
    → [Qdrant: Collection Exists]
    → [IF: exists == false]
         → [Qdrant: Create Collection]
```

### Collection Config for Dense-Only
```json
{
  "vectors": {
    "size": 3072,
    "distance": "Cosine"
  }
}
```

### Collection Config for Hybrid (Dense + Sparse)
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
        "on_disk": false
      }
    }
  }
}
```

### Create Payload Indexes After Collection Creation
Always create indexes on fields you'll filter by:
```
[Qdrant: Create Payload Index] → field: "doc_id", schema: "keyword"
[Qdrant: Create Payload Index] → field: "source_type", schema: "keyword"
[Qdrant: Create Payload Index] → field: "created_at", schema: "datetime"
[Qdrant: Create Payload Index] → field: "source_context", schema: "keyword"
```

---

## Phase 2: Source Data Extraction

### Slack Channel Ingestion
```
[Schedule Trigger: every 15min]
    → [Slack: Get Channel Messages] (paginate with cursor)
    → [Split In Batches: batchSize=50]
```

**Key fields to extract from Slack**:
- `ts` → use as `source_id` (unique message timestamp)
- `text` → content to embed
- `channel` → source_context
- `user` → author
- `thread_ts` → for threading context

### Fireflies Meeting Transcript Ingestion
```
[Webhook or Schedule Trigger]
    → [HTTP Request: GET /transcripts/{id}]
    → [Split In Batches: batchSize=1]
```

**Key fields from Fireflies**:
- `id` → doc_id
- `title` → document title
- `date` → created_at
- `sentences[]` → iterate per sentence or concatenate into segments
- `participants[]` → metadata array
- `topics[]` → pre-built topic tags

### Google Drive Folder Ingestion
```
[Manual Trigger or Schedule]
    → [Google Drive: List Files in Folder]
    → [Split In Batches: batchSize=5]
    → [Google Drive: Download File]
    → [Extract From File: text]
```

### Generic API / Database Ingestion
```
[Trigger]
    → [HTTP Request / DB Node: fetch records]
    → [Split In Batches: batchSize=20-100]
```

---

## Phase 3: Content Normalization

Use a **Set node** to normalize your source data into a consistent schema before metadata extraction and embedding.

### Standard Normalized Schema
```javascript
// Set node expressions
{
  "content": "={{ $json.text || $json.body || $json.transcript }}",
  "doc_id": "={{ $json.id || $json.ts || $json.fileId }}",
  "source_type": "slack",  // hardcode per pipeline
  "source_context": "={{ $json.channel || $json.folder_name }}",
  "author": "={{ $json.user || $json.speaker }}",
  "created_at": "={{ $json.ts ? new Date($json.ts * 1000).toISOString() : $json.date }}",
  "title": "={{ $json.title || $json.text?.substring(0, 100) }}"
}
```

**Deduplication check** (optional but recommended for re-runs):
```
[Set: normalize]
    → [Qdrant: Count Points with filter doc_id == current_id]
    → [IF: count > 0]
         → SKIP (continue to next batch item)
         → PROCESS (continue ingestion)
```

---

## Phase 4: AI Metadata Extraction

Run **before chunking** — extract metadata from the full document, then attach to every chunk.

### Information Extractor Node Config

**Input**: `={{ $json.content }}` (the full document text)

**Attributes to extract** (adapt per source type):

```json
[
  {
    "name": "summary",
    "description": "1-3 sentence summary of the content"
  },
  {
    "name": "keywords",
    "description": "Array of 5-10 keywords capturing the main topics"
  },
  {
    "name": "entities",
    "description": "Named entities mentioned: people, companies, products, locations"
  },
  {
    "name": "sentiment",
    "description": "Overall sentiment: positive, negative, neutral, mixed"
  },
  {
    "name": "topics",
    "description": "Array of topic categories from a standard taxonomy"
  },
  {
    "name": "action_items",
    "description": "Any action items, decisions, or follow-ups mentioned"
  },
  {
    "name": "language",
    "description": "ISO 639-1 language code of the content"
  }
]
```

**LLM to use**: Gemini Flash or GPT-4o-mini (fast, cost-efficient for extraction tasks)

### Merge Metadata Back

After extraction, use a **Merge node** (combineByPosition or combineAll) to join the original normalized record with the extracted metadata before passing to the chunking stage.

```
[Set: normalize] ─────────────────────────────────── [Merge: combineByPosition]
[Information Extractor] → [Set: flatten output] ──── [Merge]
                                                          ↓
                                              [Text Splitter + Embedding]
```

---

## Phase 5: Text Splitting

### Using LangChain Data Loader + Token Splitter

Connect in this order:
```
[Qdrant Vector Store (insert mode)]
    ↑ ai_document
[Data Loader (documentDefaultDataLoader)]
    ↑ ai_textSplitter
[Token Splitter]
    
[Data Loader parameters]
  dataType: "json" or "binary"
  binaryMode: "specificField" (for file downloads)
  
[Data Loader metadata] — inject all metadata fields here:
  file_id: ={{ $json.doc_id }}
  source_type: ={{ $json.source_type }}
  source_context: ={{ $json.source_context }}
  created_at: ={{ $json.created_at }}
  keywords: ={{ $json.metadata_extraction.keywords }}
  summary: ={{ $json.metadata_extraction.summary }}
  entities: ={{ $json.metadata_extraction.entities }}
  topics: ={{ $json.metadata_extraction.topics }}
```

### Chunk Size Guidelines by Source Type

| Source | chunkSize (tokens) | chunkOverlap | Rationale |
|--------|--------------------|--------------|-----------|
| Slack messages | 256 | 25 | Messages are already short; 1 message = 1-2 chunks |
| Fireflies sentences | 512 | 50 | Preserve sentence-level context |
| Meeting full transcript | 1500 | 200 | Capture full thought segments |
| PDF documents | 1000 | 150 | Balance context vs precision |
| Google Docs | 800 | 100 | Section-level granularity |
| Code files | 512 | 100 | Function-level chunks |
| Email threads | 600 | 75 | Per email + some context |

---

## Phase 6: Embedding + Upsert

### LangChain Path (Recommended for Most Cases)
```
[Data Loader] → [Qdrant Vector Store: insert]
                    ↑ ai_embedding
               [OpenAI Embeddings: text-embedding-3-large]
```

The LangChain Vector Store handles embedding + upsert atomically.

### Direct Upsert Path (When You Need Full Payload Control)
```
[Code Node: generate UUID for each chunk]
    → [HTTP Request: POST to embedding API]
    → [Code Node: parse embedding array]
    → [Qdrant Node: Upsert Points]
```

Use this path when:
- You need to compute sparse vectors alongside dense
- You have pre-computed embeddings from an external system
- You need to store custom vector names for multi-vector collections

---

## Phase 7: Rate Limiting & Flow Control

### For Large Datasets (10k+ records)

```
[Source]
    → [Split In Batches: batchSize=25]
    → [... process batch ...]
    → [Qdrant: Upsert]
    → [Wait: 1-2 seconds]  ← critical for API rate limits
    → [back to Split In Batches]
```

### Wait Node Configuration
- `resumeUnit`: `seconds`
- `resumeAmount`: 1–5 (tune based on API plan)
- Set on the Qdrant Vector Store node: `onError: continueRegularOutput` + `retryOnFail: true`

### Error Handling Pattern
```
[Qdrant Node]
    → main output: continue to Wait → Loop
    → error output (if onError=continueErrorOutput): 
          → [Set: log error record]
          → [Google Sheets / Slack: report failed record]
          → continue to Wait → Loop
```

---

## Phase 8: Completion Notification

Always send a completion signal after large ingestion jobs:

```
[Split In Batches: "done" output]
    → [Telegram / Slack: "Ingestion complete: X records processed"]
```

---

## Full Pipeline: Slack Channel to Qdrant

```
[Schedule: every hour]
    → [Slack: getMessages channel=#engineering, limit=200]
    → [IF: message not already indexed] (check via Qdrant Count Points)
    → [Split In Batches: 20]
    → [Set: normalize fields]
    → [Information Extractor: keywords, summary, sentiment]
    → [Merge: normalized + metadata]
    → [Qdrant Vector Store: insert mode]
         ↑ Token Splitter (512 tokens, 50 overlap)
         ↑ Data Loader (json, with metadata injection)
         ↑ OpenAI Embeddings (text-embedding-3-large)
    → [Wait: 1s]
    → [loop back]
    → [Slack: notify #ops "Ingestion complete"]
```

---

## Deletion Pipeline (With Safety Gate)

When source records are deleted or updated, remove old vectors:

```
[Webhook: delete event from source system]
    → [Set: extract doc_id from payload]
    → [Telegram: sendAndWait "Delete X vectors for doc_id Y? [Approve/Decline]"]
    → [IF: approved == true]
         → [Qdrant Node: Delete Points, filter: doc_id == Y]
         → [Telegram: "Deletion complete"]
    → [IF: declined]
         → [Telegram: "Deletion cancelled"]
```

For automated re-ingestion (update = delete + re-ingest):
```
[Source update event]
    → [Qdrant: Delete Points by doc_id]
    → [continue to ingestion pipeline with new content]
```
