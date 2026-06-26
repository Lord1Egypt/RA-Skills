# Pricing Intelligence Module

## Research Plan Template

```
📋 PRICING RESEARCH PLAN: [product category]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 # │ Query                                  │ Tool            │ Cost
───┼────────────────────────────────────────┼─────────────────┼───────
 1 │ "[product] [geo]" on Google Shopping   │ SerpApi*        │ 1cr
 2 │ "[product]" on Amazon [domain]         │ Rainforest API* │ ~$0.001
 3 │ "[product] price" across web           │ Web search      │ Free
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Execution Steps

### 1. Google Shopping Sweep (Tier 1)
```
engine=google_shopping, q="[product category] [geo]"
```
Collect all `extracted_price` values.
Calculate: floor (lowest 10%), median, ceiling (top 10%).
Group by brand/source to identify competitor pricing.
Note: `rating` and `reviews` alongside each price — reveals price-quality relationship.

### 2. Amazon Pricing (Tier 1b Rainforest or Tier 1 SerpApi)

**Rainforest API (richer):**
```
GET https://api.rainforestapi.com/request
  ?api_key={KEY}&type=search&q=[product]&amazon_domain=amazon.in
```
Returns: `search_results[].price.value`, `.rating`, `.ratings_total`, `.bestseller_rank`

**SerpApi Amazon (simpler):**
```
engine=amazon, q=[product], amazon_domain=amazon.in
```

### 3. Price-Quality Analysis

For each competitor: plot `price` vs `rating` vs `review count`.

Pattern flags:
- High price + high rating + many reviews = **justified premium** (strong, hard to beat)
- High price + low rating = **vulnerable** — opportunity to undercut with better quality
- Low price + high reviews = **price leader** — don't compete on price, compete on quality
- Low price + low reviews = **race to bottom** — avoid this space unless cost is your moat

### 4. Positioning Logic

```
User price vs market median:
  < -20%  → Below floor risk (perceived low quality) → test 15-20% increase
  -20–0%  → Budget tier → fine if intentional; check if premium tier is reachable
  0–+20%  → Mid-market sweet spot → differentiate on value, not price
  +20–60% → Premium → ensure brand signals match (packaging, content, reviews)
  > +60%  → Luxury → full experience must justify: service, exclusivity, brand
```

## Output: Pricing Snapshot

```
💰 PRICING SNAPSHOT: [Category]  ·  [N] products sampled  ·  [geo]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MARKET RANGE
  Floor: $X  ·  Median: $Y  ·  Ceiling: $Z

PRICE TIERS
  Budget (<$X):   [top brands]
  Mid ($X–$Y):    [top brands]
  Premium ($Y+):  [top brands]

YOUR POSITION
  Your price: $[A]  →  [Budget/Mid/Premium/Luxury]
  vs Median: [+/-X]%

TOP COMPETITORS
  [Brand A]: $[price] ·  ⭐[rating] ([N]k reviews) · [platform]
  [Brand B]: $[price] ·  ⭐[rating] ([N]k reviews) · [platform]

PRICE-QUALITY FLAGS
  🔴 [Brand X] — high price, poor reviews — vulnerable
  ✅ [Brand Y] — strong value proposition at $[price]

RECOMMENDATION
  [Specific, with rationale tied to Business Profile goals]

SOURCES  [tools used]
```

---

# News & Brand Monitoring Module

## Research Plan Template

```
📋 NEWS MONITORING PLAN: [brand/topic]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 # │ Query                                  │ Tool          │ Cost
───┼────────────────────────────────────────┼───────────────┼───────
 1 │ "[brand]" news last 30 days            │ NewsAPI*      │ 1 req
 2 │ "[industry]" trends news               │ NewsAPI*      │ 1 req
 3 │ "[brand]" news                         │ SerpApi News* │ 1cr
 4 │ "[brand] news 2025"                    │ Web search    │ Free
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Execution Steps

### NewsAPI (Tier 3)
```
GET https://newsapi.org/v2/everything
  ?q="{brand name}"   ← exact match with quotes
  &language=en
  &sortBy=publishedAt
  &pageSize=10
  &from={YYYY-MM-DD, 30 days ago}
  &apiKey={KEY}
```

Operators: `"brand" AND (launch OR funding OR controversy OR partnership OR expansion)`

### Categorise Articles
- 🟢 **Positive** — funding, awards, growth, good press
- 🔴 **Negative** — lawsuits, recalls, bad PR, leadership exits
- 🟡 **Strategic** — product launches, new markets, partnerships, acquisitions
- ℹ️ **Industry** — general market coverage (context, not company-specific)
- 🚨 **Urgent** — anything requiring immediate attention (crisis, major competitor move)

