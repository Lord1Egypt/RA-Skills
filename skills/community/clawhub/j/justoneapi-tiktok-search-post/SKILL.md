---
name: TikTok Post Search API
description: Call GET /api/tiktok/search-post/v1 for TikTok Post Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_tiktok_search_post"}}
---

# TikTok Post Search

Use this focused JustOneAPI skill for post Search in TikTok. It targets `GET /api/tiktok/search-post/v1`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get TikTok post Search data, including key details such as video ID, description, and author information, for trend monitoring and content discovery and keyword-based market analysis and sentiment tracking.

## Endpoint Scope

- Platform key: `tiktok`
- Endpoint key: `search-post`
- Platform family: TikTok
- Skill slug: `justoneapi-tiktok-search-post`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchPostV1` | `v1` | `GET` | `/api/tiktok/search-post/v1` | Post Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | Search keywords (e.g., 'deepseek') |
| `offset` | `query` | n/a | all | `integer` | Pagination offset, starting from 0 and stepping by 20 |
| `publishTime` | `query` | n/a | all | `string` | Filter posts by publishing time. Available Values: - `ALL`: All Time - `ONE_DAY`: Last 24 Hours - `ONE_WEEK`: Last 7 Days - `ONE_MONTH`: Last 30 Days - `THREE_MONTHS`: Last 90 Days - `HALF_YEAR`: Last 180 Days |
| `publishTime` enum | values | n/a | n/a | n/a | `ALL`, `HALF_YEAR`, `ONE_DAY`, `ONE_MONTH`, `ONE_WEEK`, `THREE_MONTHS` |
| `region` | `query` | n/a | all | `string` | ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB') |
| `sortType` | `query` | n/a | all | `string` | Sorting criteria for search results. Available Values: - `RELEVANCE`: Relevance (Default) - `MOST_LIKED`: Most Liked |
| `sortType` enum | values | n/a | n/a | n/a | `MOST_LIKED`, `RELEVANCE` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchPostV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchPostV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchPostV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_search_post&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_search_post&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchPostV1` on `/api/tiktok/search-post/v1`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get TikTok post Search data, including key details such as video ID, description, and author information, for trend monitoring and content discovery and keyword-based market analysis and sentiment tracking.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
