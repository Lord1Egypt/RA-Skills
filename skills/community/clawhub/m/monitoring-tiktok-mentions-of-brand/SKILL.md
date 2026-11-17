---
name: monitoring-tiktok-mentions-of-brand
description: >
  Monitors TikTok for brand mentions and product discussions using apidojo's TikTok scraper on Apify.
  Triggers when the user asks to: track mentions of a brand on TikTok, monitor TikTok hashtags for
  brand content, find TikTok videos talking about a product or company, see what TikTok says about
  a brand this week, track TikTok reactions to a product launch, find TikTok creators who mentioned
  a competitor brand, monitor brand sentiment on TikTok, or discover viral TikTok content about a
  specific brand or product.
  Returns creator handle, views, likes, comments, sentiment signal, and video caption excerpt.
  Ideal for brand managers, community teams, crisis communications, and product marketing teams.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/tiktok-scraper
---

# Monitoring TikTok Mentions of a Brand

Tracks TikTok content mentioning a brand via branded hashtags and keyword searches. TikTok is the fastest-moving platform for brand sentiment — viral criticism or praise can emerge in hours.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | TikTok URLs — user profiles, hashtags, music pages, search, locations |
| `keywords` | array | Optional | `[]` | Search keywords/terms to find posts |
| `sortType` | string | Optional | `RELEVANCE` | Sort order for keyword results: `RELEVANCE`, `MOST_LIKED`, `DATE_POSTED` |
| `location` | string | Optional | — | ISO 3166-1 alpha-2 country code for regional filtering (e.g. `US`, `GB`) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return across the run |
| `includeSearchKeywords` | boolean | Optional | `false` | Add the matched search keyword field to each post |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Run tiktok-scraper for branded hashtags
- [ ] Step 2: Filter by view count and date
- [ ] Step 3: Classify sentiment and content type
- [ ] Step 4: Identify trending posts and crisis signals
- [ ] Step 5: Deliver monitoring report
```

### Step 1: Run the Actor


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tiktok-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tiktok-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tiktok-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tiktok-scraper"
Input:
{
  "keywords": ["#[BRAND]", "#[BRAND]review", "#[BRAND]honest"],
  "maxItems": 200
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~tiktok-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{
    "keywords": ["#[brand]", "#[brand]review", "#[brand]honest"],
    "maxItems": 200
  }'
```

### Step 2: Classify and Score

**Content type:**
```
UNBOXING = "unboxing", "first impression", "first look"
REVIEW = "review", "honest", "real talk", "thoughts on"
COMPLAINT = "disappointed", "refund", "scam", "doesn't work", "returning"
TUTORIAL = "how to", "tips", "tutorial"
ENTERTAINMENT = trend audio, no product focus
```

**Sentiment** (lexical — same model as Twitter sentiment skill):
- Use positive/negative/neutral indicators
- Weight by `diggCount` (likes) as community agreement signal

**Virality signal:**
```
virality = playCount / (follower_count_of_creator + 1)
```
If `virality > 2.0`: post is reaching well beyond the creator's audience — flag as `TRENDING`

### Step 3: Crisis Detection

Flag `CRISIS_ALERT` when:
- Any single post with `playCount > 500K` AND `sentiment = NEGATIVE`
- More than 5 complaint posts in 48 hours
- Comment-to-view ratio > 3% on a negative post (high engagement = controversy)

### Step 4: Edge Cases

- **Hashtag overloaded with unrelated content**: Add brand sub-product or model name to narrow
- **Brand has low TikTok presence** (< 10 posts): This is notable data — report it; brand may need proactive TikTok strategy
- **Duet/Stitch posts about brand**: These count as mentions but are often reactions to original content — classify as `REACTION` and note the source video

## Output Format

```
# TikTok Brand Monitor: [BRAND_NAME]
Period: [DATE_RANGE] | Posts collected: [N] | Total estimated reach: [N] views | Date: [DATE]

## Overall Sentiment
Positive: [X%] | Negative: [X%] | Neutral: [X%]
⚠️ CRISIS ALERTS: [N] (posts above threshold — see below)

## Content Type Distribution
Unboxing: [N] | Reviews: [N] | Complaints: [N] | Tutorials: [N]

## Trending Posts (> 100K Views)
| Creator | @Handle | Views | Likes | Sentiment | Type | Caption Preview |
|---------|---------|-------|-------|-----------|------|----------------|

## CRISIS ALERTS (Negative + High Reach)
| Creator | Views | Complaint Theme | Days Live | Post URL |
|---------|-------|----------------|-----------|---------|

## Top Advocates
| Creator | @Handle | Followers | Views | Post Type | Score |
|---------|---------|-----------|-------|----------|-------|
```

## Troubleshooting

**Very few posts found**: Brand may be using a different hashtag convention. Try product name without brand (`#[product]` not `#[brand]product`).
**All results are unboxing/haul content**: Normal for consumer brands — this is positive. Set monitoring to alert only on negative content.
**Crisis alert triggered by troll campaign**: Check if complaint posts are from a cluster of new accounts (created within 30 days, < 100 followers) — may be coordinated; note this context in report.