### Fallback: SerpApi Google News or Web Search
```
engine=google_news, q="{brand}"
```
Or: web_search `"[brand] news [current month year]"`

## Output: News Brief

```
📰 NEWS BRIEF: [Brand/Topic]  ·  Last 30 days
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HEADLINES
  🟢 [Positive headline] — [Source] · [Date]
  🟡 [Strategic headline] — [Source] · [Date]
  🔴 [Negative headline if any] — [Source] · [Date]

KEY TAKEAWAY
  [1–2 sentences: what matters most and why]

IMPLICATIONS FOR [BUSINESS NAME]
  [Specific, actionable observation]

SOURCES  NewsAPI / SerpApi Google News / Web search
```

---

# Sentiment & Community Module

## Research Plan Template

```
📋 SENTIMENT RESEARCH PLAN: [brand/product]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 # │ Query                                    │ Tool          │ Cost
───┼──────────────────────────────────────────┼───────────────┼───────
 1 │ site:reddit.com "[brand]" review         │ Web search    │ Free
 2 │ "[brand]" Reddit top posts last year     │ Reddit API*   │ Free
 3 │ "[brand]" Amazon reviews breakdown       │ Rainforest*   │ ~$0.001
 4 │ "[brand]" problems / alternative         │ Web search    │ Free
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 All free except Rainforest (optional for Amazon review data)
```

## Execution Steps

### 1. Reddit Search (Tier 4 or web_search fallback)

**Reddit API:**
```
GET https://oauth.reddit.com/search.json
  ?q="{brand or product}"&sort=top&t=year&limit=25
```

**Web search (always works):**
- `site:reddit.com "{brand}" review`
- `site:reddit.com "{product type}" recommendation`
- `site:reddit.com "{brand}" worth it`
- `site:reddit.com "{brand}" alternative`
- `site:reddit.com "{product}" problems`

### Key subreddits by industry
| Industry | Subreddits |
|----------|-----------|
| Fashion | r/femalefashionadvice, r/malefashionadvice, r/streetwear |
| Electronics | r/gadgets, r/hardware, r/headphones |
| Beauty/Skincare | r/SkincareAddiction, r/MakeupAddiction |
| Fitness | r/Fitness, r/bodyweightfitness, r/running |
| India-specific | r/india, r/IndiaShopping, r/IndiaFinance |
| General | r/BuyItForLife, r/frugal, r/deals |

### 2. Amazon Review Breakdown (Tier 1b Rainforest)
```
GET https://api.rainforestapi.com/request
  ?api_key={KEY}&type=reviews&asin=[ASIN]&amazon_domain=amazon.in
```

Returns: `summary.rating` (avg), `summary.ratings_total`, `summary.rating_breakdown` (1–5 star counts)
High 1-star % = systemic problems. Read top critical reviews for specific complaint themes.

### 3. Categorise Sentiment Themes
- ✅ **Praised for:** (what people love, use to position your USP if competitor)
- ❌ **Complained about:** (top issues — note frequency and emotional intensity)
- 🔄 **Switching reason:** (why people leave — your opportunity if competitor)
- 💬 **Common questions:** (reveals information gaps — content opportunities)
- 💡 **Expressed wishes:** ("I wish it had X" — product gap opportunities)

### Privacy Rule
Only analyse publicly available content. Never request or process customer PII.
If the user asks to analyse their own customers' private communications, decline: "I can only analyse public reviews and discussions, not private customer data."

## Output: Sentiment Report

```
💬 SENTIMENT REPORT: [Brand/Product]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERALL    ✅ [X]% positive  ⚪ [Y]% neutral  ❌ [Z]% negative
           (Estimated from review themes and community tone)

WHAT PEOPLE LOVE ✅
  • [Theme 1] — "..." (representative quote, paraphrased)
  • [Theme 2]
  • [Theme 3]

TOP COMPLAINTS ❌
  • [Theme 1] — appears in [X]% of critical reviews
  • [Theme 2]

WHY PEOPLE SWITCH AWAY 🔄
  • [Reason 1]
  • [Reason 2]

UNMET NEEDS 💡
  • "[Direct community wish]"
  • "[Product feature people want that doesn't exist yet]"

WHAT THIS MEANS FOR [BUSINESS NAME]
  [2–3 specific observations connecting sentiment to their strategy]

SOURCES  Reddit (API/web) · Amazon reviews (Rainforest) · web search
```
