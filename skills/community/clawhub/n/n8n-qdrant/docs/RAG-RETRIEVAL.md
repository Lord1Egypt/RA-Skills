# RAG Retrieval Patterns in n8n + Qdrant

## Dense vs Sparse vs Hybrid Search

Understanding the three retrieval modes is fundamental to building effective RAG pipelines.

---

## Dense Search (Semantic / Vector Search)

### What It Is
Dense search converts the query and all documents into high-dimensional vectors (embeddings) using a neural model. Similarity is measured by cosine similarity or dot product between the query vector and stored vectors.

### Strengths
- Captures semantic meaning, synonyms, paraphrases
- Works across languages (multilingual models)
- Finds conceptually related content even with no keyword overlap

### Weaknesses
- Can miss exact keyword matches (especially technical terms, IDs, names)
- Embedding quality varies by domain
- Requires re-embedding if model changes

### When to Use Dense Only
- General Q&A over prose documents
- Multi-language content
- Finding concepts described differently across docs
- Meeting transcripts, Slack conversations, support tickets

### n8n Implementation

**Option A: LangChain Vector Store (simplest)**
```
[Chat Trigger]
    → [AI Agent]
         ↑ [Qdrant Vector Store: retrieve-as-tool]
              ↑ [OpenAI Embeddings: same model as ingestion]
```

**Option B: Official Qdrant Node (more control)**
```
[Webhook / Chat input]
    → [HTTP Request: OpenAI Embeddings API]
    → [Code: extract embedding array from response]
    → [Qdrant Node: Query Points]
         query: ={{ $json.embedding }}
         limit: 10
         withPayload: true
         scoreThreshold: 0.65
    → [Set: format results for LLM context]
    → [LLM: generate response with context]
```

**Score threshold guidance**:
- 0.85+ = very high confidence (tight semantic match)
- 0.70–0.85 = strong match (recommended default)
- 0.55–0.70 = moderate match (exploratory search)
- Below 0.55 = likely noise, filter out

---

## Sparse Search (Keyword / BM25)

### What It Is
Sparse search uses high-dimensional vectors where each dimension corresponds to a vocabulary term. Most dimensions are zero; non-zero values represent term frequency/importance scores. SPLADE and BM25 are the most common sparse encoder models.

### Strengths
- Excellent for exact term matching (product codes, names, technical jargon)
- Interpretable — you can see which terms drove the match
- No information loss on rare/specialized terms

### Weaknesses
- No semantic understanding — "automobile" doesn't match "car"
- Requires sparse encoder to be run at query time
- Needs collection configured with sparse vector support

### When to Use Sparse Only
- Searching by exact field values, IDs, names
- Code search (exact function/class names)
- Legal/medical documents with precise terminology
- When users type exact terms from the source data

### Collection Setup for Sparse
The collection must be created with sparse vector config:
```json
{
  "sparse_vectors": {
    "sparse": {
      "index": { "on_disk": false }
    }
  }
}
```

### n8n Implementation

Since n8n doesn't have a native sparse encoder node, use one of:

**Option A: HTTP Request to a SPLADE/BM25 API**
```
[Query input]
    → [HTTP Request: POST to sparse-encoder-service/encode]
         body: { "text": "={{ $json.query }}" }
    → [Code: extract indices + values from response]
    → [Qdrant Node: Query Points]
         using: "sparse"
         query: { indices: =..., values: =... }
```

**Option B: Code Node with simple BM25**
```javascript
// Simple BM25-style sparse encoding in n8n Code node
const text = $input.first().json.query;
const tokens = text.toLowerCase().split(/\W+/).filter(t => t.length > 2);
const termFreq = {};
tokens.forEach(t => { termFreq[t] = (termFreq[t] || 0) + 1; });

// Map terms to vocabulary indices (requires vocabulary lookup)
// For production, call a proper SPLADE API instead
const indices = Object.keys(termFreq).map(t => hashTerm(t));
const values = Object.values(termFreq).map(f => Math.log(1 + f));

return [{ json: { sparse_indices: indices, sparse_values: values } }];
```

For production, deploy a FastAPI service wrapping `fastembed` or `splade` and call it via HTTP Request node.

---

## Hybrid Search (Dense + Sparse + RRF Fusion)

### What It Is
Hybrid search runs both dense and sparse queries simultaneously, then combines their ranked result lists using Reciprocal Rank Fusion (RRF) or relative score fusion (RSF). The result is a unified ranked list that captures both semantic meaning and keyword relevance.

### Why It's Better
Hybrid search consistently outperforms either method alone across most real-world datasets. It captures:
- Semantic similarity (dense) AND exact keyword matching (sparse)
- Handles both "find me something about X concept" AND "find docs mentioning product code ABC-123"

### RRF Formula
RRF score = Σ(1 / (rank_k + k)) where k=60 is standard
This naturally de-emphasizes outliers and rewards results that rank well across both methods.

### When to Use Hybrid
- **Default recommendation** for production RAG systems
- When your data mixes prose and technical content
- Slack/Discord channels (casual language + technical terms)
- Support tickets (user language + product identifiers)
- Meeting transcripts with action items and names

### Collection Setup
Must have both dense and sparse vectors:
```json
{
  "vectors": {
    "dense": { "size": 3072, "distance": "Cosine" }
  },
  "sparse_vectors": {
    "sparse": { "index": { "on_disk": false } }
  }
}
```

