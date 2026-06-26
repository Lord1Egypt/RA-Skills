---
name: olostep
description: Scrape webpages, search Google, crawl sites, batch-scrape up to 10k URLs, map site structure, and get AI-powered answers with citations using the Olostep Web Data API. Use when your task needs live web content — research, documentation ingestion, competitor analysis, data extraction, error debugging, or any work that requires real-time information from the internet. Free tier: 500 requests/month at olostep.com.
version: 1.0.3
metadata: {"openclaw": {"homepage": "https://olostep.com", "requires": {"env": ["OLOSTEP_API_KEY"]}, "primaryEnv": "OLOSTEP_API_KEY"}}
---

# Olostep — Web Data API for AI Agents

Fetch live web content via the Olostep API. Covers scraping, searching, crawling, batch processing, site mapping, AI-powered answers, and structured data extraction.

**Authentication:** Every request needs `Authorization: Bearer $OLOSTEP_API_KEY`. If the env var is missing, stop and tell the user to set it. Get a free key (500 req/month) at https://olostep.com/auth.

**Base URL:** `https://api.olostep.com/v1`

---

## 1. Scrape a Single Page

Extract content from any URL as markdown, HTML, JSON, or text. Handles JavaScript rendering and anti-bot protections automatically.

```sh
curl -sS -X POST "https://api.olostep.com/v1/scrapes" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url_to_scrape": "https://example.com/page",
    "formats": ["markdown"]
  }'
```

**Response:** Content is in `result.markdown_content` (or `result.html_content`, `result.text_content`, `result.json_content` depending on requested formats).

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `url_to_scrape` | Yes | — | URL to scrape |
| `formats` | Yes | — | Array: `markdown`, `html`, `text`, `json`, `screenshot` |
| `country` | No | — | Country code for geo-targeted scraping (`US`, `GB`, `IN`) |
| `wait_before_scraping` | No | `0` | Milliseconds to wait for JS rendering (0–10000) |
| `parser` | No | — | Parser object `{"id": "@olostep/google-search"}` for structured JSON |
| `llm_extract` | No | — | Object with `schema` for LLM-based extraction |

**When to use:** Single page extraction — docs, articles, product pages, profiles.

**Tips:**
- Default to `formats: ["markdown"]` — most token-efficient for LLM processing
- For JavaScript-heavy SPAs, set `wait_before_scraping: 2000`
- Use parsers for structured JSON from known sites (see Parsers section)

---

## 2. Search Google

Search Google by scraping a Google URL with the `@olostep/google-search` parser. No separate search endpoint — search goes through `/v1/scrapes`.

```sh
curl -sS -X POST "https://api.olostep.com/v1/scrapes" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url_to_scrape": "https://www.google.com/search?q=best+AI+coding+tools+2026&gl=us",
    "formats": ["json"],
    "parser": {"id": "@olostep/google-search"}
  }'
```

**Response:** `result.json_content` is a **stringified JSON string**. Parse it to get `organic` (array of `{title, link, snippet}`), `knowledgeGraph`, `peopleAlsoAsk`, `relatedSearches`.

**How to build the Google URL:**
- Base: `https://www.google.com/search?q=YOUR+QUERY`
- Add `&gl=us` for country (ISO codes: `us`, `gb`, `de`, `in`)
- URL-encode the query (spaces become `+`)

**When to use:** Research, finding docs, competitive analysis, debugging errors.

---

## 3. Crawl a Website

Async crawl that discovers and scrapes pages by following links. Poll for results.

```sh
# Start crawl
curl -sS -X POST "https://api.olostep.com/v1/crawls" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "start_url": "https://docs.example.com",
    "max_pages": 10
  }'
```

```sh
# Check status (poll until status is "completed")
curl -sS "https://api.olostep.com/v1/crawls/CRAWL_ID" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY"
```

```sh
# Get pages (once completed)
curl -sS "https://api.olostep.com/v1/crawls/CRAWL_ID/pages?limit=10" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY"
```

