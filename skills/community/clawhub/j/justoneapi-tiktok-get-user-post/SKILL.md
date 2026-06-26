---
name: TikTok User Published Posts API
description: Call GET /api/tiktok/get-user-post/v1 for TikTok User Published Posts through JustOneAPI with secUid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_tiktok_get_user_post"}}
---

# TikTok User Published Posts

Use this focused JustOneAPI skill for user Published Posts in TikTok. It targets `GET /api/tiktok/get-user-post/v1`. Required non-token inputs are `secUid`. OpenAPI describes it as: Get TikTok user Published Posts data, including video ID, description, and publish time, for user activity analysis and posting frequency tracking, influencer performance evaluation, and content trend monitoring for specific creators.

## Endpoint Scope

- Platform key: `tiktok`
- Endpoint key: `get-user-post`
- Platform family: TikTok
- Skill slug: `justoneapi-tiktok-get-user-post`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getUserPostV1` | `v1` | `GET` | `/api/tiktok/get-user-post/v1` | User Published Posts |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `cursor` | `query` | n/a | all | `string` | Pagination cursor. Use '0' for the first page, then use the 'cursor' value returned in the previous response |
| `secUid` | `query` | all | n/a | `string` | The unique security ID of the TikTok user (e.g., MS4wLjABAAAAonP2...) |
| `sort` | `query` | n/a | all | `string` | Sorting criteria for the user's posts. Available Values: - `_0`: Default (Mixed) - `_1`: Highest Liked - `_2`: Latest Published |
| `sort` enum | values | n/a | n/a | n/a | `_0`, `_1`, `_2` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getUserPostV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getUserPostV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getUserPostV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"secUid":"<secUid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_user_post&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_user_post&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getUserPostV1` on `/api/tiktok/get-user-post/v1`.
- Echo the required lookup scope (`secUid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get TikTok user Published Posts data, including video ID, description, and publish time, for user activity analysis and posting frequency tracking, influencer performance evaluation, and content trend monitoring for specific creators.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
