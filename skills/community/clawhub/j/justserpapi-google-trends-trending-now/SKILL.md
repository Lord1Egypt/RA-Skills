---
name: Google SERP Trends Trending Now API
description: Call GET /api/v1/google/trends/trending-now for Google SERP Trends Trending Now through Just Serp API with geo.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_trending_now&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_trending_now&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_trends_trending_now"}}
---

# Google SERP Trends Trending Now

Use this focused Just Serp API skill for Google SERP Trends Trending Now. It targets `GET /api/v1/google/trends/trending-now`. Required inputs are `geo`. OpenAPI describes it as: Get Google trends Trending Now data, including latest trending topics, region and time-window filters, and volume indicators, for breaking-trend monitoring and editorial planning.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `trends/trending-now`
- Group family: Google SERP
- Skill slug: `justserpapi-google-trends-trending-now`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `TrendsTrendingNow` | `v1` | `GET` | `/api/v1/google/trends/trending-now` | Trending Now |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `geo` | `query` | all | n/a | `string` | The geographic location code to retrieve real-time trends for (e.g., 'US' for United States). Default is 'US' |
| `hours` | `query` | n/a | all | `string` | Time window for trending topics. Supported values: '4' (past 4 hours), '24' (past 24 hours), '48' (past 48 hours), '168' (past 7 days) |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en') |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `TrendsTrendingNow` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `TrendsTrendingNow`.

```bash
node {baseDir}/bin/run.mjs --operation "TrendsTrendingNow" --api-key "$JUST_SERP_API_KEY" --params-json '{"geo":"<geo>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_trending_now&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_trending_now&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `TrendsTrendingNow` on `/api/v1/google/trends/trending-now`.
- Echo the required lookup scope (`geo`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google trends Trending Now data, including latest trending topics, region and time-window filters, and volume indicators, for breaking-trend monitoring and editorial planning.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
