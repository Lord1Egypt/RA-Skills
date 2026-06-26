---
name: Douyin (TikTok China) Video Search API
description: Call GET /api/douyin/search-video/v4 for Douyin (TikTok China) Video Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_search_video"}}
---

# Douyin (TikTok China) Video Search

Use this focused JustOneAPI skill for video Search in Douyin (TikTok China). It targets `GET /api/douyin/search-video/v4`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Douyin (TikTok China) video Search data, including metadata and engagement signals, for content discovery, trend research, and competitive monitoring.

## Endpoint Scope

- Platform key: `douyin`
- Endpoint key: `search-video`
- Platform family: Douyin (TikTok China)
- Skill slug: `justoneapi-douyin-search-video`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchVideoV4` | `v4` | `GET` | `/api/douyin/search-video/v4` | Video Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `duration` | `query` | n/a | all | `string` | Filter by video duration. Available Values: - `_0`: No Limit - `_1`: Under 1 Minute - `_2`: 1-5 Minutes - `_3`: Over 5 Minutes |
| `duration` enum | values | n/a | n/a | n/a | `_0`, `_1`, `_2`, `_3` |
| `keyword` | `query` | all | n/a | `string` | The search keyword |
| `page` | `query` | n/a | all | `integer` | Page number (starting from 1) |
| `publishTime` | `query` | n/a | all | `string` | Filter by video publish time range. Available Values: - `_0`: No Limit - `_1`: Last 24 Hours - `_7`: Last 7 Days - `_180`: Last 6 Months |
| `publishTime` enum | values | n/a | n/a | n/a | `_0`, `_1`, `_180`, `_7` |
| `searchId` | `query` | n/a | all | `string` | Search ID; required for pages > 1 (use the search_id value returned by the last response) |
| `sortType` | `query` | n/a | all | `string` | Sorting criteria for search results. Available Values: - `_0`: General - `_1`: More likes - `_2`: Newest |
| `sortType` enum | values | n/a | n/a | n/a | `_0`, `_1`, `_2` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchVideoV4` for the documented `v4` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchVideoV4`.

```bash
node {baseDir}/bin/run.mjs --operation "searchVideoV4" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_search_video&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_search_video&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchVideoV4` on `/api/douyin/search-video/v4`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin (TikTok China) video Search data, including metadata and engagement signals, for content discovery, trend research, and competitive monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
