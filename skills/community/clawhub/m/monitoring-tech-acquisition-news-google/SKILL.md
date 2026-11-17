---
name: monitoring-tech-acquisition-news-google
description: >
  Monitors tech acquisition news and M&A activity using apidojo's Google Search scraper. Triggers when the user asks to: track tech acquisition news, monitor M&A activity in a sector on Google, find recent tech company acquisitions, track acquisition announcements in a technology category, monitor who is being acquired in a startup ecosystem, find companies that were recently acquired or merged, or research M&A trends in an industry.
  Returns acquisition announcements, acquirer and target company, deal size signals, and strategic rationale.
  Ideal for M&A analysts, startup founders, investors, and competitive intelligence teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/google-search-scraper
---

# Monitoring Tech Acquisition News Google

Executes monitoring tech acquisition news google using apidojo scrapers. Part of the apidojo intelligence skills library.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | Google search URLs |
| `searchTerms` | array | Optional | `[]` | Keywords to search on Google |
| `countryCode` | string | Optional | `US` | Country for Google search (e.g. `US`, `GB`, `TR`) |
| `languageCode` | string | Optional | — | Language for results (e.g. `en`) |
| `maxItems` | number | Optional | Unlimited | Maximum results to return across all queries |
| `maxPagesPerQuery` | integer | Optional | `1` | Maximum result pages per query |
| `mobileResults` | boolean | Optional | `false` | Fetch mobile SERP layout |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Define parameters
- [ ] Step 2: Run google-search-scraper
- [ ] Step 3: Filter and classify results
- [ ] Step 4: Score by quality and relevance
- [ ] Step 5: Deliver output
```

### Step 2: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~google-search-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~google-search-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~google-search-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~google-search-scraper"
Input:
{
  "searchTerms": ["[SECTOR] acquisition 2026", "[SECTOR] acquired", "[COMPANY] acquires"],
  "maxItems": 100
}
```

**REST API fallback:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~google-search-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"searchTerms": ["[SECTOR] acquisition 2026", "[SECTOR] acquired", "[COMPANY] acquires"], "maxItems": 100}'
```

Wait for `SUCCEEDED`. Fetch dataset:
```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN"
```

### Step 3: Classify Results

```
classification: CONFIRMED (official announcement) | REPORTED (press rumor) | RUMORED (speculation) | DENIED
```

### Step 4: Score Each Result

```
score = deal_significance = (named_price ? deal_value/1000000 : 0.5) * 0.50 + (acquirer_is_public ? 1 : 0.5) * 0.30 + (coverage_from_tier1_pub ? 1 : 0.5) * 0.20
```

### Step 5: Edge Cases

- **M&A news often breaks before official press releases; use Google News search type to catch breaking reports, and flag STATUS = UNCONFIRMED until official press release found**

Additional fallbacks:
- **< 20 results**: Broaden search terms; remove secondary filters
- **No results**: Verify the search terms are correct; try alternate phrasings
- **Data quality issues**: Remove entries with missing key fields; note count in output

## Output Format

```
# Monitoring Tech Acquisition News Google
Results: [N] | Date: [DATE]

| # | [Key Field] | [Metric 1] | [Metric 2] | [Classification] | [Score] |
|---|------------|-----------|-----------|-----------------|---------|
| 1 | [value] | [value] | [value] | [type] | [0.XX] |

## Summary
Top result: [description]
Key finding: [insight]
```

## Troubleshooting

**Too few results:** Broaden the primary search term; remove restrictive filters.
**Low quality results:** Apply minimum score threshold (≥ 0.50) to filter noise.
**Actor fails to run:** Verify API key; check actor status at apify.com/apidojo.

