---
name: google-news
description: >-
  A Google News API alternative on fetcher.sh — pay-per-call in USDC via
  x402, or prepaid credits with a Bearer key, no RSS scraping. Use when the
  user wants keyword search across Google News scoped to a language edition,
  section headlines (world, business, technology, entertainment, sport,
  science, health, or a specific topic ID), the latest headlines, a list of
  supported language-region codes, or to decode a Google News redirect URL
  into the real article URL. Also covers news monitoring, headline
  aggregation, media tracking, and press-mention alerts without scraping
  Google News' RSS feeds directly.
keywords:
  - google-news
  - google-news-api
  - news-api-alternative
  - headline-monitoring
  - media-monitoring
  - x402
  - ai-agent
---

# Google News API

Google News headlines and search as clean JSON — one plain HTTP GET per call,
paid as you go. No RSS feed scraping, no redirect-URL decoding by hand, no
undocumented internal endpoints.

Base URL: `https://google-news.fetcher.sh`

## Authentication

Two ways to pay, same data — full mechanics in the [`fetcher`
skill](../fetcher/SKILL.md):

```bash
# 1. Prepaid credits (recommended — get a key at https://fetcher.sh/topup
#    or via POST /api/credits/topup, see the fetcher skill)
export FETCHER_API_KEY="bby_live_xxxxxxxxxxxx"
curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  "https://google-news.fetcher.sh/api/search?keyword=hello&languageCode=en-US"

# 2. x402 pay-per-call — omit the header; a GET with no payment returns 402
#    with machine-readable payment requirements (USDC on Base, Polygon,
#    Arbitrum, Monad, or Solana). @x402/fetch signs and retries automatically.
```

Every response is `{ "status": number, "message": string, "data": ... }`; the
HTTP status mirrors `status`.

## Endpoints (12 — all GET, $0.005/call)

| Endpoint | What it returns |
| --- | --- |
| `/api/search` | Headlines matching a keyword, in one language edition |
| `/api/latest` | Latest headlines |
| `/api/world` | World section headlines |
| `/api/business` | Business section headlines |
| `/api/technology` | Technology section headlines |
| `/api/entertainment` | Entertainment section headlines |
| `/api/sport` | Sport section headlines |
| `/api/science` | Science section headlines |
| `/api/health` | Health section headlines |
| `/api/topic/{topicId}` | Headlines for an arbitrary topic ID |
| `/api/language-regions` | Every supported `languageCode` value |
| `/api/decode-article-url` | Resolves a Google News redirect URL to the real article URL |

`languageCode` (e.g. `en-US`, `en-GB`, `fr-FR`) is **required on every
endpoint except `/api/language-regions`**, which takes no parameters at all
and exists specifically to list the valid values. `keyword` is additionally
required on `/api/search`; `url` is required on `/api/decode-article-url`.

## Scenarios

**Keyword search, US English edition:**

```bash
curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  --data-urlencode "keyword=stablecoin regulation" -G \
  --data-urlencode "languageCode=en-US" \
  "https://google-news.fetcher.sh/api/search"
```

**Same search, UK English edition:**

```bash
curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  --data-urlencode "keyword=ai policy" -G \
  --data-urlencode "languageCode=en-GB" \
  "https://google-news.fetcher.sh/api/search"
```

**Section headlines (technology, business):**

```bash
curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  --data-urlencode "languageCode=en-US" -G \
  "https://google-news.fetcher.sh/api/technology"

curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  --data-urlencode "languageCode=en-US" -G \
  "https://google-news.fetcher.sh/api/business"
```

**Headlines for a specific topic ID:**

```bash
curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  --data-urlencode "languageCode=en-US" -G \
  "https://google-news.fetcher.sh/api/topic/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGxqTVdZU0FtVnVHZ0pWVXlnQVAB"
```

**List every supported language/region code before picking one:**

```bash
curl -H "Authorization: Bearer $FETCHER_API_KEY" \
  "https://google-news.fetcher.sh/api/language-regions"
```

**Decode a Google News redirect URL into the real article link:**

```bash
curl -H "Authorization: Bearer $FETCHER_API_KEY" -G \
  --data-urlencode "url=https://news.google.com/rss/articles/CBMi..." \
  "https://google-news.fetcher.sh/api/decode-article-url"
```

## MCP

```json
{
  "mcpServers": {
    "google-news": {
      "url": "https://google-news.fetcher.sh/mcp",
      "headers": { "Authorization": "Bearer bby_live_..." }
    }
  }
}
```

Free: `search_endpoints`, `describe_endpoint`, `check_balance`. Paid:
`fetch_data` (any endpoint above), `topup_credits`, plus the named shortcut
`google_news_search`. Drop the `headers` block to pay per call with x402
instead — see the [`fetcher` skill](../fetcher/SKILL.md) for the full flow.

## Errors

- `400` — missing/invalid parameter (message names it) — most commonly a
  missing `languageCode`
- `401` — unknown or rotated key
- `402` — payment required (x402 challenge) or `topup_required` (credits
  exhausted)
- `404` — not a priced path
- No rate limits; no refunds on upstream failures (settlement precedes
  delivery)

## Reference

- Full agent setup: <https://google-news.fetcher.sh/skill.md>
- OpenAPI 3.1 contract: <https://google-news.fetcher.sh/openapi.json>
- Condensed catalog: <https://google-news.fetcher.sh/llms.txt>
- Payment, credits, and MCP deep dive: [`fetcher` skill](../fetcher/SKILL.md)
- Site: <https://google-news.fetcher.sh>
