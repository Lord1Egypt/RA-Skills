---
name: Google SERP Trends Search API
description: Call GET /api/v1/google/trends/search for Google SERP Trends Search through Just Serp API with query.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_search&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_search&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google_trends_search"}}
---

# Google SERP Trends Search

Use this focused Just Serp API skill for Google SERP Trends Search. It targets `GET /api/v1/google/trends/search`. Required inputs are `query`. OpenAPI describes it as: Get Google trends Search data, including interest over time, geo breakdowns, and related queries, for demand analysis and seasonal trend monitoring.

## Endpoint Scope

- Group key: `google`
- Endpoint key: `trends/search`
- Group family: Google SERP
- Skill slug: `justserpapi-google-trends-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `TrendsSearch` | `v1` | `GET` | `/api/v1/google/trends/search` | Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `cat` | `query` | n/a | all | `string` | The search category code (e.g., '0' for all categories) |
| `data_type` | `query` | n/a | all | `string` | The type of trend data to retrieve. Supported values: 'TIMESERIES' (Interest over time), 'GEO_MAP' (Breakdown by region) |
| `date` | `query` | n/a | all | `string` | Date range filter for the search. Supports predefined values (now 1-H, now 4-H, now 1-d, now 7-d, today 1-m, today 3-m, today 12-m, today 5-y, all) and custom ranges: yyyy-mm-dd yyyy-mm-dd (e.g. 2021-10-15 2022-05-25) or hourly yyyy-mm-ddThh yyyy-mm-ddThh within 1 week (e.g. 2022-05-19T10 2022-05-24T22, based on tz) |
| `geo` | `query` | n/a | all | `string` | The geographic location code to filter trends (e.g., 'US', 'GB'). Omit for worldwide trends. See <a href="/reference/google-trends-locations">Google Trends Locations</a> |
| `gprop` | `query` | n/a | all | `string` | The Google property to filter trends. Supported values: 'images', 'news', 'froogle' (Shopping), 'youtube' |
| `language` | `query` | n/a | all | `string` | Set the language for the results using its two-letter code (e.g., 'en' for English, 'fr' for French). See <a href="/reference/google-language">Google Language</a> |
| `query` | `query` | all | n/a | `string` | The search term or topic ID to analyze in Google Trends (e.g., 'iPhone', '/m/027lnzs' for Bitcoin). You can provide up to 5 terms separated by commas for comparisons |
| `region` | `query` | n/a | all | `string` | Refines results for region charts. Supported values: 'COUNTRY', 'REGION', 'DMA', 'CITY' |
| `tz` | `query` | n/a | all | `integer` | Time zone offset in minutes (e.g., '420' for PDT). Range: -1439 to 1439 |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `TrendsSearch` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `TrendsSearch`.

```bash
node {baseDir}/bin/run.mjs --operation "TrendsSearch" --api-key "$JUST_SERP_API_KEY" --params-json '{"query":"<query>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_search&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google_trends_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `TrendsSearch` on `/api/v1/google/trends/search`.
- Echo the required lookup scope (`query`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Google trends Search data, including interest over time, geo breakdowns, and related queries, for demand analysis and seasonal trend monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
