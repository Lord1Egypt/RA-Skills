---
name: Douyin (TikTok China) User Profile API
description: Call GET /api/douyin/get-user-detail/v3 for Douyin (TikTok China) User Profile through JustOneAPI with secUid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_get_user_detail"}}
---

# Douyin (TikTok China) User Profile

Use this focused JustOneAPI skill for user Profile in Douyin (TikTok China). It targets `GET /api/douyin/get-user-detail/v3`. Required non-token inputs are `secUid`. OpenAPI describes it as: Get Douyin (TikTok China) user Profile data, including follower counts, verification status, and bio details, for creator research and account analysis.

## Endpoint Scope

- Platform key: `douyin`
- Endpoint key: `get-user-detail`
- Platform family: Douyin (TikTok China)
- Skill slug: `justoneapi-douyin-get-user-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getUserDetailV3` | `v3` | `GET` | `/api/douyin/get-user-detail/v3` | User Profile |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `secUid` | `query` | all | n/a | `string` | The unique user ID (sec_uid) on Douyin |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getUserDetailV3` for the documented `v3` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getUserDetailV3`.

```bash
node {baseDir}/bin/run.mjs --operation "getUserDetailV3" --token "$JUST_ONE_API_TOKEN" --params-json '{"secUid":"<secUid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_user_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_user_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getUserDetailV3` on `/api/douyin/get-user-detail/v3`.
- Echo the required lookup scope (`secUid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin (TikTok China) user Profile data, including follower counts, verification status, and bio details, for creator research and account analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
