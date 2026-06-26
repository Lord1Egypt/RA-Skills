# Competitor Analysis Module

## Research Plan Template

Before executing, show this plan and get user approval:

```
📋 COMPETITOR RESEARCH PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 # │ Query                                    │ Tool        │ Cost
───┼──────────────────────────────────────────┼─────────────┼───────
 1 │ "best [category] brands [geo]"           │ Web search  │ Free
 2 │ "[category] price comparison [geo]"      │ SerpApi*    │ 1cr
 3 │ "[Competitor A] [product]"               │ SerpApi*    │ 1cr
 4 │ SEO traffic: competitor.com              │ DataForSEO* │ ~$0.001
 5 │ "[Competitor A]" news last 30 days       │ NewsAPI*    │ 1 req
 6 │ site:reddit.com "[Competitor A]" review  │ Web search  │ Free
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 * = only if that tier is configured
 Approve?
```

---

## Execution Steps

### 1. Discover Competitors

**Web search (always):**
- `"best [product category] brands [geography] 2025"`
- `"[product type] alternatives"`
- `"[product type] [geography] online store"`

Target: 3–5 meaningful competitors. Start with the user's known list, expand from search.

**SerpApi Google Search (if Tier 1):**
```
engine=google, q="best [category] [geo]"
```
Mine `organic_results[].displayed_link` for competitor domains.
Mine `related_searches[].query` for discovery signals.
Mine `related_questions[]` for what buyers are actually asking.

---

### 2. Pricing Intelligence

**SerpApi Google Shopping (if Tier 1):**
```
engine=google_shopping, q="[product category] [geo]"
```
Collect all `extracted_price` values.
Group by brand to find each competitor's price range.
Calculate: floor / median / ceiling across all results.

**Rainforest API (if Tier 1b, and competitors sell on Amazon):**
```
type=search, q="[product category]", amazon_domain=amazon.in
```
Extract: `price.value`, `rating`, `ratings_total`, `bestseller_rank`, `asin`

**Web search fallback:**
`"[competitor brand] [product] price"`
Note in output: "Pricing estimated from web search"

---

### 3. SEO & Traffic Estimate

**DataForSEO (if Tier 2):**
```
POST /v3/dataforseo_labs/google/domain_rank_overview/live
{ "target": "competitor.com", "location_name": "[geo]" }
```
Returns: `metrics.organic.etv` (monthly traffic estimate), `metrics.organic.count` (keyword count)

**Web search fallback:**
`"[competitor] monthly visitors"` or `"[competitor] website traffic"` — often picked up by SimilarWeb estimates in snippets.

---

### 4. SEO Keyword Profile

**DataForSEO (if Tier 2):**
```
POST /v3/dataforseo_labs/google/ranked_keywords/live
{ "target": "competitor.com", "location_name": "[geo]", "limit": 20 }
```
Returns top keywords the competitor ranks for — reveals their content strategy.

---

### 5. News & Developments

**NewsAPI (if Tier 3):**
```
GET /v2/everything?q="{competitor name}"&sortBy=publishedAt&from=[30d ago]
```

**SerpApi Google News (if Tier 1, no NewsAPI):**
```
engine=google_news, q="{competitor name}"
```

**Web search fallback:**
`"[competitor] news 2025"`

Flag: funding rounds, product launches, controversies, leadership changes, market exits.

---

### 6. Customer Sentiment

**Reddit API (if Tier 4):**
```
GET /search.json?q="{competitor}"&sort=top&t=year&limit=25
```

**Web search (always effective):**
- `site:reddit.com "{competitor}" review`
- `"{competitor}" problems`
- `"{competitor}" alternative`
- `"{competitor} vs" [user's brand or category]`

**Rainforest reviews (if Tier 1b + Amazon competitor):**
```
type=reviews, asin=[competitor ASIN], amazon_domain=amazon.in
```
Returns: review text samples, rating breakdown (1–5 star counts), verified purchase %

Categorise: ✅ loved, ❌ complaints, 🔄 why people switch, 💡 unmet needs

---

### 7. Threat Scoring

Score each competitor 1–3 on each dimension:

| Dimension | 1 | 2 | 3 |
|-----------|---|---|---|
| Price overlap | Different tier | Partial | Same tier |
| Product overlap | Different | Partial | Direct |
| Market overlap | Different region | Some | Same market |
| Brand strength | Weak | Moderate | Strong |
| Growth signal | Declining | Stable | Growing fast |

Total: 5–7 = 🟢 Low, 8–11 = 🟡 Medium, 12–15 = 🔴 High

---

## Output: Competitor Card

```
🏢 [NAME]  ·  [URL]  ·  Sells on: [platforms]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRICING    $X–$Y  vs your $Z → [X]% [cheaper/more expensive]
           Best listing: "[product]" at $Y with ⭐[rating] ([N]k reviews)
SEO        ~[X]k monthly visits · [N]k organic keywords · [DA score if available]
STRENGTHS  • [Point 1]  • [Point 2]
WEAKNESSES • [Top customer complaint from reviews]  • [Second complaint]
NEWS       [Notable development last 30 days, or "No significant news"]
THREAT     🔴/🟡/🟢 [level] — [one-line rationale]
SOURCES    [list of tools actually used]
```
