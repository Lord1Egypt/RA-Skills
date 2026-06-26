---
name: TikTok User Search API
description: Call GET /api/tiktok/search-user/v1 for TikTok User Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_tiktok_search_user"}}
---

# TikTok User Search

Use this focused JustOneAPI skill for user Search in TikTok. It targets `GET /api/tiktok/search-user/v1`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get TikTok user Search data, including basic profile information such as user ID, nickname, and unique handle, for discovering influencers in specific niches via keywords and identifying target audiences and conducting competitor research.

## Endpoint Scope

- Platform key: `tiktok`
- Endpoint key: `search-user`
- Platform family: TikTok
- Skill slug: `justoneapi-tiktok-search-user`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchUserV1` | `v1` | `GET` | `/api/tiktok/search-user/v1` | User Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `cursor` | `query` | n/a | all | `string` | Pagination cursor. Start with '0' |
| `keyword` | `query` | all | n/a | `string` | Search keywords (e.g., 'deepseek') |
| `searchId` | `query` | n/a | all | `string` | The 'logid' returned from the previous request for consistent search results |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchUserV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchUserV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchUserV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_search_user&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_search_user&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchUserV1` on `/api/tiktok/search-user/v1`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get TikTok user Search data, including basic profile information such as user ID, nickname, and unique handle, for discovering influencers in specific niches via keywords and identifying target audiences and conducting competitor research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
