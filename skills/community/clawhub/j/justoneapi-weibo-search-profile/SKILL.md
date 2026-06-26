---
name: Weibo Search User Published Posts API
description: Call GET /api/weibo/search-profile/v1 for Weibo Search User Published Posts through JustOneAPI with q and uid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weibo_search_profile"}}
---

# Weibo Search User Published Posts

Use this focused JustOneAPI skill for search User Published Posts in Weibo. It targets `GET /api/weibo/search-profile/v1`. Required non-token inputs are `q` and `uid`. OpenAPI describes it as: Get Weibo search User Published Posts data, including matched results, metadata, and ranking signals, for author research and historical content discovery.

## Endpoint Scope

- Platform key: `weibo`
- Endpoint key: `search-profile`
- Platform family: Weibo
- Skill slug: `justoneapi-weibo-search-profile`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchProfileV1` | `v1` | `GET` | `/api/weibo/search-profile/v1` | Search User Published Posts |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `endDay` | `query` | n/a | all | `string` | End Day (yyyy-MM-dd) |
| `page` | `query` | n/a | all | `integer` | Page number, starting with 1 |
| `q` | `query` | all | n/a | `string` | Search Keywords |
| `startDay` | `query` | n/a | all | `string` | Start Day (yyyy-MM-dd) |
| `uid` | `query` | all | n/a | `string` | Weibo User ID (UID) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchProfileV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchProfileV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchProfileV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"uid":"<uid>","q":"<q>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_search_profile&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_search_profile&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchProfileV1` on `/api/weibo/search-profile/v1`.
- Echo the required lookup scope (`q` and `uid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Weibo search User Published Posts data, including matched results, metadata, and ranking signals, for author research and historical content discovery.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
