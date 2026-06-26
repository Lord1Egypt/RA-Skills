# Chunking Strategy & Metadata Schema Design

## Why Metadata Matters

In Qdrant, every point has a **payload** (the metadata). Rich, consistent payload design is what separates a basic prototype from a production-ready RAG system. Good metadata enables:

- **Filtered search**: find only content from a specific channel, timeframe, or source
- **Targeted deletion**: remove all chunks for a document without knowing their IDs
- **Source attribution**: tell users where an answer came from
- **Hybrid retrieval**: combine semantic search with structured filters
- **Observability**: audit what's in your collection

---

## Universal Metadata Schema

Every point in every collection should have these fields:

```json
{
  "text": "The actual chunk text that was embedded",
  "doc_id": "Unique identifier for the parent document/record",
  "chunk_index": 0,
  "chunk_total": 5,
  "source_type": "slack | fireflies | gdrive | pdf | email | webhook",
  "source_context": "Channel name, folder path, or collection identifier",
  "source_url": "Direct link to the source record (optional)",
  "author": "Who created the content",
  "created_at": "2024-03-15T10:30:00Z",
  "ingested_at": "2024-03-15T11:00:00Z",
  "language": "en",
  "collection_version": "1"
}
```

Plus **AI-extracted enrichment metadata** (generated at ingest time):
```json
{
  "summary": "1-3 sentence summary of the full parent document",
  "keywords": ["api", "redesign", "backend", "latency"],
  "entities": {
    "people": ["Alice Chen", "Bob Martinez"],
    "companies": ["Acme Corp"],
    "products": ["PaymentAPI v2"]
  },
  "topics": ["engineering", "product-design", "performance"],
  "sentiment": "neutral",
  "action_items": ["Review API spec by Friday", "Schedule design review"],
  "overarching_theme": "API redesign discussion focusing on latency improvements"
}
```

---

## Source-Specific Metadata Schemas

### Slack Messages
```json
{
  "text": "chunk text",
  "doc_id": "C01CHANNEL-1709123456.789000",
  "source_type": "slack",
  "source_context": "#engineering",
  "author": "alice.chen",
  "created_at": "2024-03-15T10:30:00Z",
  "thread_id": "1709123400.000000",
  "is_thread_reply": false,
  "reaction_count": 3,
  "workspace": "acme-corp"
}
```

**doc_id formula for Slack**: `{channel_id}-{message_ts}` — globally unique, sortable by time.

### Fireflies Meeting Transcripts
```json
{
  "text": "chunk text from transcript segment",
  "doc_id": "fireflies-meeting-abc123",
  "source_type": "fireflies",
  "source_context": "weekly-engineering-standup",
  "created_at": "2024-03-15T09:00:00Z",
  "meeting_title": "Weekly Engineering Standup",
  "duration_minutes": 45,
  "participants": ["alice@acme.com", "bob@acme.com"],
  "meeting_type": "standup",
  "has_action_items": true
}
```

**Chunking strategy for transcripts**: Chunk by speaker turns or by fixed token windows with overlap that preserves sentence boundaries. Segment-level chunks (one exchange = one chunk) often outperform fixed token splitting for meeting data.

### Google Drive Documents
```json
{
  "text": "chunk text",
  "doc_id": "gdrive-1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
  "source_type": "gdrive",
  "source_context": "/Company Docs/Engineering/",
  "author": "alice@acme.com",
  "created_at": "2024-02-01T00:00:00Z",
  "modified_at": "2024-03-10T14:22:00Z",
  "file_name": "API Design Guidelines.pdf",
  "file_type": "pdf",
  "file_size_bytes": 245000,
  "drive_folder": "Engineering"
}
```

### Email / Gmail
```json
{
  "text": "chunk text from email body",
  "doc_id": "gmail-18e1f2a3b4c5d6e7",
  "source_type": "email",
  "source_context": "engineering@acme.com",
  "author": "sender@external.com",
  "created_at": "2024-03-15T08:15:00Z",
  "subject": "Re: API v2 Launch Timeline",
  "thread_id": "18e1f2a3b4c5d6e7",
  "recipient_count": 5,
  "has_attachments": false
}
```

---

## Metadata Extraction with Information Extractor Node

### Node Configuration

```
[Information Extractor]
  text: ={{ $json.content }}
  model: Gemini Flash or GPT-4o-mini
  
  systemPromptTemplate: |
    You are an expert information extraction system. Extract structured
    metadata from the provided content. Return only the requested fields.
    If a field cannot be determined, omit it rather than guessing.
```

### Attributes Configuration by Use Case

