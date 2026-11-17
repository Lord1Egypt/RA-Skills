---
name: monitoring-brand-mentions-on-twitter
description: >
  Monitors and aggregates brand mentions on Twitter/X using apidojo's Tweet and Search scrapers on Apify.
  Triggers when the user asks to: track mentions of a brand on Twitter, find what people are saying
  about a company on X, monitor brand sentiment on Twitter, set up brand mention tracking, find
  customer complaints or praise about a product on Twitter, analyze brand reputation based on tweets,
  or measure share of voice on X compared to competitors.
  Returns tweet text, author, engagement metrics, sentiment signals, and timestamps per mention.
  Ideal for brand managers, PR teams, community managers, and reputation analysts.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actors: apidojo/tweet-scraper, apidojo/tweet-scraper
---

# Monitoring Brand Mentions on Twitter

Collects all public tweets mentioning a brand, product, or keyword on Twitter/X within a date range. Groups by sentiment, surfaces top complaints and praise, and provides engagement totals.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed


## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `searchTerms` | array | ✅ | `[]` | Twitter advanced search queries (e.g. `["#AI lang:en", "from:NASA"]`) |
| `sort` | string | Optional | `Top` | Sort order: `Latest`, `Top`, or `Latest+Top` |
| `tweetLanguage` | string | Optional | — | ISO 639-1 language code (e.g. `en`) |
| `maxItems` | number | Optional | Unlimited | Maximum tweets to return |
| `onlyVerifiedUsers` | boolean | Optional | `false` | Only tweets from verified users |
| `onlyTwitterBlue` | boolean | Optional | `false` | Only Twitter Blue subscribers |
| `onlyImage` | boolean | Optional | `false` | Only tweets with images |
| `onlyVideo` | boolean | Optional | `false` | Only tweets with videos |
| `onlyQuote` | boolean | Optional | `false` | Only quote tweets |
| `author` | string | Optional | — | Filter to a specific author handle |
| `inReplyTo` | string | Optional | — | Tweets replying to a specific handle |
| `mentioning` | string | Optional | — | Tweets mentioning a specific handle |
| `geotaggedNear` | string | Optional | — | Tweets near a location |
| `withinRadius` | string | Optional | — | Radius around geotaggedNear |
| `geocode` | string | Optional | — | Lat/lng + radius string |
| `placeObjectId` | string | Optional | — | Tweets tagged with a place |
| `minimumRetweets` | number | Optional | — | Minimum retweet count |
| `minimumFavorites` | number | Optional | — | Minimum like count |
| `minimumReplies` | number | Optional | — | Minimum reply count |
| `start` | string | Optional | — | Tweets after this date (YYYY-MM-DD) |
| `end` | string | Optional | — | Tweets before this date (YYYY-MM-DD) |
| `includeSearchTerms` | boolean | Optional | `false` | Add the matched search term to each tweet |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |
## Workflow

```
Progress:
- [ ] Step 1: Define brand terms and date range
- [ ] Step 2: Run tweet-scraper
- [ ] Step 3: Retrieve dataset
- [ ] Step 4: Classify sentiment (positive/negative/neutral)
- [ ] Step 5: Deliver structured report
```

### Step 1: Clarify Parameters

Ask the user for:
- **Brand terms** — brand name, handle, product name, hashtag, and common misspellings. Build a list.
  Example: `["@Nike", "Nike", "#Nike", "Nike shoes"]`
- **Date range** — e.g., "last 7 days" or specific dates
- **Exclude retweets?** (default: yes — filters noise)
- **Min engagement** (optional — e.g., tweets with ≥10 likes only)
- **Language** (default: all)

### Step 2: Run tweet-scraper

Run once per major search term to maximize coverage. Combine results after.


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~tweet-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~tweet-scraper"
Input:
{
  "searchTerms": ["[BRAND_TERM]"],
  "maxItems": 500,
  "includeReplies": true,
  "tweetLanguage": "en",
  "since": "[YYYY-MM-DD]",
  "until": "[YYYY-MM-DD]"
}
```

**If Apify MCP is not available:**
```bash
curl -X POST \
  "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "searchTerms": ["[BRAND_TERM]"],
    "maxItems": 500,
    "includeReplies": true,
    "since": "[YYYY-MM-DD]",
    "until": "[YYYY-MM-DD]"
  }'
```

Run for each brand term in the list. Wait for `SUCCEEDED`, collect all results.

### Step 3: Fetch and Merge Results

```bash
curl "https://api.apify.com/v2/actor-runs/$RUN_ID/dataset/items?token=$APIFY_TOKEN"
```

Merge datasets from all runs. Deduplicate by tweet `id`. Result: unified list of all mentions.

### Step 4: Classify Sentiment

For each tweet's `text` field, apply a simple classification pass:

**Positive signals:** words like "love", "great", "amazing", "best", "recommend", "thank", "perfect"
**Negative signals:** words like "hate", "awful", "broken", "scam", "worst", "never again", "disappointed", "avoid"
**Neutral:** everything else (announcements, news, questions)

Group tweets into three buckets: Positive, Negative, Neutral.

Identify top 5 most-engaged negative tweets (these need the fastest response).
Identify top 5 most-engaged positive tweets (retweet candidates / testimonial material).

### Step 5: Format Report

Use the output template below.

## Output Format

```
# Brand Mention Report: [BRAND]
Period: [START_DATE] – [END_DATE] | Total mentions: [N] | Analyzed: [DATE]

## Sentiment Summary
| Sentiment | Count | % of Total | Avg Engagement |
|-----------|-------|------------|----------------|
| Positive  | [N]   | [X%]       | [likes+RT avg] |
| Negative  | [N]   | [X%]       | [likes+RT avg] |
| Neutral   | [N]   | [X%]       | [likes+RT avg] |

## 🔴 Top Negative Mentions (Action Required)
1. @[handle] ([likes] likes): "[tweet text excerpt]" → [url]
2. @[handle] ([likes] likes): "[tweet text excerpt]" → [url]
3. @[handle] ([likes] likes): "[tweet text excerpt]" → [url]

## 🟢 Top Positive Mentions (Amplify These)
1. @[handle] ([likes] likes): "[tweet text excerpt]" → [url]
2. @[handle] ([likes] likes): "[tweet text excerpt]" → [url]
3. @[handle] ([likes] likes): "[tweet text excerpt]" → [url]

## Volume Over Time
[Day 1]: [N] mentions | [Day 2]: [N] mentions | [Day 3]: [N] mentions...

## Key Themes in Negative Mentions
- [Theme 1]: [N] tweets (e.g., "shipping delays")
- [Theme 2]: [N] tweets (e.g., "customer service")

## Key Themes in Positive Mentions
- [Theme 1]: [N] tweets
- [Theme 2]: [N] tweets
```

## Troubleshooting

**Too many results for popular brands:** Increase `minLikes` filter to 5 or 10 to focus on influential mentions.
**Missing mentions:** Twitter search API has ~7-10 day lookback limit for free tier. For historical data, reduce date range.
**Sentiment misclassification:** Sarcasm is hard to catch with keyword matching — flag high-engagement tweets for manual review.