At ingest time, you must store BOTH vectors per point:
```json
{
  "id": "point-uuid",
  "vector": {
    "dense": [0.12, -0.34, ...],
    "sparse": {
      "indices": [102, 5843, 921],
      "values": [0.82, 0.61, 0.44]
    }
  },
  "payload": { ... }
}
```

### n8n Hybrid Search Implementation

```
[Query input: "what did the team decide about the API redesign?"]
    → [Parallel branches]:
         Branch A: [HTTP Request: Dense Embedding API]
                       → get dense vector
         Branch B: [HTTP Request: Sparse Encoder API]  
                       → get sparse indices + values
    → [Merge: combineAll]
    → [Qdrant Node: Query Points]
         prefetch: [
           {
             query: ={{ $json.dense_vector }},
             using: "dense",
             limit: 20
           },
           {
             query: {
               indices: ={{ $json.sparse_indices }},
               values: ={{ $json.sparse_values }}
             },
             using: "sparse",
             limit: 20
           }
         ],
         query: { fusion: "rrf" },
         limit: 10,
         withPayload: true
    → [Set: format context chunks]
    → [LLM: answer with context]
```

---

## RAG Agent Pipeline (LangChain Pattern)

The simplest production RAG setup using n8n's LangChain nodes:

```
[When chat message received]
    → [AI Agent]
         ↑ [LLM: Gemini Flash / GPT-4o]
         ↑ [Window Buffer Memory: contextWindowLength=40]
         ↑ [Qdrant Vector Store: retrieve-as-tool]
              toolName: "knowledge_base"
              toolDescription: "Search for relevant information from company documents and conversations"
              topK: 15
              ↑ [OpenAI Embeddings: text-embedding-3-large]
```

**AI Agent system prompt pattern**:
```
You are a helpful assistant with access to a knowledge base of [source description].

Use the knowledge_base tool to retrieve relevant information before answering.
Always cite which source you used (document title, date, channel).
If the knowledge base doesn't contain the answer, say so clearly.
Do not hallucinate or invent information not present in the retrieved context.
```

---

## Retrieval Configuration Reference

### topK / limit Values
| Use Case | Recommended topK |
|----------|-----------------|
| Single focused question | 5–8 |
| Complex multi-part question | 10–15 |
| Summarization / synthesis | 15–25 |
| AI Agent with re-ranking | 20–30 |

### Score Thresholds (Dense Search)
| Threshold | Interpretation |
|-----------|----------------|
| 0.90+ | Near-duplicate match |
| 0.80–0.90 | Highly relevant |
| 0.70–0.80 | Relevant — good default cutoff |
| 0.60–0.70 | Loosely related |
| <0.60 | Likely noise |

### Filtered Retrieval Examples

Retrieve only from a specific Slack channel:
```json
{
  "filter": {
    "must": [
      { "key": "source_context", "match": { "value": "#engineering" } }
    ]
  }
}
```

Retrieve only recent content:
```json
{
  "filter": {
    "must": [
      { 
        "key": "created_at",
        "range": { "gte": "2024-06-01T00:00:00Z" }
      }
    ]
  }
}
```

Retrieve from multiple sources:
```json
{
  "filter": {
    "should": [
      { "key": "source_type", "match": { "value": "slack" } },
      { "key": "source_type", "match": { "value": "fireflies" } }
    ]
  }
}
```

---

## Context Assembly for LLM

After retrieval, format the chunks into a clean context block:

### Set Node Expression (context assembly)
```javascript
// In a Code node after Qdrant search
const results = $input.all();
const contextChunks = results.map((item, i) => {
  const p = item.json.payload;
  return `[${i+1}] Source: ${p.source_type} | ${p.source_context} | ${p.created_at?.substring(0,10)}
${p.text || p.content}`;
}).join('\n\n---\n\n');

return [{ json: { context: contextChunks, source_count: results.length } }];
```

### LLM Prompt Pattern
```
Given the following context retrieved from our knowledge base:

{{ $json.context }}

Answer the following question:
{{ $('Chat Trigger').item.json.chatInput }}

If the context doesn't contain enough information, say "I don't have enough information about this in the knowledge base."
Always mention which sources you used.
```

---

## Query Points Groups (Diverse Results)

Prevent returning 10 chunks from the same document — get diverse results across documents:

```json
{
  "resource": "search",
  "operation": "queryPointsGroups",
  "collectionName": "my-collection",
  "query": "={{ $json.embedding }}",
  "groupBy": "doc_id",
  "groupSize": 2,
  "limit": 5
}
```
Returns top 2 chunks from each of the top 5 distinct documents — 10 results total, maximum diversity.

---

## Re-ranking (Post-Retrieval)

For high-stakes retrieval, add a re-ranking step after initial Qdrant search:

```
[Qdrant: Query Points, topK=30]
    → [HTTP Request: Cohere Re-rank API or similar]
         body: {
           query: "={{ $('Chat Trigger').item.json.chatInput }}",
           documents: "={{ $json.results.map(r => r.payload.text) }}",
           top_n: 8
         }
    → [Code: reassemble top_n results with original payloads]
    → [LLM: answer with re-ranked context]
```

Re-ranking consistently improves answer quality for complex questions and is recommended for production systems where accuracy is critical.
