---
name: okra
description: OkraPDF — upload PDFs, read extracted content, ask questions, extract structured data, and manage collections. Covers MCP, CLI, and HTTP.
---

# OkraPDF

Upload a PDF, get an API. Extract tables, ask questions, get structured JSON — via MCP, CLI, or HTTP.

**Designed for subagents.** Every document is its own stateless endpoint. Fire off parallel queries to different documents — no shared state, no locks, no ordering issues. Ideal as a tool inside agent loops (Claude, GPT, custom orchestrators).

## Setup

### MCP (Claude Code, Cursor, OpenCode)

Add to `~/.claude/mcp.json` or `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "okra-pdf": {
      "type": "url",
      "url": "https://api.okrapdf.com/mcp",
      "headers": { "Authorization": "Bearer YOUR_API_KEY" }
    }
  }
}
```

### CLI

```bash
npm install -g okrapdf
okra auth set-key YOUR_API_KEY
```

### HTTP

All endpoints use `https://api.okrapdf.com` with header `Authorization: Bearer $OKRA_API_KEY`.

Get a free API key at [okrapdf.com](https://okrapdf.com) (Settings > API Keys).

---

## Upload a PDF

### CLI
```bash
okra extract invoice.pdf
okra extract https://arxiv.org/pdf/2307.09288
okra extract report.pdf --processor llamaparse
okra run report.pdf "What was total revenue?"     # upload + ask in one shot
```

Options: `-o json|markdown|table`, `--processor`, `--tables-only`, `--text-only`, `-d <dir>` (agentic workspace), `-q` (quiet, for piping)

### MCP
```
upload_document(url: "https://example.com/report.pdf")
upload_document(url: "https://arxiv.org/pdf/2307.09288", wait: true)
upload_document(url: "https://example.com/invoice.pdf", page_images: "lazy")
```

Parameters: `url` (required), `wait` (default: true), `document_id` (optional), `page_images` (`none`/`cover`/`lazy`), `processor`

### HTTP
```bash
# From URL
curl -X POST https://api.okrapdf.com/v1/documents \
  -H "Authorization: Bearer $OKRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://arxiv.org/pdf/2307.09288"}'

# From file
curl -X POST https://api.okrapdf.com/v1/documents \
  -H "Authorization: Bearer $OKRA_API_KEY" \
  -F "file=@report.pdf" -F "page_images=cover"
```

Response: `{"document_id": "doc-abc123", "phase": "extracting", "pages_total": 42}`

---

## Check Status

### CLI
```bash
okra status doc-abc123
```

### MCP
```
get_document_status(document_id: "doc-abc123")
```

### HTTP
```bash
curl https://api.okrapdf.com/v1/documents/doc-abc123/status \
  -H "Authorization: Bearer $OKRA_API_KEY"
```

Response: `{"phase": "complete", "page_count": 42, "total_nodes": 318}`

Documents must reach `phase: "complete"` before reading/asking. Use `wait: true` on upload (MCP) or poll status.

---

## Read Content

### CLI
```bash
okra read doc-abc123
okra page get doc-abc123 1
okra toc doc-abc123
okra tree doc-abc123
okra search doc-abc123 "revenue"
```

### MCP
```
read_document(document_id: "doc-abc123")
read_document(document_id: "doc-abc123", pages: "1-5")
read_document(document_id: "arxiv:2307.09288")
```

`document_id` accepts: `doc-abc123`, `arxiv:2307.09288`, or `https://arxiv.org/pdf/2307.09288`.

### HTTP
```bash
# Full markdown
curl https://api.okrapdf.com/v1/documents/doc-abc123/full.md \
  -H "Authorization: Bearer $OKRA_API_KEY"

# Specific page
curl "https://api.okrapdf.com/v1/documents/doc-abc123/pages/3" \
  -H "Authorization: Bearer $OKRA_API_KEY"

# All pages as JSON
curl https://api.okrapdf.com/v1/documents/doc-abc123/pages \
  -H "Authorization: Bearer $OKRA_API_KEY"
```

---

## Ask Questions

### CLI
```bash
okra chat doc-abc123
okra chat send doc-abc123 -m "What are the key findings?"
```

### MCP
```
ask_document(document_id: "doc-abc123", question: "What was total revenue in 2024?")
```

Returns answer with page citations (page number + supporting snippet).

### HTTP (OpenAI-compatible)
```bash
curl -X POST https://api.okrapdf.com/document/doc-abc123/chat/completions \
  -H "Authorization: Bearer $OKRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "What was total revenue in 2024?"}],
    "stream": false
  }'
```

Supports `"stream": true` for SSE streaming.

---

## Extract Structured Data

### CLI
```bash
okra extract report.pdf -o json -q | jq '.entities[] | select(.type == "table")'
```

### MCP
```
extract_data(
  document_id: "doc-abc123",
  prompt: "Extract all line items from this invoice",
  json_schema: {
    "type": "object",
    "properties": {
      "line_items": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "description": {"type": "string"},
            "quantity": {"type": "number"},
            "unit_price": {"type": "number"},
            "total": {"type": "number"}
          }
        }
      },
      "grand_total": {"type": "number"}
    }
  }
)
```

### HTTP
```bash
curl -X POST https://api.okrapdf.com/document/doc-abc123/chat/completions \
  -H "Authorization: Bearer $OKRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Extract all line items"}],
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "invoice",
        "schema": {
          "type": "object",
          "properties": {
            "line_items": {"type": "array", "items": {"type": "object", "properties": {"description": {"type": "string"}, "amount": {"type": "number"}}}},
            "total": {"type": "number"}
          }
        },
        "strict": true
      }
    },
    "stream": false
  }'
```

---

## Tables and Entities

### CLI
```bash
okra tables doc-abc123
okra tables get doc-abc123 table-0
okra entities list doc-abc123
okra entities images doc-abc123
okra query doc-abc123 "table:has(revenue)"
```

### HTTP
```bash
curl https://api.okrapdf.com/v1/documents/doc-abc123/entities/tables \
  -H "Authorization: Bearer $OKRA_API_KEY"

curl https://api.okrapdf.com/v1/documents/doc-abc123/entities \
  -H "Authorization: Bearer $OKRA_API_KEY"
```

---

## Collections

Group documents and query across all of them at once.

### Create and manage

**CLI:**
```bash
okra collections create "Q4 Earnings" -d "Quarterly filings" --docs doc-abc123,doc-def456
okra collections list                          # or: okra col ls
okra collections show "Q4 Earnings"
okra collections add "Q4 Earnings" doc-ghi789
okra collections remove "Q4 Earnings" doc-abc123
okra collections delete "Q4 Earnings"
```

**HTTP:**
```bash
# Create with seed documents
curl -X POST https://api.okrapdf.com/v1/collections \
  -H "Authorization: Bearer $OKRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Q4 Earnings", "document_ids": ["doc-abc123", "doc-def456"]}'

# Add documents
curl -X POST https://api.okrapdf.com/v1/collections/col-xxx/documents \
  -H "Authorization: Bearer $OKRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"document_ids": ["doc-ghi789"]}'

# List / get / delete
curl https://api.okrapdf.com/v1/collections -H "Authorization: Bearer $OKRA_API_KEY"
curl https://api.okrapdf.com/v1/collections/col-xxx -H "Authorization: Bearer $OKRA_API_KEY"
curl -X DELETE https://api.okrapdf.com/v1/collections/col-xxx -H "Authorization: Bearer $OKRA_API_KEY"
```

### Query across documents

Two modes:

| Mode | Behavior | Best for |
|------|----------|----------|
| `fanout` (default) | Separate completion per document, NDJSON stream | Per-document answers |
| `sandbox` | Single LLM with grep/Python over all docs | Cross-doc search, comparisons |

**CLI:**
```bash
okra chat -c "Q4 Earnings" -m "Compare revenue across companies"
okra chat "compare revenue" --doc doc-abc123,doc-def456
```

**HTTP (fanout):**
```bash
curl -X POST https://api.okrapdf.com/v1/collections/col-xxx/query \
  -H "Authorization: Bearer $OKRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "What was total revenue in Q4?"}'
```

Response (NDJSON):
```
{"type":"start","query_id":"...","doc_count":7}
{"type":"result","doc_id":"doc-xxx","answer":"..."}
{"type":"done","completed":7,"failed":0}
```

**HTTP (sandbox):**
```bash
curl -X POST https://api.okrapdf.com/v1/collections/col-xxx/query \
  -H "Authorization: Bearer $OKRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Compare R&D spending. Show a table.", "mode": "sandbox"}'
```

### Export
```bash
# NDJSON stream
curl -N "https://api.okrapdf.com/v1/collections/col-xxx/export?format=markdown" \
  -H "Authorization: Bearer $OKRA_API_KEY"

# Zip archive
curl -L "https://api.okrapdf.com/v1/collections/col-xxx/export?format=zip" \
  -H "Authorization: Bearer $OKRA_API_KEY" -o collection.zip
```

---

## Exports

```bash
# CLI
okra extract report.pdf -o json -q > report.json

# HTTP
curl https://api.okrapdf.com/exports/doc-abc123/markdown -H "Authorization: Bearer $OKRA_API_KEY"
curl -o report.xlsx https://api.okrapdf.com/exports/doc-abc123/excel -H "Authorization: Bearer $OKRA_API_KEY"
curl -o report.docx https://api.okrapdf.com/exports/doc-abc123/docx -H "Authorization: Bearer $OKRA_API_KEY"
curl https://api.okrapdf.com/exports/doc-abc123/snapshot -H "Authorization: Bearer $OKRA_API_KEY"
```

---

## Page Images

Deterministic, CDN-cached URLs:

```
https://res.okrapdf.com/v1/documents/{id}/pg_1.png
https://res.okrapdf.com/v1/documents/{id}/w_400,h_300/pg_1.png
```

---

## Document Management

### CLI
```bash
okra list
okra read doc-abc123
okra status doc-abc123
okra delete doc-abc123
okra auth set-key YOUR_API_KEY
okra auth whoami
```

### HTTP
```bash
curl "https://api.okrapdf.com/v1/documents?limit=20" -H "Authorization: Bearer $OKRA_API_KEY"
```

---

## Subagent & Parallel Patterns

OkraPDF is built for agent-to-agent use. Each document is an isolated Durable Object with its own SQLite — queries to different documents never contend. Run them in parallel freely.

### As tools inside an agent loop

Map each document to a callable tool. The orchestrating agent picks which docs to query:

```ts
import { createOkra } from '@okrapdf/runtime';

const okra = createOkra({ apiKey: process.env.OKRA_API_KEY! });

const docs = [
  { id: 'doc-abc123', label: 'NVIDIA 10-K' },
  { id: 'doc-def456', label: 'AMD 10-K' },
  { id: 'doc-ghi789', label: 'Intel 10-K' },
];

// Each doc becomes a tool the agent can call
const sessions = Object.fromEntries(
  docs.map((d) => [d.label, okra.sessions.from(d.id)]),
);

// Execute in parallel when agent calls multiple tools at once
const results = await Promise.all(
  toolCalls.map(tc => sessions[tc.name].prompt(tc.input.question))
);
```

### Fan-out: same question across N documents

```ts
// SDK — fire all in parallel, collect answers
const question = 'What was total revenue and YoY growth?';
const answers = await Promise.all(
  docIds.map(id => okra.sessions.from(id).prompt(question))
);
```

```bash
# curl — parallel background requests
for doc_id in doc-abc123 doc-def456 doc-ghi789; do
  curl -s -X POST "https://api.okrapdf.com/document/$doc_id/chat/completions" \
    -H "Authorization: Bearer $OKRA_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"messages\": [{\"role\": \"user\", \"content\": \"$question\"}], \"stream\": false}" &
done
wait
```

```bash
# CLI — multi-doc in one command
okra chat "compare revenue" --doc doc-abc123,doc-def456,doc-ghi789
```

### MCP subagent pattern (Claude Code)

When Claude Code spawns subagents, each can independently call OkraPDF MCP tools:

```
# Subagent 1: ask_document(document_id: "doc-abc123", question: "What was revenue?")
# Subagent 2: ask_document(document_id: "doc-def456", question: "What was revenue?")
# Subagent 3: ask_document(document_id: "doc-ghi789", question: "What was revenue?")
# All run concurrently — no contention
```

### When to use which pattern

| Pattern | Best for |
|---------|----------|
| **MCP tools** | Agent picks which docs to query dynamically |
| **SDK `Promise.all`** | You know the doc set upfront, want max parallelism |
| **Collections query** | Same question across a predefined group, server handles fan-out |
| **`okra chat --doc`** | Quick CLI comparison of 2-5 docs |

---

## Piping and Scripting

```bash
# Batch extract
for pdf in *.pdf; do okra extract "$pdf" -o json -q > "${pdf%.pdf}.json"; done

# Fan-out: same question to multiple docs in parallel
for doc_id in doc-abc123 doc-def456 doc-ghi789; do
  curl -s -X POST "https://api.okrapdf.com/document/$doc_id/chat/completions" \
    -H "Authorization: Bearer $OKRA_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"messages\": [{\"role\": \"user\", \"content\": \"What was total revenue?\"}], \"stream\": false}" &
done
wait
```

---

## Available Processors

| Processor | Best For | Speed |
|-----------|----------|-------|
| textlayer | Native PDFs with selectable text | Fast |
| llamaparse | Complex layouts, mixed content | Medium |
| unstructured | General purpose | Medium |
| azure-di | Forms, invoices, receipts | Medium |
| docai | High-accuracy OCR | Slow |
| gemini | Vision-based extraction | Medium |
| qwen | Open-source VLM extraction | Medium |

---

## Error Codes

| Status | Meaning |
|--------|---------|
| 202 | Accepted, processing async |
| 400 | Bad request |
| 401 | Missing or invalid API key |
| 404 | Document not found |
| 409 | Conflict (document exists) |
| 429 | Rate limited |

## Links

- [Documentation](https://docs.okrapdf.com)
- [API Reference](https://api.okrapdf.com)
- [MCP Endpoint](https://api.okrapdf.com/mcp)
- [SDK](https://github.com/okrapdf/sdk)
