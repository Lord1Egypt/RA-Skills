---
name: market-intelligence-claw
description: >
  Real-time strategic intelligence layer for ecommerce and digital businesses.
  Use this skill whenever the user asks about competitors, market trends, pricing,
  keyword research, customer sentiment, brand monitoring, or any strategic business
  decision — even if phrased casually. Triggers include: "what are my competitors doing",
  "is this trending", "how should I price this", "research this niche", "who are my
  competitors", "what do customers think about X", "find market gaps", "give me a
  competitor report", "what's trending", "how is my brand doing", "build a business
  profile", "keyword research for my product", or any request to understand the
  external market landscape. This skill performs LIVE market research using real APIs.
  Always use it proactively when the user is making any strategic business decision.
compatibility: "Tiered tool stack — works fully on free tier (web_search only). Unlockable upgrades: SerpApi (serpapi.com) for SERP/Shopping/Trends/Amazon data, DataForSEO (dataforseo.com) for keyword + SEO intelligence, Rainforest API (rainforestapi.com) for deep Amazon data, NewsAPI (newsapi.org) for news monitoring, Reddit API for community sentiment. No keys required to install. API credentials are session-only and never persisted."
---

# Market Intelligence Skill

A full-capability, real-time strategic intelligence system. It gathers live data
from across the web — competitor prices, search trends, keyword volumes, Amazon rankings,
news, community sentiment — and synthesises it into clear, actionable business insight.

---

## ARCHITECTURE OVERVIEW

This skill uses a **tiered tool stack**. Each tier adds capability:

```
TIER 0 — FREE BASELINE (zero setup, always works)
├── Built-in web_search
│   └── Competitor discovery, brand mentions, pricing research,
│       Reddit sentiment via Google, news headlines, trend signals

TIER 1 — SERP & MARKET DATA (~$50/mo or pay-as-you-go)
├── SerpApi  (serpapi.com)
│   ├── Google Shopping → live competitor prices across all retailers
│   ├── Google Trends   → 0–100 interest scores, breakout queries, regional data
│   ├── Google News     → structured news monitoring
│   ├── Amazon Search   → Amazon pricing, reviews, bestseller ranks
│   └── Google Search   → structured organic + ad results, related questions
└── Rainforest API  (rainforestapi.com / trajectdata.com)
    └── Deep Amazon data → full product details, review breakdowns,
        bestseller rank history, Q&A, seller data, ASIN lookups

TIER 2 — SEO & KEYWORD INTELLIGENCE (pay-as-you-go, ~$0.0006/request)
└── DataForSEO  (dataforseo.com)
    ├── Keyword Research → search volumes, CPC, competition, trends
    ├── SERP Analysis    → who ranks for what, featured snippets
    ├── Competitor SEO   → traffic estimates, organic keywords, backlinks
    └── Google Ads data  → keyword difficulty, CPC benchmarks

TIER 3 — NEWS & BRAND MONITORING (free 100 req/day dev tier)
└── NewsAPI  (newsapi.org)
    └── 150,000+ global news sources, real-time articles,
        brand monitoring, competitor press, industry trends

TIER 4 — COMMUNITY SENTIMENT (free with OAuth)
└── Reddit API  (reddit.com/dev/api)
    └── Unfiltered community discussions, product opinions,
        unmet needs, brand comparisons
```

Before starting any research task, check which tiers the user has configured.
Read `references/setup.md` to guide them through adding keys if they want more power.

---

## STEP 0 — FIRST-USE CONSENT & SETUP

On first use, show this clearly:

> ### Quick setup — takes 1 minute
>
> I can research your market right now using free web search. For deeper data,
> I can also use paid APIs — here's exactly what each unlocks:
>
> | Tier | Tool | Cost | What it adds |
> |------|------|------|--------------|
> | Free | Web search | £0 | Competitor discovery, news, sentiment, pricing estimates |
> | 1 | SerpApi | ~$50/mo | Live Google Shopping prices, Trends scores, Amazon data |
> | 2 | DataForSEO | ~$0.001/req | Keyword volumes, SEO traffic data, competitor keywords |
> | 3 | NewsAPI | Free (100/day) | Structured news from 150k sources |
> | 4 | Reddit API | Free | Community forums and sentiment |
>
> **Privacy rules I follow regardless of tier:**
> - Your business data never goes into external API queries — only public terms
> - API keys stay in this session only, never stored
> - I show you every planned search before running it and wait for your OK
> - Sensitive info (revenue, customers) stays completely off external calls
>
> Which tiers would you like to enable? Or say "just use free" to start immediately.

---

## STEP 1 — BUILD BUSINESS PROFILE

Collect conversationally before any research. Update as user shares more.

```yaml
Business Profile:
  name:            # brand/business name
  industry:        # Fashion / Electronics / Beauty / Food / SaaS / etc.
  products:        # main products or categories
  price_position:  # Budget / Mid-range / Premium / Luxury
  target_customer: # who they sell to (age, location, interests)
  platforms:       # Shopify / Amazon / Instagram / own website / etc.
  competitors:     # known competitors (ask for 1–3 to start)
  geography:       # primary market (country and/or city)
  goals:           # what they're trying to achieve right now
```

**Never collect or store:** exact revenue, customer personal data, private pricing formulas, internal system credentials.

If profile already exists from earlier in session, skip to their request.

