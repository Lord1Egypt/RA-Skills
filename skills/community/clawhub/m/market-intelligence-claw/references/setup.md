# API Setup Guide

## Philosophy
The skill works out of the box with zero setup using web_search.
Each tier you add gives meaningfully better data. None are required.
All keys are read-only, session-only, and never used beyond approved queries.

When guiding a user through setup, always recommend:
- Create a **dedicated API key** for this skill (never reuse production keys)
- Set the **lowest quota** that fits their use case
- Enable **read-only scopes** wherever the platform allows
- Set a **monthly spend cap** to prevent surprise charges

---

## TIER 1 — SerpApi

**Website:** https://serpapi.com
**What it unlocks:** Live Google Shopping prices, Google Trends (0–100 interest scores + breakout queries), structured Google News, Amazon product data, Google Search with rich features (ads, featured snippets, related questions)
**Pricing:** Free = 100 searches/month. Developer = $50/month for 5,000. Pay-as-you-go available.
**Our recommendation:** Developer plan ($50/mo) is plenty for active daily use. Set a search quota cap in the dashboard.

### Get your key (5 minutes)
1. Go to **serpapi.com** → Sign Up
2. Verify your email
3. In dashboard → **API Key** → copy the key
4. In dashboard → **Billing** → set a monthly usage cap (recommend $10–20 to start)

### What queries look like
Only public search terms are sent — never your business's private data:
- `"wireless earbuds India"` → Google Shopping
- `"athleisure brands"` → Google Trends
- `"Nykaa news"` → Google News

### Engines used in this skill
- `google_shopping` — competitor pricing
- `google_trends` with `data_type=TIMESERIES` — trend direction
- `google_trends_trending_now` — real-time trending topics
- `google_news` — news monitoring
- `amazon` — Amazon product/pricing data
- `google` — organic search results + related questions

---

## TIER 1b — Rainforest API (Amazon depth)

**Website:** https://rainforestapi.com (by Traject Data)
**What it unlocks:** Deep Amazon data — full product details, review summaries, bestseller rank, seller information, Q&A sections, ASIN lookups, review breakdowns by star rating
**Pricing:** Pay-as-you-go. Starts at ~$0.001 per request. Free trial available.
**When to use:** If the user sells on Amazon or has Amazon competitors — provides far richer data than SerpApi Amazon engine.

### Get your key
1. Go to **rainforestapi.com** → Sign Up
2. Verify email and activate account
3. Dashboard → **API Keys** → copy

### Endpoints used
```
GET https://api.rainforestapi.com/request
  ?api_key={KEY}
  &type=search            → search results + prices
  &type=product           → full product detail (by ASIN)
  &type=reviews           → review breakdown
  &type=bestsellers       → category bestseller rankings
  &amazon_domain=amazon.in  → India; amazon.com for US
```

---

## TIER 2 — DataForSEO

