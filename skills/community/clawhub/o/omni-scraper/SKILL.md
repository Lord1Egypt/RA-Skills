---
name: omni-scraper
version: 1.0.1
description: "Scrape any URL and get structured data back. Amazon product pages and search results are automatically parsed into clean JSON (title, price, rating, BSR, reviews, search rankings). API access provided by Claw School — no third-party scraping account needed. Requires a CLAW_KEY from claw-school.com. Trigger on: scrape, crawl, fetch page, get product data, Amazon search results, 爬取, 抓取."
---

# omni-scraper

Scrape any webpage via Claw School's proxy. Amazon URLs return structured JSON automatically — no HTML parsing needed.

## Setup

You need a `CLAW_KEY` from [claw-school.com](https://claw-school.com). Purchase one and set it in your agent environment:

```
CLAW_KEY=CLAW-XXXX-XXXX-XXXX-XXXX
```

## Scrape a URL

```bash
curl -s -X POST "$CLAW_API_BASE/api/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "claw_key": "'"$CLAW_KEY"'",
    "url": "URL_HERE",
    "mode": "scraper"
  }'
```

**Mode options:**
- `scraper` — headless browser, handles JS-rendered pages (default, use for Amazon)
- `proxy` — raw HTTP, faster for static pages and REST endpoints

## Optional parameters

| Field | Type | Description |
|---|---|---|
| `mode` | string | `"scraper"` or `"proxy"` (default: `"scraper"`) |
| `js_snippet` | string | JavaScript to execute after page load (scraper only) |
| `country` | string | Two-letter country code for geo-targeting, e.g. `"US"`, `"JP"` |

## Response format

**Amazon product page (PDP)** — structured fields extracted automatically:
```json
{
  "url": "https://www.amazon.com/dp/B07DN8ZJRL",
  "status": 200,
  "parsed": {
    "asin": "B07DN8ZJRL",
    "title": "Echo Dot (3rd Gen)",
    "price": "$29.99",
    "rating": "4.7 out of 5 stars",
    "review_count": "847,231 ratings",
    "bought_past_month": "10K+ bought in past month",
    "bsr": ["#1 in Smart Speakers"],
    "badges": ["Amazon's Choice"],
    "bullet_points": ["..."],
    "reviews": [{ "author": "...", "rating": "5.0", "title": "...", "body": "..." }]
  },
  "body": null,
  "error": null
}
```

**Amazon search page (SERP)** — ranked results with pricing:
```json
{
  "url": "https://www.amazon.com/s?k=iphone+case",
  "status": 200,
  "parsed": {
    "keyword": "iphone case",
    "result_count": 48,
    "results": [
      {
        "position": "1",
        "asin": "B0XXXXX",
        "title": "...",
        "price": "$12.99",
        "rating": "4.7 out of 5 stars",
        "review_count": "23,456 ratings",
        "bought_past_month": "5K+ bought in past month",
        "sponsored": false,
        "ac_badge": "Amazon's Choice"
      }
    ]
  },
  "body": null,
  "error": null
}
```

> **Note:** If `parsed` fields are sparse (parse quality low), the response includes `body` with raw HTML as fallback so you can extract data yourself.

**Any other URL** — raw HTML in `body`:
```json
{ "url": "https://example.com", "status": 200, "parsed": null, "body": "<html>...</html>", "error": null }
```

## Error codes

| code | meaning |
|---|---|
| `KEY_NOT_FOUND` | CLAW_KEY is invalid |
| `KEY_NOT_ACTIVATED` | Key exists but hasn't been activated yet — visit claw-school.com |
| `KEY_BLOCKED` | Key suspended or revoked — contact support |
| `UPSTREAM_TIMEOUT` | Target site is slow, retry once |

## Get a CLAW_KEY

Visit [claw-school.com](https://claw-school.com) to purchase access.
Each key is tied to one agent. Keys do not expire.
