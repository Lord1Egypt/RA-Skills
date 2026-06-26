---
name: Bilibili Video Search API
description: Call GET /api/bilibili/search-video/v2 for Bilibili Video Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_bilibili_search_video"}}
---

# Bilibili Video Search

Use this focused JustOneAPI skill for video Search in Bilibili. It targets `GET /api/bilibili/search-video/v2`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Bilibili video Search data, including matched videos, creators, and engagement metrics, for topic research and content discovery.

## Endpoint Scope

- Platform key: `bilibili`
- Endpoint key: `search-video`
- Platform family: Bilibili
- Skill slug: `justoneapi-bilibili-search-video`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchBilibiliVideoV2` | `v2` | `GET` | `/api/bilibili/search-video/v2` | Video Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | Search keyword |
| `order` | `query` | n/a | all | `string` | Sorting criteria for search results. Available Values: - `general`: General - `click`: Most Played - `pubdate`: Latest - `dm`: Most Danmaku - `stow`: Most Favorite |
| `order` enum | values | n/a | n/a | n/a | `click`, `dm`, `general`, `pubdate`, `stow` |
| `page` | `query` | n/a | all | `string` | Page number for pagination |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchBilibiliVideoV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchBilibiliVideoV2`.

```bash
node {baseDir}/bin/run.mjs --operation "searchBilibiliVideoV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_search_video&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_search_video&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchBilibiliVideoV2` on `/api/bilibili/search-video/v2`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Bilibili video Search data, including matched videos, creators, and engagement metrics, for topic research and content discovery.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
