---
name: Douyin (TikTok China) User Search API
description: Call GET /api/douyin/search-user/v2 for Douyin (TikTok China) User Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_search_user"}}
---

# Douyin (TikTok China) User Search

Use this focused JustOneAPI skill for user Search in Douyin (TikTok China). It targets `GET /api/douyin/search-user/v2`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Douyin (TikTok China) user Search data, including profile metadata and follower signals, for creator discovery and account research.

## Endpoint Scope

- Platform key: `douyin`
- Endpoint key: `search-user`
- Platform family: Douyin (TikTok China)
- Skill slug: `justoneapi-douyin-search-user`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchDouyinUserV2` | `v2` | `GET` | `/api/douyin/search-user/v2` | User Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | The search keyword |
| `page` | `query` | n/a | all | `integer` | Page number (starting from 1) |
| `userType` | `query` | n/a | all | `string` | Filter by user type. Available Values: - `common_user`: Common User - `enterprise_user`: Enterprise User - `personal_user`: Verified Individual User |
| `userType` enum | values | n/a | n/a | n/a | `common_user`, `enterprise_user`, `personal_user` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchDouyinUserV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchDouyinUserV2`.

```bash
node {baseDir}/bin/run.mjs --operation "searchDouyinUserV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_search_user&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_search_user&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchDouyinUserV2` on `/api/douyin/search-user/v2`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin (TikTok China) user Search data, including profile metadata and follower signals, for creator discovery and account research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
