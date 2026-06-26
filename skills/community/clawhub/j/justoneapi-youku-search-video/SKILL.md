---
name: YOUKU Video Search API
description: Call GET /api/youku/search-video/v1 for YOUKU Video Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_youku_search_video"}}
---

# YOUKU Video Search

Use this focused JustOneAPI skill for video Search in YOUKU. It targets `GET /api/youku/search-video/v1`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get YOUKU video Search data, including video ID, title, and cover image, for keyword-based video discovery, monitoring specific topics or trends on youku, and analyzing search results for market research.

## Endpoint Scope

- Platform key: `youku`
- Endpoint key: `search-video`
- Platform family: YOUKU
- Skill slug: `justoneapi-youku-search-video`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchVideoV1` | `v1` | `GET` | `/api/youku/search-video/v1` | Video Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | Keyword to search for |
| `page` | `query` | n/a | all | `integer` | Page number for pagination, starting from 1 |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchVideoV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchVideoV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchVideoV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_search_video&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_search_video&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchVideoV1` on `/api/youku/search-video/v1`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get YOUKU video Search data, including video ID, title, and cover image, for keyword-based video discovery, monitoring specific topics or trends on youku, and analyzing search results for market research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
