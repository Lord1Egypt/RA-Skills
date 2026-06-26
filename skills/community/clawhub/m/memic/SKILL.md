---
name: memic-sdk
version: 0.3.0
description: Context engineering platform for AI agents. Upload documents, search with semantic + structured queries, and inject relevant context into LLM prompts. Supports RAG, Text2SQL, hybrid search, metadata filters, and multi-tenant isolation. Use this skill to integrate Memic into any AI agent, copilot, or application that needs grounded context from documents and databases.
homepage: https://app.memic.ai
metadata:
  openclaw:
    emoji: "🧠"
    primaryEnv: MEMIC_API_KEY
    requires:
      env:
        - MEMIC_API_KEY
      bins:
        - pip
---

# Memic — Context Engineering SDK

## What is Memic?

Memic is a managed context engineering platform. Instead of stuffing raw documents into your LLM's context window (expensive, slow, hits token limits), Memic handles the entire pipeline — document ingestion, chunking, embedding, vector storage — and gives you a single search API that returns only the relevant pieces. It also supports Text2SQL for structured databases, so one API covers both documents and databases.

**The problem it solves**: AI agents and LLM apps need grounded context from real data. Without Memic, you'd build and maintain your own chunking pipeline, embedding infrastructure, vector database, and query routing. Memic does all of this as a service — upload files, search with one API call, get back ranked chunks with source attribution.

**Key capabilities**:
- **Document search (RAG)** — Upload PDFs, DOCX, PPTX, TXT, etc. Memic chunks, embeds, and indexes them. Search returns ranked content with file name, page number, and relevance score.
- **Database search (Text2SQL)** — Connect PostgreSQL/MySQL. Ask natural language questions, get SQL-generated results back.
- **Hybrid search** — Single API auto-routes queries to the right source (documents, database, or both).
- **Multi-tenant isolation** — Each API key is scoped to an org/project/environment. No data leaks between tenants.
- **Metadata filters** — Filter by reference ID, page range, category, document type.

Your API key auto-resolves all context (org, project, environment) — no IDs needed in API calls.

**Coming soon**:
- **MCP server** — Native Model Context Protocol integration so AI agents (OpenClaw, Claude Code, etc.) can call Memic as a tool directly.
- **Context compaction** — Upload raw agent session logs or MEMORY.md files. Memic summarizes, compresses, and indexes them so agents can retrieve past context without re-loading full session history.
- **Bulk context injection** — Ingest entire knowledge bases (session JSONL, chat logs, wiki exports) in one call. Memic auto-chunks and indexes for instant search.

**When to use this skill**: Setting up Memic SDK, uploading documents, searching for context, building RAG pipelines, connecting databases for Text2SQL, debugging integration issues, or reducing LLM token costs by replacing raw context with targeted search.

## Quick Start

```bash
pip install memic
export MEMIC_API_KEY=mk_your_key_here
```

```python
from memic import Memic

client = Memic()  # API key auto-resolves org/project/environment

# Upload a document
file = client.upload_file("/path/to/doc.pdf")

# Search — returns only the relevant chunks, not the whole document
results = client.search(query="What are the key findings?", top_k=5)
for r in results:
    print(f"[{r.score:.2f}] {r.file_name} p{r.page_number}: {r.content[:100]}")
```

## First: Understand the Use Case

**Ask the developer two questions:**

### Question 1: Integration Pattern
"How are you planning to use Memic?"

1. **Context tool for an AI agent** — Memic provides RAG context for an LLM agent (chatbot, copilot, assistant)
2. **Deterministic service** — Direct search API in your app (no LLM involved)

### Question 2: Data Source
"What type of data will you be searching?"

1. **Unstructured (Documents)** — PDFs, Word docs, text files → semantic vector search
2. **Structured (Databases)** — PostgreSQL/MySQL → natural language to SQL
3. **Hybrid** — Both document search and database queries via a single API

## Prerequisites

- Python 3.8+
- A Memic account at https://app.memic.ai
- An API key (starts with `mk_...`)

## Step 1: Get API Key

1. Go to https://app.memic.ai → Dashboard → API Keys
2. Click "Create API Key"
3. Copy the key

**Important**: Each API key is scoped to an organization + project + environment. The SDK auto-resolves this context — you never need to pass IDs.

## Step 2: Install & Configure

```bash
pip install memic
```

```bash
# .env file
MEMIC_API_KEY=mk_your_api_key_here
```

## Step 3: Verify Setup

```python
from memic import Memic

client = Memic()

# Check what your API key resolves to
print(f"Org: {client.org_id}")
print(f"Project: {client.project_id}")
print(f"Environment: {client.environment_slug}")

# List projects in your org
projects = client.list_projects()
for p in projects:
    print(f"  - {p.name} ({p.id})")
```

### If No Data Found