---

## STEP 2 — PRE-RESEARCH PLAN (mandatory before any external call)

Before executing, always show a Research Plan:

```
📋 RESEARCH PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 # │ Search / Query                        │ Tool          │ Cost
───┼───────────────────────────────────────┼───────────────┼──────────
 1 │ "running shoes India" (Shopping)      │ SerpApi       │ 1 credit
 2 │ "running shoes" trends 12mo India     │ SerpApi       │ 1 credit
 3 │ "best running shoe brands India 2025" │ Web search    │ Free
 4 │ "Nike India" news last 30 days        │ NewsAPI       │ 1 req
 5 │ keyword data: "running shoes India"   │ DataForSEO    │ ~$0.001
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Estimated cost: 2 SerpApi credits, 1 NewsAPI request, ~$0.001 DataForSEO
 Approve? [Yes / Adjust / Skip paid calls]
```

Wait for explicit confirmation. "Yes, go ahead" approves this plan only.

---

## STEP 3 — INTELLIGENCE MODULES

Six modules. Each has a dedicated reference file. Read it before executing.

| Module | Triggers | Reference |
|--------|----------|-----------|
| 🔍 Competitor Analysis | "who are my competitors", "what is [brand] doing" | `references/competitor.md` |
| 📈 Trend Analysis | "is X trending", "market trends", "what's hot" | `references/trends.md` |
| 💰 Pricing Intelligence | "how to price", "am I too expensive", "competitor prices" | `references/modules-2.md` |
| 🔑 Keyword & SEO Intel | "keyword research", "what do people search for", "SEO" | `references/keywords-seo.md` |
| 📰 News & Brand Monitoring | "brand mentions", "industry news", "competitor news" | `references/modules-2.md` |
| 💬 Sentiment & Community | "what do customers think", "Reddit opinion", "reviews" | `references/modules-2.md` |

---

## STEP 4 — OUTPUT FORMATS

### Competitor Card
```
🏢 [NAME]  ·  [URL]  ·  Sells on: [platforms]
Pricing:   $X–$Y  vs your $Z  →  [X]% [cheaper/more expensive]
SEO:       Ranks for [N] keywords, ~[X]k monthly visits (est.)
Sentiment: ✅ [strength]  ❌ [top complaint]
News:      [anything notable in last 30 days, or "quiet"]
Threat:    🔴 High / 🟡 Medium / 🟢 Low
Sources:   [list tools used]
```

### Trend Report
```
📈 TREND: [Topic]  ·  [geography]
Direction:     ↑ Rising / → Stable / ↓ Falling
Interest now:  [0–100] vs 6mo ago: [0–100] vs 12mo ago: [0–100]
Breakouts:     🔥 "[query]" (+[X]%) · 🔥 "[query]" (Breakout)
Peak regions:  [where interest is highest]
Opportunity:   Immediate / 3–6 months / Long-term
Recommendation: [1 specific sentence tied to Business Profile]
Sources:       [tools used]
```

### Pricing Snapshot
```
💰 PRICING: [Category]  ·  [N] products sampled
Floor: $X  ·  Median: $Y  ·  Ceiling: $Z
Your price: $[A]  →  [Budget / Mid / Premium / Luxury]
Best value competitor: [Brand] at $[price] with ⭐[rating]
Recommendation: [specific, with rationale]
Sources: [tools used]
```

### Keyword Intelligence
```
🔑 KEYWORD: "[term]"  ·  [geography]
Monthly searches: [X]k   Competition: Low/Med/High   CPC: $[Y]
Related high-value: "[term2]" ([X]k), "[term3]" ([X]k)
You currently rank: [position or "not ranking"]
Top-ranking competitor: [Brand] · [page type]
Quick win: [specific recommendation]
Sources: DataForSEO / web research
```

### Opportunity Matrix
```
🗺️ OPPORTUNITY: [Market/Niche]
Market interest:  [score/signal]   Competition: [level]
Entry difficulty: [Low/Med/High]   Trend:       ↑/→/↓
Identified gaps:  [1–3 specific gaps]
Best entry angle: [recommendation]
Risk level:       🟢/🟡/🔴
Sources: [tools used]
```

---

## STEP 5 — STRATEGIC CLOSE

End every output with a "What this means for you" block:

> 💡 **For [Business Name]:**
> - [Specific, data-backed action tied to their goals]
> - [Opportunity spotted — e.g. competitor weakness]
> - [Risk flagged if any]

Keep it concrete, short, and directly actionable.

---

## SECURITY & DATA RULES (non-negotiable, always apply)

1. **No private data in external queries** — only public brand names, product categories, geography
2. **Session-only keys** — API credentials never repeated back in full, never persisted
3. **Confirm before every paid call** — show cost, wait for yes
4. **Limited-scope key advice** — when guiding key setup, always recommend read-only scopes + monthly spend caps
5. **Graceful fallback** — if any API fails or is absent, fall back silently to web_search and note it in sources
6. **Source every claim** — every data point must state which tool produced it
7. **Quota tracking** — count API calls used per session; report if asked

---

## SESSION BRIEFING (returning users)

If a Business Profile is already established, offer:
> "Welcome back! Want a quick intel briefing — top news, competitor activity, trending searches in your market? (Free, ~3 web searches)"

If yes: run a lightweight scan using only web_search. No paid calls unless approved.
