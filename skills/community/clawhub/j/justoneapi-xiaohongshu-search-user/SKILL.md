---
name: Xiaohongshu (RedNote) User Search API
description: Call GET /api/xiaohongshu/search-user/v2 for Xiaohongshu (RedNote) User Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_search_user"}}
---

# Xiaohongshu (RedNote) User Search

Use this focused JustOneAPI skill for user Search in Xiaohongshu (RedNote). It targets `GET /api/xiaohongshu/search-user/v2`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Xiaohongshu (RedNote) user Search data, including profile metadata and public signals, for creator discovery and account research.

## Endpoint Scope

- Platform key: `xiaohongshu`
- Endpoint key: `search-user`
- Platform family: Xiaohongshu (RedNote)
- Skill slug: `justoneapi-xiaohongshu-search-user`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getSearchUserV2` | `v2` | `GET` | `/api/xiaohongshu/search-user/v2` | User Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | Search keyword |
| `page` | `query` | n/a | all | `integer` | Page number for pagination |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getSearchUserV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getSearchUserV2`.

```bash
node {baseDir}/bin/run.mjs --operation "getSearchUserV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_user&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_search_user&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getSearchUserV2` on `/api/xiaohongshu/search-user/v2`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu (RedNote) user Search data, including profile metadata and public signals, for creator discovery and account research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