**Website:** https://dataforseo.com
**What it unlocks:** Keyword research (search volumes, CPC, competition), SERP rank tracking, competitor SEO traffic estimates, organic keyword portfolios, backlink data, Google Ads keyword data
**Pricing:** Pay-as-you-go only. $50 minimum deposit (credits don't expire). Typical cost: ~$0.0006–$0.002 per request. A small business might spend $5–15/month total.
**Auth:** Login + password (not API key). Self-serve registration available.

### Get credentials
1. Go to **dataforseo.com** → Sign Up
2. Registration is self-serve for individuals (some enterprise features require sales contact)
3. Deposit minimum $50 to activate (unused credits carry forward)
4. Use your login email + password as credentials in API calls

### Auth pattern
```
All requests use HTTP Basic Auth:
  Authorization: Basic base64("{login}:{password}")
```

### Key endpoints used in this skill

**Keyword Research — Search Volume:**
```
POST https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live
Body:
[{
  "keywords": ["running shoes india", "best running shoes"],
  "location_name": "India",
  "language_name": "English"
}]
```
Returns: `search_volume`, `cpc`, `competition` (0–1), monthly trends

**Keyword Suggestions:**
```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live
Body:
[{
  "keyword": "running shoes",
  "location_name": "India",
  "language_name": "English",
  "limit": 20
}]
```

**Competitor SEO Traffic Estimate:**
```
POST https://api.dataforseo.com/v3/dataforseo_labs/google/domain_rank_overview/live
Body:
[{
  "target": "competitor.com",
  "location_name": "India",
  "language_name": "English"
}]
```
Returns: estimated monthly organic traffic, total ranking keywords, traffic value

**SERP Check (who ranks for a keyword):**
```
POST https://api.dataforseo.com/v3/serp/google/organic/live/advanced
Body:
[{
  "keyword": "running shoes india",
  "location_name": "India",
  "language_name": "English",
  "device": "desktop",
  "depth": 10
}]
```

---

## TIER 3 — NewsAPI

**Website:** https://newsapi.org
**What it unlocks:** Real-time articles from 150,000+ global publishers. Full-text search with filters for language, date, source, and relevance.
**Pricing:** Free developer plan = 100 req/day, articles from past month. Paid = $449/month for production (real-time + full history). Free tier is sufficient for most users.

### Get your key (2 minutes)
1. Go to **newsapi.org/register**
2. Fill in email + password → key shown immediately

### Endpoints used
```
GET https://newsapi.org/v2/everything
  ?q="{brand or topic}"
  &language=en
  &sortBy=publishedAt
  &pageSize=10
  &from={30 days ago YYYY-MM-DD}
  &apiKey={KEY}

GET https://newsapi.org/v2/top-headlines
  ?category=business
  &country=in
  &pageSize=10
  &apiKey={KEY}
```

**Query operators supported:**
- `"Nykaa"` — exact match
- `Nykaa AND launch` — both terms
- `Nykaa OR Myntra` — either brand
- `Nykaa -funding` — exclude term

---

## TIER 4 — Reddit API

**Website:** https://reddit.com/dev/api
**What it unlocks:** Raw community conversations — product opinions, brand comparisons, complaints, wishes, recommendations. The most unfiltered customer voice available.
**Pricing:** Free (60 requests/minute with OAuth). Non-commercial use.

### Get credentials (10 minutes)
1. Log in to Reddit (create account if needed)
2. Go to **reddit.com/prefs/apps**
3. Click **Create App** at the bottom
4. Choose type: **script**
5. Name: anything (e.g. "Market Research")
6. Redirect URI: `http://localhost:8080`
7. Click **Create app**
8. Note: **Client ID** (under app name) and **Secret**

### Auth
```
POST https://www.reddit.com/api/v1/access_token
  Authorization: Basic base64("{client_id}:{secret}")
  Content-Type: application/x-www-form-urlencoded
  User-Agent: MarketIntelligenceSkill/1.0

  Body: grant_type=client_credentials
```

### Key endpoints
```
GET https://oauth.reddit.com/search.json?q={query}&sort=top&t=month&limit=25
  Authorization: Bearer {access_token}
  User-Agent: MarketIntelligenceSkill/1.0

GET https://oauth.reddit.com/r/{subreddit}/search.json
  ?q={query}&restrict_sr=true&sort=top&t=year&limit=25
```

### Fallback without Reddit API
Use web_search: `site:reddit.com "{brand}" review`
Achieves the same results via Google's Reddit indexing.
Note in output: "Source: Reddit via web search"

---

## Key Safety Practices (always enforce)

| Rule | Detail |
|------|--------|
| Dedicated keys | One key per skill, not shared with other services |
| Spend caps | Set in each provider's dashboard before activating |
| Read-only | DataForSEO and NewsAPI are read-only by nature. SerpApi is read-only. |
| No PII in queries | Never send customer names, emails, order IDs to any external API |
| Session expiry | Remind users their keys only live in this conversation |
| Partial key display | If confirming a key is set, show only last 4 chars: `...ab3f` |
