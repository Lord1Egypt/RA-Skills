# n8n + Qdrant: Ingestion & RAG Pipeline Skill

## Overview

This skill enables AI agents to design, build, and troubleshoot **production-grade Qdrant ingestion and retrieval pipelines in n8n**. It covers the full lifecycle: source data extraction → chunking → metadata enrichment → vector embedding → Qdrant upsert → retrieval (dense, sparse, hybrid) → RAG response generation.

**Always read the supporting docs in `/docs/` before building workflows:**
- `docs/NODE-REFERENCE.md` — Every Qdrant node, mode, and parameter explained
- `docs/INGESTION-PIPELINE.md` — Step-by-step ingestion architecture
- `docs/RAG-RETRIEVAL.md` — Dense, sparse, and hybrid retrieval patterns
- `docs/CHUNKING-METADATA.md` — Chunking strategies and metadata schema design
- `docs/examples/` — Annotated workflow JSON examples

---

## Two Node Systems to Know

n8n has **two separate Qdrant integration systems** — knowing which to use is critical:

### 1. Official Qdrant Node (`n8n-nodes-qdrant`)
- **Package**: `n8n-nodes-qdrant` (community node, install via n8n Settings → Community Nodes)
- **Purpose**: Direct Qdrant API operations — collection management, point upsert/delete/scroll, search queries
- **Node name in editor**: `Qdrant`
- **Use for**: Building custom ingestion pipelines, running Query Points (dense/sparse/hybrid search), collection setup, point management
- **GitHub**: https://github.com/qdrant/n8n-nodes-qdrant

### 2. LangChain Vector Store Node (built-in)
- **Package**: Built into n8n's AI/LangChain nodes
- **Purpose**: LangChain-compatible vector store integration — connects with Document Loaders, Text Splitters, Embeddings, and AI Agents
- **Node name in editor**: `Qdrant Vector Store` (`@n8n/n8n-nodes-langchain.vectorStoreQdrant`)
- **Use for**: LangChain-style RAG pipelines, AI Agent tool integration, retrieve-as-tool mode
- **Modes**: `insert` (ingest documents), `retrieve` (similarity search), `retrieve-as-tool` (AI agent tool)

**Rule of thumb**: Use LangChain Vector Store for LangChain-native agent/RAG flows. Use the Official Qdrant Node for direct API control, hybrid search, payload operations, and production ingestion pipelines.

---

## Quick Decision Matrix

| Goal | Use This Node | Mode/Operation |
|------|--------------|---------------|
| Ingest documents via LangChain chain | LangChain Vector Store | `insert` |
| AI Agent retrieves from Qdrant as tool | LangChain Vector Store | `retrieve-as-tool` |
| Run hybrid (dense+sparse) search | Official Qdrant Node | `Search → Query Points` |
| Create/manage collections | Official Qdrant Node | `Collection → Create Collection` |
| Upsert raw points with custom payloads | Official Qdrant Node | `Point → Upsert Points` |
| Delete points by filter (e.g. file_id) | Official Qdrant Node | `Point → Delete Points` |
| Scroll all points for audit/export | Official Qdrant Node | `Point → Scroll Points` |
| Batch ingest large datasets | Official Qdrant Node | `Point → Batch Update Points` |

---

## Canonical Ingestion Pipeline Architecture

```
[Trigger]
    │
    ▼
[Source Node] ──────────────────────────────────────────────
(Slack, Fireflies, Google Drive, HTTP, DB, etc.)             │
    │                                                         │
    ▼                                                         │
[Split in Batches]  ←── Loop for large datasets              │
    │                                                         │
    ▼                                                         │
[Extract/Normalize]                                          │
(Set node: build content string + raw metadata)              │
    │                                                         │
    ▼                                                         │
[AI: Extract Metadata]                                       │
(Information Extractor or LLM Chain)                         │
Produces: themes, keywords, entities, summary, tags          │
    │                                                         │
    ▼                                                         │
[Text Splitter]                                              │
(Token Splitter or Recursive Character Splitter)             │
chunkSize: 512–2000 tokens, overlap: 10–15%                  │
    │                                                         │
    ▼                                                         │
[Embeddings Node]                                            │
(OpenAI text-embedding-3-large or similar)                   │
    │                                                         │
    ▼                                                         │
[Qdrant Vector Store — insert mode]  OR                      │
[Official Qdrant Node — Upsert Points]                       │
    │                                                         │
    ▼                                                         │
[Wait Node]  ←── Rate limiting / backpressure                │
    │                                                         │
    └─────────────────── back to Split in Batches ───────────┘
```

See `docs/INGESTION-PIPELINE.md` for full node-by-node configuration.

---

## Canonical RAG Retrieval Architecture

```
[Chat Trigger / Webhook]
    │
    ▼
[AI Agent Node]
    │
    ├── [LLM: Gemini / GPT-4o / Claude]
    ├── [Memory: Window Buffer Memory]
    └── [Tool: Qdrant Vector Store — retrieve-as-tool]
              │
              └── [Embeddings Node]
```

For hybrid search (dense + sparse), use the **Official Qdrant Node** → Query Points with a `prefetch` array combining dense and sparse queries + RRF fusion. See `docs/RAG-RETRIEVAL.md`.

---

## Credentials Setup

### Official Qdrant Node
- **Credential type**: `qdrantApi`
- Fields: `URL` (e.g. `https://your-cluster.cloud.qdrant.io`) + `API Key`

### LangChain Vector Store Node
- **Credential type**: `qdrantApi` (same credential, shared)

### Qdrant Cloud Setup
1. Open https://cloud.qdrant.io → select cluster
2. Copy **Endpoint** → use as URL
3. Go to **API Keys** tab → copy key

### Local (Docker / AI Starter Kit)
- URL: `http://qdrant:6333/`
- Set `QDRANT_API_KEY=your_key` in docker-compose environment

---

## Naming Conventions

Use consistent naming across workflows:

| Element | Convention | Example |
|---------|-----------|---------|
| Collection name | `{org}-{source}-{content-type}` | `acme-slack-messages` |
| Metadata key for source ID | `source_id` | `"source_id": "C01234-1709123456"` |
| Metadata key for document ID | `doc_id` | `"doc_id": "file_abc123"` |
| Metadata key for chunk index | `chunk_index` | `"chunk_index": 3` |
| Metadata key for timestamp | `created_at` | ISO 8601 string |
| Metadata key for source type | `source_type` | `"slack"`, `"fireflies"`, `"gdrive"` |
| Metadata key for channel/folder | `source_context` | `"#engineering"` |

---

## Critical Rules

1. **Always set `file_id` or `doc_id` in metadata** — enables targeted deletion without full collection wipe
2. **Always use `onError: continueRegularOutput`** on the Qdrant Vector Store node — prevents single-item failures from crashing the whole batch
3. **Always use `retryOnFail: true`** on the Qdrant node for production ingestion
4. **Chunk before embedding** — never embed full documents; always split first
5. **Never store raw text in collection names or keys** — normalize to lowercase slug format
6. **Use `Split in Batches` with a `Wait` node** for large datasets — prevents API rate limit errors and memory exhaustion
7. **Run metadata extraction BEFORE the text splitter** — extract from the full document, then attach metadata to each chunk
8. **For delete operations, always add human-in-the-loop confirmation** (Telegram sendAndWait, Slack approval, etc.)
