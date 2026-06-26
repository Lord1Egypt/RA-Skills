# Example: RAG Chat Agent with Qdrant

Two patterns are documented here:
1. **Simple RAG Agent** — LangChain AI Agent + Qdrant as tool (easiest setup)
2. **Hybrid Search RAG** — Official Qdrant node with dense+sparse+RRF (best quality)

---

## Pattern 1: Simple RAG Agent (LangChain)

### Overview
Uses n8n's built-in LangChain nodes. The AI Agent automatically decides when to query the knowledge base and formulates answers from retrieved context.

```
[Chat Trigger] → [AI Agent] → [Respond to User]
                    ↑ LLM (Gemini/GPT-4o)
                    ↑ Window Buffer Memory
                    ↑ Qdrant Vector Store Tool
                         ↑ OpenAI Embeddings
```

### Workflow JSON
```json
{
  "name": "RAG Chat Agent - Qdrant",
  "nodes": [
    {
      "id": "chat-trigger",
      "name": "Chat Trigger",
      "type": "@n8n/n8n-nodes-langchain.chatTrigger",
      "position": [-600, 0],
      "parameters": { "options": {} },
      "webhookId": "your-webhook-id",
      "typeVersion": 1.1
    },
    {
      "id": "ai-agent",
      "name": "AI Agent",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "position": [-400, 0],
      "parameters": {
        "text": "={{ $json.chatInput }}",
        "promptType": "define",
        "options": {
          "systemMessage": "You are a helpful knowledge assistant. Use the knowledge_base tool to search for relevant information before answering questions.\n\nAlways:\n- Search the knowledge base first for any question about company matters\n- Cite your sources (mention the source_context and created_at from retrieved results)\n- If the knowledge base doesn't contain relevant information, say so clearly\n- Never make up facts not present in the retrieved context"
        }
      },
      "typeVersion": 1.7
    },
    {
      "id": "llm-gemini",
      "name": "Gemini Flash",
      "type": "@n8n/n8n-nodes-langchain.lmChatGoogleGemini",
      "position": [-550, 200],
      "parameters": {
        "modelName": "models/gemini-2.0-flash-exp",
        "options": { "maxOutputTokens": 8192, "temperature": 0.3 }
      },
      "credentials": { "googlePalmApi": { "id": "gemini-cred", "name": "Google Gemini" } },
      "typeVersion": 1
    },
    {
      "id": "memory",
      "name": "Window Buffer Memory",
      "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
      "position": [-400, 200],
      "parameters": { "contextWindowLength": 20 },
      "typeVersion": 1.3
    },
    {
      "id": "qdrant-tool",
      "name": "Qdrant: Knowledge Base Tool",
      "type": "@n8n/n8n-nodes-langchain.vectorStoreQdrant",
      "position": [-250, 200],
      "parameters": {
        "mode": "retrieve-as-tool",
        "topK": 15,
        "toolName": "knowledge_base",
        "toolDescription": "Search the company knowledge base including Slack conversations, meeting transcripts, and documents. Use this for any question about company processes, decisions, or historical information.",
        "qdrantCollection": {
          "__rl": true,
          "mode": "id",
          "value": "CONFIGURE_ME_COLLECTION"
        },
        "options": {}
      },
      "credentials": { "qdrantApi": { "id": "qdrant-cred", "name": "Qdrant" } },
      "typeVersion": 1
    },
    {
      "id": "embeddings-retrieval",
      "name": "OpenAI Embeddings (Retrieval)",
      "type": "@n8n/n8n-nodes-langchain.embeddingsOpenAi",
      "position": [-100, 300],
      "parameters": {
        "model": "text-embedding-3-large",
        "options": {}
      },
      "credentials": { "openAiApi": { "id": "openai-cred", "name": "OpenAI" } },
      "typeVersion": 1
    },
    {
      "id": "respond",
      "name": "Respond to User",
      "type": "n8n-nodes-base.set",
      "position": [-200, 0],
      "parameters": {
        "options": {},
        "assignments": {
          "assignments": [
            { "name": "output", "value": "={{ $json.output }}", "type": "string" }
          ]
        }
      },
      "typeVersion": 3.4
    }
  ],
  "connections": {
    "Chat Trigger": { "main": [[{ "node": "AI Agent", "type": "main", "index": 0 }]] },
    "AI Agent": { "main": [[{ "node": "Respond to User", "type": "main", "index": 0 }]] },
    "Gemini Flash": { "ai_languageModel": [[{ "node": "AI Agent", "type": "ai_languageModel", "index": 0 }]] },
    "Window Buffer Memory": { "ai_memory": [[{ "node": "AI Agent", "type": "ai_memory", "index": 0 }]] },
    "Qdrant: Knowledge Base Tool": { "ai_tool": [[{ "node": "AI Agent", "type": "ai_tool", "index": 0 }]] },
    "OpenAI Embeddings (Retrieval)": { "ai_embedding": [[{ "node": "Qdrant: Knowledge Base Tool", "type": "ai_embedding", "index": 0 }]] }
  }
}
```