Pages return `retrieve_id` per page. Use `/v1/retrieve?retrieve_id=ID&formats=markdown` to get content.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `start_url` | Yes | — | Starting URL |
| `max_pages` | Yes | — | Maximum pages to crawl |
| `include_urls` | No | `["/**"]` | Glob patterns to include (`["/blog/**"]`) |
| `exclude_urls` | No | — | Glob patterns to exclude (`["/admin/**"]`) |
| `max_depth` | No | — | Maximum link depth from start URL |

**When to use:** Ingesting docs sites, blog archives, product catalogs.

---

## 4. Batch Scrape URLs

Scrape up to **10,000 URLs** in one parallel batch. Async — poll for results.

```sh
curl -sS -X POST "https://api.olostep.com/v1/batches" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"url": "https://example.com/page1", "custom_id": "page1"},
      {"url": "https://example.com/page2", "custom_id": "page2"}
    ]
  }'
```

```sh
# Check status
curl -sS "https://api.olostep.com/v1/batches/BATCH_ID" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY"
```

```sh
# Get results (once completed)
curl -sS "https://api.olostep.com/v1/batches/BATCH_ID/items?limit=20" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY"
```

Items return `retrieve_id`. Use `/v1/retrieve?retrieve_id=ID&formats=markdown` for content.

**When to use:** Large-scale extraction — product pages, directories, documentation sets.

---

## 5. Map a Website

Discover all URLs on a site without scraping content. **Synchronous** — returns immediately.

```sh
curl -sS -X POST "https://api.olostep.com/v1/maps" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "include_urls": ["/blog/**"],
    "top_n": 50
  }'
```

**Response:** `urls` array of discovered URLs, `urls_count` total.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `url` | Yes | — | Website to map |
| `search_query` | No | — | Sort URLs by relevance |
| `top_n` | No | — | Limit number of URLs |
| `include_urls` | No | — | Glob patterns to include |
| `exclude_urls` | No | — | Glob patterns to exclude |

**When to use:** Site analysis, content auditing, planning before crawl/batch.

---

## 6. AI-Powered Answers

Web-sourced answers with citations. Optionally provide JSON schema for structured output. **Synchronous.**

```sh
curl -sS -X POST "https://api.olostep.com/v1/answers" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "What are the top 5 AI agent frameworks in 2026?"
  }'
```

With structured output:
```sh
curl -sS -X POST "https://api.olostep.com/v1/answers" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Find the founders and funding of Olostep",
    "json_format": {"company": "", "founders": [], "total_funding": "", "last_round": ""}
  }'
```

**Response:** `result.json_content` matches your schema. `result.sources` lists URLs used.

**When to use:** Research, fact-checking, competitive analysis, structured web intelligence.

---

## 7. Retrieve Content by ID

Crawl and batch results return `retrieve_id` per item. Get actual content with:

```sh
curl -sS "https://api.olostep.com/v1/retrieve?retrieve_id=RETRIEVE_ID&formats=markdown" \
  -H "Authorization: Bearer $OLOSTEP_API_KEY"
```

---

## Common Workflows

### Research a topic
1. **Search Google** → find sources
2. **Scrape** top results → get full content
3. Synthesize into deliverable

### Ingest documentation
1. **Map** the docs site → discover URLs
2. **Batch** or **Crawl** relevant sections
3. **Retrieve** content by ID

### Debug an error
1. **Search** the exact error message (in quotes)
2. **Scrape** GitHub issues or Stack Overflow answers
3. Apply the fix

### Extract structured data at scale
1. **Map** to find all product/listing URLs
2. **Batch** with `parser` for structured JSON
3. Retrieve and process results

---

## Available Parsers

Use with `"parser": {"id": "PARSER_ID"}` and `"formats": ["json"]`:

| Parser ID | Use Case |
|-----------|----------|
| `@olostep/google-search` | Google SERP (organic, knowledge graph) |
| `@olostep/amazon-it-product` | Amazon product pages |
| `@olostep/extract-emails` | Email addresses from pages |
| `@olostep/extract-socials` | Social media links |

---

## Rules

- Always check `$OLOSTEP_API_KEY` is set before making requests.
- Default to `formats: ["markdown"]` — most efficient for LLM context.
- Content is inside `result.markdown_content` (not a top-level field).
- Crawls and batches are **async** — poll status before fetching results.
- Only fetch what the current task needs. Do not scrape unnecessarily.