#### For Slack / Chat Messages
```json
[
  { "name": "summary", "description": "1-2 sentence summary of what this message or thread is about" },
  { "name": "keywords", "description": "5-8 keywords as an array of strings" },
  { "name": "topics", "description": "Topic categories from: engineering, product, design, ops, hr, finance, general" },
  { "name": "sentiment", "description": "One of: positive, negative, neutral, frustrated, excited" },
  { "name": "has_question", "description": "Boolean: does the message contain a question?" },
  { "name": "has_decision", "description": "Boolean: does the message announce a decision?" },
  { "name": "action_items", "description": "Array of action items or tasks mentioned, empty array if none" }
]
```

#### For Meeting Transcripts
```json
[
  { "name": "overarching_theme", "description": "The main topic or purpose of this meeting segment" },
  { "name": "recurring_topics", "description": "Topics that come up repeatedly, as array of strings" },
  { "name": "pain_points", "description": "Problems or challenges mentioned, as array of strings" },
  { "name": "decisions_made", "description": "Concrete decisions or agreements reached, as array" },
  { "name": "action_items", "description": "Tasks assigned or volunteered for, include owner if mentioned" },
  { "name": "keywords", "description": "10 keywords that best represent this segment" },
  { "name": "sentiment", "description": "Overall tone: productive, tense, exploratory, conclusive" }
]
```

#### For Documents / PDFs
```json
[
  { "name": "title", "description": "Document title if not already known" },
  { "name": "summary", "description": "2-3 sentence executive summary" },
  { "name": "document_type", "description": "One of: policy, guide, report, spec, proposal, reference, other" },
  { "name": "keywords", "description": "10 most important keywords" },
  { "name": "entities", "description": "Named entities: people, companies, products, locations as nested object" },
  { "name": "topics", "description": "Topic taxonomy labels as array" },
  { "name": "target_audience", "description": "Who this document is intended for" },
  { "name": "version", "description": "Document version number if mentioned" }
]
```

---

## Flattening Metadata for Qdrant

The Information Extractor returns an `output` object. You need to flatten it for use in Data Loader metadata fields.

### Set Node Pattern (after Information Extractor)
```javascript
// Expression in Set node to flatten extracted metadata
{
  "meta_summary": "={{ $json.output.summary }}",
  "meta_keywords": "={{ $json.output.keywords }}",
  "meta_topics": "={{ $json.output.topics }}",
  "meta_sentiment": "={{ $json.output.sentiment }}",
  "meta_action_items": "={{ $json.output.action_items }}",
  "meta_entities": "={{ JSON.stringify($json.output.entities) }}"
}
```

Note: Qdrant payload supports arrays natively. Pass arrays directly for `keywords`, `topics`, `action_items`. Serialize complex nested objects to JSON string if needed.

---

## Chunking Decision Tree

```
Is the source structured with natural record boundaries?
    YES (Slack messages, emails, individual rows)
        → One chunk per record if under 512 tokens
        → If longer, split at 512 tokens with 50 token overlap
    
    NO (Long documents, transcripts, PDFs)
        → Is content conversational?
            YES (transcripts)
                → Split by speaker turn or sentence boundary
                → Max 1000 tokens per chunk, 150 token overlap
            NO (technical docs, reports)
                → Split at paragraph boundaries first
                → Max 1500 tokens per chunk, 200 token overlap
```

### Semantic Chunking (Advanced)
For highest retrieval quality, use semantic chunking: split text where the topic changes, not at fixed token boundaries. Implement via:
1. Split into sentences
2. Embed each sentence
3. Find breakpoints where cosine similarity between adjacent sentences drops below threshold
4. Group sentences into chunks at breakpoints

This requires a Code node with the embedding API. Performance improvement is 10-20% over fixed chunking but adds latency and cost.

---

## Payload Index Strategy

Always create these indexes after collection setup:

| Field | Index Type | Priority |
|-------|-----------|---------|
| `doc_id` | keyword | Critical — enables targeted deletion |
| `source_type` | keyword | High — multi-source filtering |
| `source_context` | keyword | High — channel/folder filtering |
| `created_at` | datetime | High — time-range filtering |
| `author` | keyword | Medium — per-author search |
| `topics` | keyword | Medium — topic filtering |
| `has_action_items` | bool | Low — task extraction workflows |
| `chunk_index` | integer | Low — debugging/auditing |

Create indexes via the Official Qdrant Node → Payload → Create Payload Index, or via the Qdrant REST API at collection setup time.

---

## Content Quality Filters (Pre-Ingestion)

Filter out low-value content before spending tokens on embedding:

```javascript
// Code node: filter before ingestion
const item = $input.first().json;
const text = item.content || '';

// Skip conditions
if (text.length < 20) return []; // Too short
if (text.trim().split(' ').length < 5) return []; // Less than 5 words
if (/^[\s\W]+$/.test(text)) return []; // Only whitespace/punctuation
if (text.startsWith('http') && text.split(' ').length < 3) return []; // Bare URLs

return [$input.first()];
```

This reduces noise, lowers embedding costs, and improves retrieval precision.