---

## Pattern 2: Hybrid Search RAG (Maximum Quality)

### Overview
Uses the Official Qdrant Node to run dense + sparse search with RRF fusion, then passes context to an LLM manually. More control, better retrieval quality.

**Requirements**: Collection must be configured with both dense and sparse vectors. Requires a sparse encoding service (see notes below).

```
[Chat Trigger]
    → [Parallel: Dense Embed + Sparse Encode]
    → [Merge embeddings]
    → [Qdrant: Query Points (hybrid/RRF)]
    → [Code: format context]
    → [OpenAI / Gemini: generate answer]
    → [Respond]
```

### Workflow JSON (Simplified)
```json
{
  "name": "Hybrid RAG Pipeline - Qdrant",
  "nodes": [
    {
      "id": "webhook-in",
      "name": "Chat Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [-800, 0],
      "parameters": { "path": "chat", "options": {} },
      "typeVersion": 2
    },
    {
      "id": "dense-embed",
      "name": "Dense Embedding",
      "type": "n8n-nodes-base.httpRequest",
      "position": [-600, -80],
      "parameters": {
        "url": "https://api.openai.com/v1/embeddings",
        "method": "POST",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [{ "name": "Authorization", "value": "=Bearer {{ $env.OPENAI_API_KEY }}" }]
        },
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            { "name": "model", "value": "text-embedding-3-large" },
            { "name": "input", "value": "={{ $json.body.query }}" }
          ]
        },
        "options": {}
      },
      "typeVersion": 4.2
    },
    {
      "id": "sparse-encode",
      "name": "Sparse Encoding (BM25/SPLADE)",
      "type": "n8n-nodes-base.httpRequest",
      "position": [-600, 80],
      "parameters": {
        "url": "http://your-sparse-encoder-service/encode",
        "method": "POST",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            { "name": "text", "value": "={{ $json.body.query }}" }
          ]
        },
        "options": {}
      },
      "typeVersion": 4.2
    },
    {
      "id": "merge-vectors",
      "name": "Merge Vectors",
      "type": "n8n-nodes-base.merge",
      "position": [-400, 0],
      "parameters": { "mode": "combine", "combineBy": "combineAll", "options": {} },
      "typeVersion": 3
    },
    {
      "id": "hybrid-search",
      "name": "Qdrant: Hybrid Search",
      "type": "n8n-nodes-qdrant.qdrant",
      "position": [-200, 0],
      "parameters": {
        "resource": "search",
        "operation": "queryPoints",
        "collectionName": "CONFIGURE_ME_COLLECTION",
        "prefetch": "=[{ \"query\": {{ $json.dense_vector }}, \"using\": \"dense\", \"limit\": 20 }, { \"query\": { \"indices\": {{ $json.sparse_indices }}, \"values\": {{ $json.sparse_values }} }, \"using\": \"sparse\", \"limit\": 20 }]",
        "query": "={ \"fusion\": \"rrf\" }",
        "limit": 10,
        "withPayload": true,
        "withVector": false
      },
      "credentials": { "qdrantApi": { "id": "qdrant-cred", "name": "Qdrant" } },
      "typeVersion": 1
    },
    {
      "id": "format-context",
      "name": "Format Context",
      "type": "n8n-nodes-base.code",
      "position": [0, 0],
      "parameters": {
        "language": "javaScript",
        "jsCode": "const results = $input.all();\nconst query = $('Chat Webhook').item.json.body.query;\n\nconst context = results.map((item, i) => {\n  const p = item.json.payload;\n  return `[${i+1}] ${p.source_type} | ${p.source_context} | ${p.created_at?.substring(0,10)}\\n${p.text}`;\n}).join('\\n\\n---\\n\\n');\n\nreturn [{ json: { query, context, source_count: results.length } }];"
      },
      "typeVersion": 2
    },
    {
      "id": "llm-answer",
      "name": "Generate Answer",
      "type": "n8n-nodes-base.httpRequest",
      "position": [200, 0],
      "parameters": {
        "url": "https://api.openai.com/v1/chat/completions",
        "method": "POST",
        "sendHeaders": true,
        "headerParameters": {
          "parameters": [{ "name": "Authorization", "value": "=Bearer {{ $env.OPENAI_API_KEY }}" }]
        },
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            { "name": "model", "value": "gpt-4o" },
            { "name": "messages", "value": "=[{ \"role\": \"system\", \"content\": \"You are a helpful assistant. Answer questions based only on the provided context. Cite sources.\" }, { \"role\": \"user\", \"content\": \"Context:\\n{{ $json.context }}\\n\\nQuestion: {{ $json.query }}\" }]" },
            { "name": "max_tokens", "value": "=2000" }
          ]
        },
        "options": {}
      },
      "typeVersion": 4.2
    },
    {
      "id": "respond-webhook",
      "name": "Webhook Response",
      "type": "n8n-nodes-base.respondToWebhook",
      "position": [400, 0],
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ { \"answer\": $json.choices[0].message.content, \"sources_used\": $('Format Context').item.json.source_count } }}"
      },
      "typeVersion": 1
    }
  ]
}
```

