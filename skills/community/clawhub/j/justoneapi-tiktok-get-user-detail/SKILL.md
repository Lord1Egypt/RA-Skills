---
name: TikTok User Profile API
description: Call GET /api/tiktok/get-user-detail/v1 for TikTok User Profile through JustOneAPI.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_tiktok_get_user_detail"}}
---

# TikTok User Profile

Use this focused JustOneAPI skill for user Profile in TikTok. It targets `GET /api/tiktok/get-user-detail/v1`. It has no required non-token parameters. OpenAPI describes it as: Get TikTok user Profile data, including nickname, unique ID, and avatar, for influencer profiling and audience analysis, account performance tracking and growth monitoring, and identifying verified status and official accounts.

## Endpoint Scope

- Platform key: `tiktok`
- Endpoint key: `get-user-detail`
- Platform family: TikTok
- Skill slug: `justoneapi-tiktok-get-user-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getTiktokUserDetailV1` | `v1` | `GET` | `/api/tiktok/get-user-detail/v1` | User Profile |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `secUid` | `query` | n/a | all | `string` | The unique security ID of the user |
| `uniqueId` | `query` | n/a | all | `string` | The unique handle/username of the user (e.g., 'tiktok') |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getTiktokUserDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getTiktokUserDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getTiktokUserDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"key":"value"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_user_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_user_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getTiktokUserDetailV1` on `/api/tiktok/get-user-detail/v1`.
- Prioritize fields that support this endpoint purpose: Get TikTok user Profile data, including nickname, unique ID, and avatar, for influencer profiling and audience analysis, account performance tracking and growth monitoring, and identifying verified status and official accounts.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
