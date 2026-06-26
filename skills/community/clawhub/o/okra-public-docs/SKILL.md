---
name: okra-public-docs
description: Query pre-extracted public documents via OkraPDF MCP — arxiv AI papers, SEC 10-K/10-Q filings, and more. Read, ask questions, extract structured data. No upload needed.
---

# OkraPDF Public Documents

Pre-extracted public document corpora queryable via MCP. No upload, no waiting — documents are already parsed and indexed. Just pass an ID and start asking questions.

## Available Channels

| Channel | Coverage | Auth | ID Format |
|---------|----------|------|-----------|
| **Arxiv AI papers** | 400+ papers from cs.AI, cs.CL, cs.LG (updated weekly) | API key required | `arxiv:2603.26653` |
| **SEC filings** | Mag7 + FinanceBench (~80 companies), 10-K and 10-Q | No auth needed | Ticker-based (`NVDA`) |

## Setup

### Arxiv papers (authenticated MCP)

Add to `~/.claude/mcp.json` (Claude Code) or `.cursor/mcp.json` (Cursor):

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

Get a free API key at [okrapdf.com](https://okrapdf.com) (Settings > API Keys).

### SEC filings (zero-auth MCP)

```json
{
  "mcpServers": {
    "okra-sec": {
      "type": "url",
      "url": "https://mcp.okrapdf.com/mcp"
    }
  }
}
```

No API key, no signup. Restart your agent after adding.

---

## Arxiv Papers

400+ recent AI research papers parsed with Docling OCR on GPU — tables, equations, figures, and full text preserved as structured markdown.

### Read a paper

```
read_document(document_id: "arxiv:2603.26653")
read_document(document_id: "arxiv:2603.26653", pages: "1-5")
read_document(document_id: "https://arxiv.org/pdf/2603.26653")
```

No upload needed — papers are pre-indexed as public sources. Just pass the arxiv ID.

### Ask questions

```
ask_document(document_id: "arxiv:2603.26653", question: "What is the main contribution?")
ask_document(document_id: "arxiv:2603.26653", question: "What were the benchmark results on MMLU?")
ask_document(document_id: "arxiv:2603.18272", question: "How is retrieval-augmented experience used?")
```

Returns answer with page citations.

### Extract structured data

```
extract_data(
  document_id: "arxiv:2603.26653",
  prompt: "Extract all benchmark results with model names, dataset names, and scores",
  json_schema: {
    "type": "object",
    "properties": {
      "benchmarks": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "model": {"type": "string"},
            "dataset": {"type": "string"},
            "metric": {"type": "string"},
            "score": {"type": "number"}
          }
        }
      }
    }
  }
)
```

### Literature survey workflow

```
# Read abstracts from several papers
read_document(document_id: "arxiv:2603.26499", pages: "1")
read_document(document_id: "arxiv:2603.26266", pages: "1")

# Ask targeted questions
ask_document(document_id: "arxiv:2603.26499", question: "What bottlenecks in AI research does this address?")

# Same question across papers for comparison
ask_document(document_id: "arxiv:2603.18272", question: "How does this handle multi-agent coordination?")
ask_document(document_id: "arxiv:2603.07379", question: "How does this handle multi-agent coordination?")
```

### Discover papers

**Semantic Scholar** (free, no key needed for basic use):
```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=agentic+RAG&year=2026&fields=externalIds,title,citationCount&limit=10" \
  | jq '.data[] | {arxiv: .externalIds.ArXiv, title, citations: .citationCount}'
```

**Arxiv RSS feeds** (same feeds used to build the collection):
```
https://rss.arxiv.org/rss/cs.AI    # Artificial Intelligence
https://rss.arxiv.org/rss/cs.CL    # Computation and Language (NLP)
https://rss.arxiv.org/rss/cs.LG    # Machine Learning
```

**Papers With Code:**
```bash
curl -s "https://paperswithcode.com/api/v1/papers/?q=agentic+RAG&items_per_page=5" | jq '.results[] | {title, arxiv_id}'
```

### Current snapshot

411 papers from cs.AI (~200), cs.CL (~100), cs.LG (~200). Full manifest in [`papers.json`](papers.json).

If a paper isn't found, upload it yourself with `upload_document`.

### Tips

- Use `arxiv:XXXX.XXXXX` format (not full URL) for cleaner queries
- `pages: "1"` reads just the abstract/intro quickly
- For survey papers (50+ pages), use `ask_document` instead of reading everything
- `extract_data` with JSON schemas is ideal for pulling benchmark tables

---

## SEC Filings

Pre-extracted SEC 10-K and 10-Q filings. No API key, no signup, completely free.

### Available tools

| Tool | Purpose |
|------|---------|
| `read_filing_index` | Browse available filings, filter by ticker/type |
| `read_filing_contents` | Get full extracted text as markdown |
| `ask_question` | AI-powered Q&A with citations, single or cross-company |
| `get_verification_summary` | Check extraction quality page-by-page |
| `verify_pages` | Approve or flag pages for quality control |

### Browse filings

```
read_filing_index()
read_filing_index(ticker: "NVDA")
read_filing_index(ticker: "AAPL", filing_type: "10-K")
```

Always start here to see what's available.

### Ask questions (single company)

```
ask_question(question: "What was NVIDIA's data center revenue?", tickers: ["NVDA"])
ask_question(question: "List all risk factors related to AI regulation", tickers: ["MSFT"])
ask_question(question: "What are the outstanding debt obligations?", tickers: ["TSLA"], filing: "10-k-2024")
```

### Cross-company comparison (up to 10 tickers)

```
ask_question(
  question: "Compare R&D spending as a percentage of revenue",
  tickers: ["AAPL", "MSFT", "GOOGL", "NVDA", "META", "AMZN", "TSLA"]
)

ask_question(
  question: "Which company has the highest gross margin?",
  tickers: ["AAPL", "MSFT", "GOOGL"]
)

ask_question(
  question: "Summarize each company's AI strategy",
  tickers: ["NVDA", "AMD", "INTC"]
)
```

Fans out to each company's filing in parallel, then synthesizes a cross-company answer.

### Read full filing text

```
read_filing_contents(ticker: "TSLA", filing: "10-k-2024")
```

Filing slug formats (all equivalent): `10-k-2024`, `10-K/2024`, `2024-10K`.

### Extraction quality audit

```
get_verification_summary(document_id: "doc-xxx")
get_verification_summary(document_id: "doc-xxx", status: "needs_review")
verify_pages(document_id: "doc-xxx", action: "approve", confidence_above: 0.9)
verify_pages(document_id: "doc-xxx", action: "flag", pages: [67], reason: "Table has merged cells")
```

### Available companies

**Mag7:** AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA

**FinanceBench:** ~80 companies including major banks (JPM, BAC, GS), pharma (PFE, JNJ, ABBV), industrials (GE, MMM, CAT), and more.

Use `read_filing_index()` to browse the full catalog. New filings added as published.

### Tips

- Start with `read_filing_index` before querying
- `ask_question` with multiple tickers is the fastest way to compare — no need to read each filing
- Cross-company queries work best with clear, quantitative questions
- Verification tools require `document_id` (not ticker) — get it from other tool responses