---

## Sparse Encoder Service

For production hybrid search, run a simple FastAPI service alongside n8n:

```python
# sparse_encoder.py - Deploy as Docker container
from fastapi import FastAPI
from fastembed import SparseTextEmbedding

app = FastAPI()
model = SparseTextEmbedding(model_name="Qdrant/bm25")

@app.post("/encode")
async def encode(request: dict):
    text = request["text"]
    result = list(model.embed([text]))[0]
    return {
        "indices": result.indices.tolist(),
        "values": result.values.tolist()
    }
```

Add to docker-compose.yml:
```yaml
sparse-encoder:
  build: ./sparse_encoder
  ports:
    - "8001:8001"
  networks: ['demo']
```

Then in n8n, call `http://sparse-encoder:8001/encode`.

---

## Multi-Collection RAG (Multiple Sources)

When you have separate collections for different source types, use multiple Qdrant tool nodes:

```json
{
  "qdrant-tool-slack": {
    "toolName": "slack_messages",
    "toolDescription": "Search Slack channel messages and conversations",
    "qdrantCollection": "acme-slack-messages"
  },
  "qdrant-tool-meetings": {
    "toolName": "meeting_transcripts", 
    "toolDescription": "Search meeting transcripts and call recordings",
    "qdrantCollection": "acme-fireflies-transcripts"
  },
  "qdrant-tool-docs": {
    "toolName": "company_documents",
    "toolDescription": "Search company documents, policies, and guides",
    "qdrantCollection": "acme-gdrive-documents"
  }
}
```

The AI Agent will intelligently route queries to the appropriate tool(s) based on context.
