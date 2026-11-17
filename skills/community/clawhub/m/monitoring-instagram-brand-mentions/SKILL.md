---
name: monitoring-instagram-brand-mentions
description: >
  Monitors Instagram for brand mentions and tagged posts using apidojo's Instagram scraper on Apify.
  Triggers when the user asks to: track Instagram mentions of a brand or product, monitor hashtag
  activity around a brand on Instagram, find posts where users tag or mention a company on Instagram,
  discover organic brand sentiment on Instagram, find untagged brand mentions in captions,
  track user-generated content featuring a brand, or monitor competitor mentions on Instagram.
  Returns post URL, caption, author handle, likes, comments, timestamp, and mention type.
  Ideal for brand managers, social listening teams, PR agencies, and community managers.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/instagram-scraper
---

# Monitoring Instagram Brand Mentions

Tracks all public Instagram posts mentioning a brand — via branded hashtags, @mentions, or product name keywords. Classifies mentions by sentiment and type (UGC, complaint, press coverage, competitor comparison).

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | ✅ | `[]` | Instagram URLs — profiles, hashtags, locations, audio pages, reels |
| `until` | string | Optional | — | Scrape posts until this date (YYYY-MM-DD) |
| `maxItems` | number | Optional | Unlimited | Maximum posts to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Build hashtag and keyword list
- [ ] Step 2: Run instagram-scraper for each hashtag
- [ ] Step 3: Classify mention type and sentiment
- [ ] Step 4: Identify top advocates and critics
- [ ] Step 5: Deliver brand health report
```

### Step 1 & 2: Run instagram-scraper


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~instagram-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~instagram-scraper"
Input:
{
  "keywords": ["#[BRAND]", "#[BRAND]review", "#[BRAND]community"],
  "maxItems": 100
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~instagram-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"keywords": ["#[brand]", "#[brand]review"], "maxItems": 100}'
```

Run for each hashtag cluster. Merge results and deduplicate by `postUrl`.

### Step 2: Classify Mentions

**Mention type:**
```
UGC = post contains product photo + brand mention; author is not verified
COMPLAINT = caption contains negative indicators: "broken", "disappointed", "scam", "refund", "terrible", "never again"
POSITIVE_REVIEW = caption contains: "love", "amazing", "best", "recommend", "obsessed"
PRESS/EDITORIAL = author is verified OR follower_count > 100K
COMPETITOR_COMPARISON = caption mentions competitor brand alongside this brand
```

**Sentiment:** Apply same lexical classification as Twitter sentiment skill (positive/negative/neutral indicators).

### Step 3: Score Reach

```
mention_reach = likes + comments * 5 + (followers_of_author / 100)
```

### Step 4: Edge Cases

- **Official brand account's own posts in results**: Drop posts where `ownerUsername` = brand's own handle
- **Hashtag is overloaded** (> 1M posts): Use long-tail branded hashtags instead; or filter by date
- **Sentiment misclassified for complex posts**: Flag posts with both positive and negative indicators as `MIXED`; report count
- **Foreign language mentions dominant**: Report language distribution; flag non-English mentions separately

## Output Format

```
# Instagram Brand Mention Monitor: [BRAND]
Posts collected: [N] | Period: [DATE_RANGE] | Date: [DATE]

## Mention Type Distribution
UGC: [N] | Positive Reviews: [N] | Complaints: [N] | Press: [N] | Comparisons: [N]

## Sentiment Summary
Positive: [X%] | Negative: [X%] | Neutral: [X%]
Weighted by reach: Positive [X%] | Negative [X%]

## Top UGC Posts (Most Liked)
| Creator | @Handle | Likes | Type | Caption Excerpt | Post URL |
|---------|---------|-------|------|----------------|---------|

## Complaints to Address
| Creator | Likes | Complaint Summary | Post URL |
|---------|-------|------------------|---------|

## Top Brand Advocates (Most Frequent Positive Posters)
1. @[handle] — [N] positive posts | [N] avg likes
```

## Troubleshooting

**Hashtag returns generic posts**: The brand hashtag may be ambiguous (e.g. "#apple"). Use `#[brand]official` or `#[brand][product]` for precision.
**Mostly competitor posts**: This may indicate your brand is being used in comparison posts — analyze `COMPETITOR_COMPARISON` category for positioning insights.
**Sentiment skewed by a single viral negative post**: Check `weighted sentiment` vs. raw sentiment; one viral post can shift the raw numbers.

