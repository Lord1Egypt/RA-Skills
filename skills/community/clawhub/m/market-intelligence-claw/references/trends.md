# Trend Analysis Module

## Research Plan Template

```
📋 TREND RESEARCH PLAN: [topic]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 # │ Query                                  │ Tool                   │ Cost
───┼────────────────────────────────────────┼────────────────────────┼───────
 1 │ "[topic]" trends 12mo [geo]            │ SerpApi Trends*        │ 1cr
 2 │ Trending now [geo]                     │ SerpApi TrendingNow*   │ 1cr
 3 │ "[topic]" keyword volume               │ DataForSEO*            │ ~$0.001
 4 │ "[topic]" on Google Shopping           │ SerpApi Shopping*      │ 1cr
 5 │ "[topic] trending 2025" news           │ NewsAPI* / Web search  │ free/1req
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Execution Steps

### 1. Google Trends (Tier 1)
```
engine=google_trends, q=[topic], data_type=TIMESERIES, date=today 12-m, geo=[country code]
```
Extract from `interest_over_time.timeline_data`:
- Score now (most recent month)
- Score 6 months ago
- Score 12 months ago

Compare to determine direction: rising / stable / falling

Also pull `related_queries.rising[]` for breakout terms.
"Breakout" means >5000% growth — a genuinely emerging sub-trend.

**Compare multiple terms:**
`q=[term1],[term2],[term3]` (comma-separated, max 5)
Use this to benchmark the user's product against related search terms.

**Seasonality check:**
`date=today 5-y` — reveals whether the trend is seasonal or evergreen.

### 2. Real-Time Trending Now (Tier 1)
```
engine=google_trends_trending_now, geo=[country code e.g. IN]
```
Filter `trending_searches[]` by `categories[].name` matching user's industry.
Flag anything with `increase_percentage > 100` in their category.

### 3. Keyword Volume Validation (Tier 2)
```
POST /v3/keywords_data/google_ads/search_volume/live
{ "keywords": ["[trend topic]", "[related term]"], "location_name": "[geo]" }
```
Cross-reference with Trends score to validate:
- High Trends score + high search volume = strong validated trend
- High Trends score + low search volume = niche/emerging (still an opportunity)

### 4. Market Supply Check (Tier 1 or Web)
```
engine=google_shopping, q=[trend topic]
```
Count results and quality of listings:
- Few/thin results + high trend interest = market gap opportunity
- Many strong listings = competitive but validated

### 5. News Validation (Tier 3 or Web)
```
GET /v2/everything?q="[trend topic]"&sortBy=publishedAt
```
- Multiple recent articles = mainstream traction, trend is real
- No articles = early stage niche (can be first mover advantage)

### 6. Trend Interpretation

| Pattern | Interpretation | Recommendation |
|---------|---------------|----------------|
| Scores 70–100 sustained for 12mo | Mature, stable | Safe to enter, expect competition |
| Rising 20→80 in 6–12 months | Fast growth | Act now — window open |
| Peaked at 100, now 40–60 | Post-peak stabilising | Entering maturing market |
| Peaked, now <20 | Declining | Avoid unless strong differentiation angle |
| Annual spikes | Seasonal | Plan campaigns around peak months |
| Consistent <20 | Niche | Small market — validate with keyword volume |
| Breakout queries with <100 Shopping results | Emerging gap | High opportunity |

---

## Output: Trend Report

```
📈 TREND: [Topic]  ·  [Geography]  ·  [Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIRECTION   ↑ Rising / → Stable / ↓ Falling
INTEREST    Now: [score]/100  ·  6mo ago: [score]  ·  12mo ago: [score]

BREAKOUT QUERIES (fastest growing)
  🔥 "[query]" — [X]% increase (or "Breakout")
  📈 "[query]" — [X]% increase

PEAK REGIONS    [where interest is highest]
SEARCH VOLUME   [X]k searches/month  ·  CPC: $[Y]  (DataForSEO)
MARKET SUPPLY   [N] Shopping results — [thin/moderate/saturated]
NEWS SIGNAL     [Active coverage / Emerging / Minimal]

OPPORTUNITY WINDOW   Immediate / 3–6 months / Long-term
SEASONAL?            [Yes — peaks in {months} / No — evergreen]

RECOMMENDATION FOR [BUSINESS NAME]
  [2–3 sentences, specific and tied to their products/platforms]

SOURCES   [list of tools used]
```