**For documents:** Upload via dashboard (https://app.memic.ai → Project → Upload) or SDK (see below).

**For databases:** Go to https://app.memic.ai → Connectors → Add Connector. Enter your PostgreSQL/MySQL connection details.

## Core API Reference

### Upload Files

```python
# Upload and wait for processing to complete
file = client.upload_file(
    file_path="/path/to/document.pdf",
    reference_id="lesson_123",       # optional — for external system linking
    metadata={"category": "legal"},  # optional — custom key-value pairs
)
print(f"ID: {file.id}, Status: {file.status}")  # status = "ready" when done
```

Supported formats: PDF, DOCX, DOC, PPTX, XLSX, TXT, MD, HTML, and more.

### Check File Status

```python
file = client.get_file_status(file_id="...")
print(f"Status: {file.status}")
print(f"Processing: {file.status.is_processing}")
print(f"Failed: {file.status.is_failed}")
print(f"Chunks: {file.total_chunks}")
```

### Search Documents (Semantic)

```python
results = client.search(
    query="What are the key findings?",
    top_k=10,
    min_score=0.7,
)

print(f"Found {results.total_results} results in {results.search_time_ms}ms")
for r in results:
    print(f"[{r.score:.2f}] {r.file_name} p{r.page_number}: {r.content[:150]}")
```

### Search with Metadata Filters

```python
from memic import MetadataFilters, PageRange

results = client.search(
    query="contract terms",
    top_k=5,
    filters=MetadataFilters(
        reference_id="contract_2024",              # filter by reference
        page_range=PageRange(gte=1, lte=20),       # pages 1-20 only
        category="legal",                          # by category
    )
)
```

**Available filters:**
- `reference_id` / `reference_ids` — match file reference IDs
- `page_number` / `page_numbers` — exact page match
- `page_range` — page range with `gte`/`lte`
- `category` — filter by category
- `document_type` — filter by document type

### Search with File Scoping

```python
# Search only within specific files
results = client.search(
    query="revenue figures",
    file_ids=["file-id-1", "file-id-2"],
    top_k=5,
)
```

### Hybrid Search (Documents + Databases)

When you have both documents and database connectors configured, Memic auto-routes queries:

```python
results = client.search(query="Show me top customers by revenue")

# Check how the query was routed
if results.routing:
    print(f"Route: {results.routing.route}")        # "semantic", "structured", or "hybrid"
    print(f"Reason: {results.routing.reasoning}")

# Document results
if results.has_documents:
    for r in results.results.semantic:
        print(f"[Doc] {r.file_name}: {r.content[:100]}")

# Database results (Text2SQL)
if results.has_structured:
    print(f"SQL: {results.routing.sql_generated}")
    for row in results.results.structured.rows:
        print(f"[DB] {row}")
```

### Chat (RAG with built-in LLM)

```python
response = client._request(
    "POST", "/sdk/chat",
    json={"question": "What are the Q4 results?", "top_k": 5, "min_score": 0.5}
)
print(response["answer"])
print(f"Citations: {response['citations']}")
print(f"Model: {response['model']}")
```

## Integration Patterns

### Pattern A: Context Tool for AI Agent

Use Memic to inject grounded context into your LLM:

```python
from memic import Memic
from openai import OpenAI  # or anthropic, etc.

memic = Memic()
llm = OpenAI()

def ask_with_context(question: str) -> str:
    # 1. Get relevant context from Memic
    results = memic.search(query=question, top_k=5, min_score=0.6)

    # 2. Format as LLM context
    context = "\n\n".join([
        f"[Source: {r.file_name}, Page {r.page_number}]\n{r.content}"
        for r in results
    ])

    # 3. Generate grounded response
    response = llm.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Answer based on this context:\n\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

answer = ask_with_context("What are the key contract terms?")
```

### Pattern B: OpenClaw / AI Agent Context Optimization

Replace expensive raw-context loading with targeted search to cut token costs:

```python
from memic import Memic

memic = Memic()

# Instead of loading entire documents into context (thousands of tokens),
# search for just the relevant chunks (hundreds of tokens)
results = memic.search(query=user_question, top_k=3, min_score=0.7)

# Only inject what's relevant — typically 90%+ token savings vs raw context
context = "\n".join([r.content for r in results])
```

### Pattern C: Deterministic Search API

Direct integration for app search functionality:

```python
from memic import Memic, MetadataFilters

memic = Memic()

def search_documents(query: str, category: str = None) -> dict:
    filters = MetadataFilters(category=category) if category else None

    results = memic.search(
        query=query,
        top_k=10,
        min_score=0.5,
        filters=filters,
    )

    return {
        "results": [
            {
                "title": r.file_name,
                "snippet": r.content[:300],
                "page": r.page_number,
                "score": r.score,
            }
            for r in results
        ],
        "total": results.total_results,
    }
```

## Debugging

| Issue | Solution |
|-------|----------|
| `AuthenticationError` | Check `MEMIC_API_KEY` is set and valid |
| `NotFoundError` | API key may be scoped to wrong project |
| Empty results | Check files are uploaded and status is `READY` |
| Low scores | Lower `min_score` or rephrase query |
| Timeout on upload | Large files take longer; increase `poll_timeout` |

### Exception Handling

```python
from memic import MemicError, AuthenticationError, NotFoundError, APIError

try:
    results = client.search(query="test")
except AuthenticationError:
    print("Invalid or expired API key")
except NotFoundError:
    print("Resource not found")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
except MemicError as e:
    print(f"SDK error: {e}")
```

## Resources

- **SDK**: `pip install memic` | https://pypi.org/project/memic/
- **Dashboard**: https://app.memic.ai
- **GitHub**: https://github.com/memic-ai/memic-python
