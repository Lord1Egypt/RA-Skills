---
name: Toutiao User Profile API
description: Call GET /api/toutiao/get-user-detail/v1 for Toutiao User Profile through JustOneAPI with userId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_toutiao_get_user_detail"}}
---

# Toutiao User Profile

Use this focused JustOneAPI skill for user Profile in Toutiao. It targets `GET /api/toutiao/get-user-detail/v1`. Required non-token inputs are `userId`. OpenAPI describes it as: Get Toutiao user Profile data, including user ID, nickname, and avatar, for influencer profiling and audience analysis and monitoring creator performance and growth.

## Endpoint Scope

- Platform key: `toutiao`
- Endpoint key: `get-user-detail`
- Platform family: Toutiao
- Skill slug: `justoneapi-toutiao-get-user-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getToutiaoUserDetailV1` | `v1` | `GET` | `/api/toutiao/get-user-detail/v1` | User Profile |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `userId` | `query` | all | n/a | `string` | The unique identifier of the Toutiao user |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getToutiaoUserDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getToutiaoUserDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getToutiaoUserDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"userId":"<userId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_get_user_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao_get_user_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getToutiaoUserDetailV1` on `/api/toutiao/get-user-detail/v1`.
- Echo the required lookup scope (`userId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Toutiao user Profile data, including user ID, nickname, and avatar, for influencer profiling and audience analysis and monitoring creator performance and growth.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
