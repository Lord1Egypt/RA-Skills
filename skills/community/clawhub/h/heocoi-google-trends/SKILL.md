---
name: heocoi-google-trends
description: Get Google Trends data (interest over time, interest by region, related queries, Trending Now) for up to 5 keywords. Web, YouTube, News, Images or Shopping search. Use when the user asks what is trending, compares search interest, or checks demand for a keyword.
version: 0.1.0
metadata:
  openclaw:
    primaryEnv: APIFY_TOKEN
    requires:
      env: [APIFY_TOKEN]
      bins: [curl]
    homepage: https://apify.com/heocoi/google-trends-api
---

# Google Trends

Calls the `heocoi/google-trends-api` Actor on Apify and returns JSON. Costs $3 per 1,000 results
(one result = one query or one Trending Now country), billed to the user's Apify account. Apify's free
plan includes $5 of monthly credit. Get a token at https://console.apify.com/settings/integrations.

## Query

```bash
curl -s -X POST \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  "https://api.apify.com/v2/acts/heocoi~google-trends-api/run-sync-get-dataset-items" \
  -d '{"searchTerms": ["iphone, android"], "geo": "US", "timeRange": "today 12-m"}'
```

Input fields:
- `searchTerms`: list of queries. Comma-separate up to 5 keywords in one query to compare them.
- `geo`: `US`, `JP`, `US-CA`... empty = worldwide.
- `timeRange`: `now 1-H`, `now 7-d`, `today 1-m`, `today 3-m`, `today 12-m`, `today 5-y`, `all`, or `customTimeRange` as `YYYY-MM-DD YYYY-MM-DD`.
- `searchProperty`: `web`, `youtube`, `news`, `images`, `shopping`.
- `sections`: any of `interestOverTime`, `interestByRegion`, `relatedQueries`.
- `trendingNowGeos`: country codes for today's Trending Now list, e.g. `["US"]`.

## Reading the result

Each item has `interestOverTime` (`date`, `values` per keyword on Google's 0-100 scale), `interestByRegion`
and `relatedQueries` (`top`, `rising`). Trending Now items have `"type": "trendingNow"` and a `trends` list.
Values are relative, so compare keywords inside one query rather than across separate queries.
