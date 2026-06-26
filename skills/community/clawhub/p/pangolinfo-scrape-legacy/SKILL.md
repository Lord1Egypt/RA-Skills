---
name: pangolin-serp
description: >
  Search Google and scrape Amazon using Pangolin APIs. Supports AI Mode search
  (Google AI Overview with multi-turn dialogue), standard SERP with AI Overview
  extraction, Amazon product/keyword/category scraping, and screenshot capture.
  Use when needing to search Google programmatically, get AI overviews, scrape
  SERP results, perform multi-turn Google AI search, or extract Amazon product
  data. Requires PANGOLIN_EMAIL and PANGOLIN_PASSWORD env vars (or PANGOLIN_TOKEN).
---

# Pangolin SERP & Scrape

**New canonical (AI SERP):** https://clawhub.ai/pangolinfo/pangolinfo-ai-serp  
**Amazon skill:** https://clawhub.ai/pangolinfo/pangolinfo-amazon-scraper

Search Google and scrape Amazon programmatically via Pangolin APIs. Extract AI overviews, organic search results, Amazon product data, and page screenshots.

## Prerequisites

- **Python 3.6+** (uses only standard library)
- **Pangolin account** at [pangolinfo.com](https://www.pangolinfo.com)
- **Environment variables** (one of):
  - `PANGOLIN_TOKEN` -- existing bearer token
  - `PANGOLIN_EMAIL` + `PANGOLIN_PASSWORD` -- for automatic login

## Quick Start

### AI Mode Search (Google AI Overview)

```bash
python3 scripts/pangolin.py --q "what is quantum computing" --mode ai-mode
```

### Standard SERP with AI Overview

```bash
python3 scripts/pangolin.py --q "how does java work" --mode serp --screenshot
```

### Multi-Turn Dialogue

```bash
python3 scripts/pangolin.py --q "python web frameworks" --mode ai-mode \
  --follow-up "compare flask vs django" \
  --follow-up "which is better for beginners"
```

### Amazon Product Detail

```bash
python3 scripts/pangolin.py --url "https://www.amazon.com/dp/B0DYTF8L2W" --mode amazon
```

### Amazon Keyword Search

```bash
python3 scripts/pangolin.py --q "wireless mouse" --mode amazon --parser amzKeyword
```

## Workflow

1. **Authenticate** -- Token resolved from env var, cache (`~/.pangolin_token`), or fresh login
2. **Choose API mode** -- `ai-mode` | `serp` | `amazon`
3. **Execute** -- Script builds the request, calls the API with retry logic
4. **Parse output** -- Structured JSON to stdout

## Usage

### AI Mode (`--mode ai-mode`)

Uses `parserName: "googleAISearch"` with `udm=50` to get Google AI Mode results.

```bash
python3 scripts/pangolin.py --q "explain machine learning" --mode ai-mode
```

Output includes `ai_overview` with content paragraphs and source references.

### AI Overview SERP (`--mode serp`)

Uses `parserName: "googleSearch"` for standard SERP results with AI overview extraction.

```bash
python3 scripts/pangolin.py --q "best programming languages 2025" --mode serp
```

Output includes both `organic_results` and optional `ai_overview`.

### Multi-Turn Follow-Up

Add follow-up questions to an AI Mode search. Keep to 5 or fewer for optimal performance (more is allowed but slower):

```bash
python3 scripts/pangolin.py --q "kubernetes" --mode ai-mode \
  --follow-up "how to deploy" \
  --follow-up "monitoring tools" \
  --follow-up "cost optimization"
```

### Amazon (`--mode amazon`)

Scrape Amazon product data using various parsers.

**Product detail by URL:**
```bash
python3 scripts/pangolin.py --url "https://www.amazon.com/dp/B0DYTF8L2W" --mode amazon
```

**Keyword search:**
```bash
python3 scripts/pangolin.py --q "mechanical keyboard" --mode amazon --parser amzKeyword
```

**Best sellers:**
```bash
python3 scripts/pangolin.py --url "https://www.amazon.com/gp/bestsellers/electronics" \
  --mode amazon --parser amzBestSellers
```

**With custom zipcode and raw HTML:**
```bash
python3 scripts/pangolin.py --url "https://www.amazon.com/dp/B0DYTF8L2W" \
  --mode amazon --zipcode 90210 --format rawHtml
```

**Available Amazon parsers:**

| Parser | Use Case |
|--------|----------|
| `amzProductDetail` | Single product page (default) |
| `amzKeyword` | Keyword search results |
| `amzProductOfCategory` | Category listing |
| `amzProductOfSeller` | Seller's products |
| `amzBestSellers` | Best sellers ranking |
| `amzNewReleases` | New releases ranking |
| `amzFollowSeller` | Product variants / other sellers |

### Authentication Only

```bash
python3 scripts/pangolin.py --auth-only
```

### Raw API Response

```bash
python3 scripts/pangolin.py --q "test" --mode ai-mode --raw
```

### All CLI Options

```
--q QUERY          Search query
--url URL          Target URL (for Amazon product pages, category pages, etc.)
--mode MODE        ai-mode (default) | serp | amazon
--screenshot       Capture page screenshot (Google only)
--follow-up TEXT   Follow-up question (repeatable, ai-mode only)
--num N            Number of results (default: 10, Google only)
--parser PARSER    Amazon parser name (default: amzProductDetail)
--zipcode CODE     Amazon zipcode (default: 10041)
--format FMT       Amazon response format: json (default) | rawHtml | markdown
--auth-only        Authenticate and show token info
--raw              Output raw API response
```

## Choosing the Right API

| Feature | AI Mode | SERP | Amazon |
|---------|---------|------|--------|
| Parser | `googleAISearch` | `googleSearch` | `amz*` (7 types) |
| Input | `--q` | `--q` | `--url` or `--q` |
| Primary output | AI-generated answer | Organic results + AI overview | Product data |
| Multi-turn | Yes (via `--follow-up`) | No | No |
| Screenshot | Yes | Yes | No |
| Best for | AI answers | Search results with AI context | Product & market data |
| Cost | 2 credits | 2 credits | 1 credit (json) / 0.75 (raw) |

## Output Format

### Google (ai-mode / serp)

```json
{
  "success": true,
  "task_id": "...",
  "results_num": 1,
  "ai_overview_count": 1,
  "ai_overview": [{"content": ["..."], "references": [{"title": "...", "url": "...", "domain": "..."}]}],
  "organic_results": [{"title": "...", "url": "...", "text": "..."}],
  "screenshot": "https://..."
}
```

### Amazon

```json
{
  "success": true,
  "task_id": "...",
  "url": "https://www.amazon.com/dp/...",
  "results_count": 1,
  "product": {"asin": "...", "title": "...", "price": "...", "star": "...", "rating": "..."}
}
```

See reference files for full response schemas.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | API error (non-zero response code) |
| 2 | Usage error (invalid arguments) |
| 3 | Network error |
| 4 | Authentication error |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Auth fails | Check `PANGOLIN_EMAIL` and `PANGOLIN_PASSWORD` env vars |
| Empty AI overview | Not all queries trigger AI overview; try informational queries |
| Token invalid (1004) | Script auto-refreshes; ensure email/password env vars are set |
| Insufficient credits (2001) | Top up at pangolinfo.com |
| Timeout | Script retries 3x with backoff; check network |
| Amazon returns empty | Verify the URL and parser match (e.g. product URL + `amzProductDetail`) |

See [references/error-codes.md](references/error-codes.md) for the full error code reference.

## Deep-Dive Documentation

| Reference | Content |
|-----------|---------|
| [references/ai-mode-api.md](references/ai-mode-api.md) | AI Mode API schema, multi-turn dialogue mechanism |
| [references/ai-overview-serp-api.md](references/ai-overview-serp-api.md) | AI Overview SERP API schema, organic result structure |
| [references/amazon-api.md](references/amazon-api.md) | Amazon Scrape API, all parser types, product fields |
| [references/error-codes.md](references/error-codes.md) | Error codes, auth lifecycle, credit management |
