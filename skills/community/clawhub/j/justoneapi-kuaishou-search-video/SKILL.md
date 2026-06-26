---
name: Kuaishou Video Search API
description: Call GET /api/kuaishou/search-video/v2 for Kuaishou Video Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_kuaishou_search_video"}}
---

# Kuaishou Video Search

Use this focused JustOneAPI skill for video Search in Kuaishou. It targets `GET /api/kuaishou/search-video/v2`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Kuaishou video Search data, including video ID, cover image, and description, for competitive analysis and market trends and keywords monitoring and brand tracking.

## Endpoint Scope

- Platform key: `kuaishou`
- Endpoint key: `search-video`
- Platform family: Kuaishou
- Skill slug: `justoneapi-kuaishou-search-video`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchKuaishouVideoV2` | `v2` | `GET` | `/api/kuaishou/search-video/v2` | Video Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | The search keyword to find videos |
| `page` | `query` | n/a | all | `integer` | Page number for results, starting from 1 |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchKuaishouVideoV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchKuaishouVideoV2`.

```bash
node {baseDir}/bin/run.mjs --operation "searchKuaishouVideoV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_search_video&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_search_video&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchKuaishouVideoV2` on `/api/kuaishou/search-video/v2`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Kuaishou video Search data, including video ID, cover image, and description, for competitive analysis and market trends and keywords monitoring and brand tracking.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
