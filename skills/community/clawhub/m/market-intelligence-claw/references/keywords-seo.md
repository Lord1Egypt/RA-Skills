# Keyword & SEO Intelligence Module

This module is powered primarily by DataForSEO (Tier 2). It provides keyword volumes,
competition levels, CPC data, and SEO landscape analysis. With only web search,
provide estimated signals using search result counts and Google autocomplete data.

---

## Research Plan Template

```
📋 KEYWORD & SEO PLAN: [topic]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 # │ Query / Action                           │ Tool        │ Cost
───┼──────────────────────────────────────────┼─────────────┼─────────
 1 │ Search volume: "[keyword]"               │ DataForSEO* │ ~$0.001
 2 │ Keyword suggestions for "[seed term]"    │ DataForSEO* │ ~$0.001
 3 │ Who ranks for "[keyword]" in [geo]       │ DataForSEO* │ ~$0.001
 4 │ Competitor.com organic traffic estimate  │ DataForSEO* │ ~$0.001
 5 │ "[keyword] india" autocomplete signals   │ Web search  │ Free
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Estimated DataForSEO cost: ~$0.004 total
```

---

## Execution Steps

### 1. Seed Keyword Search Volume (Tier 2)
```
POST https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live
Body:
[{
  "keywords": ["[keyword 1]", "[keyword 2]", "[keyword 3]"],
  "location_name": "[geo from Business Profile]",
  "language_name": "English"
}]
```

Key response fields per keyword:
- `search_volume` — monthly searches
- `competition` — 0 (low) to 1.0 (high)
- `cpc` — cost per click in Google Ads (proxy for commercial value)
- `monthly_searches[]` — 12-month trend array (reveals seasonality)

**Interpret CPC:**
- CPC > $2 = high commercial intent, competitive space
- CPC $0.50–$2 = moderate
- CPC < $0.50 = low competition or low commercial intent

### 2. Keyword Expansion (Tier 2)
```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live
Body:
[{
  "keyword": "[seed term]",
  "location_name": "[geo]",
  "language_name": "English",
  "limit": 30,
  "filters": [["keyword_info.search_volume", ">", 100]]
}]
```

Sort results by `keyword_info.search_volume` DESC to find highest-opportunity terms.
Flag keywords with high volume + low competition + relevant to business = quick wins.

### 3. SERP Landscape — Who Ranks? (Tier 2)
```
POST https://api.dataforseo.com/v3/serp/google/organic/live/advanced
Body:
[{
  "keyword": "[keyword]",
  "location_name": "[geo]",
  "language_name": "English",
  "device": "desktop",
  "depth": 10
}]
```

From results, note:
- Which domains rank in top 10 (competitor SEO visibility)
- Is there a featured snippet? What type? (Can you beat it?)
- Are there People Also Ask boxes? (Content gap opportunities)
- Ratio of big brands to small sites (lower = easier to compete)

### 4. Competitor Traffic Estimate (Tier 2)
```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live
Body:
[{
  "target": "competitor.com",
  "location_name": "[geo]",
  "language_name": "English"
}]
```

Key fields:
- `metrics.organic.etv` — estimated monthly traffic value ($)
- `metrics.organic.count` — number of keywords they rank for
- `metrics.organic.pos_1` — keywords ranking in position #1

### 5. Competitor Top Keywords (Tier 2)
```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live
Body:
[{
  "target": "competitor.com",
  "location_name": "[geo]",
  "language_name": "English",
  "limit": 20,
  "order_by": ["keyword_data.keyword_info.search_volume,desc"]
}]
```

This reveals exactly what keywords bring the competitor traffic.
Identify which of their top keywords the user is NOT targeting — content gaps.

---

## Web Search Fallback (no DataForSEO)

When DataForSEO is not available, use signals from web search to estimate:

- **Search volume proxy:** Number of Google results for exact phrase `"[keyword]"` in quotes
  - >1B results = very high volume term
  - 100M–1B = high volume
  - 10M–100M = moderate
  - <10M = low volume

- **Competition proxy:** Count how many ads appear on the SERP. More ads = more competition.

- **Keyword suggestions:** Use Google autocomplete signals by searching `"[keyword] "` and noting suggested completions.

- **Who ranks:** Simply run the search and note the top 10 results manually.

Always note in output: "Keyword data estimated from web signals (DataForSEO not configured)"

---

## Output: Keyword Intelligence Card

```
🔑 KEYWORD INTELLIGENCE: "[Seed Term]"  ·  [Geography]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRIMARY TERM
  Monthly searches: [X]k   Competition: Low/Med/High   CPC: $[Y]
  Trend: [↑ Rising / → Stable / ↓ Falling] (12-month)
  Seasonality: [Peak months or "Evergreen"]

HIGH-VALUE RELATED KEYWORDS
  "[term]"   [X]k/mo  ·  [Low/Med/High] comp  ·  $[CPC]
  "[term]"   [X]k/mo  ·  [Low/Med/High] comp  ·  $[CPC]
  "[term]"   [X]k/mo  ·  [Low/Med/High] comp  ·  $[CPC]

QUICK WINS (high volume, low competition)
  "[term]" — [X]k searches, low competition, you could rank here

WHO RANKS (top 5 for primary term)
  1. [Domain] — [page type]
  2. [Domain] — [page type]
  ...

CONTENT GAPS (competitor ranks for, you don't)
  "[term]" — [competitor] gets [X]k/mo from this

RECOMMENDATION
  [Specific action: "Focus your homepage SEO on '[term]'" or
  "Write a comparison article for '[term]'" etc.]

SOURCES  DataForSEO / web signals
```
