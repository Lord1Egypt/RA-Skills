---
name: Xiaohongshu Creator Marketplace (Pugongying) Creator Profile API
description: Call GET /api/xiaohongshu-pgy/api/solar/cooperator/user/blogger/userId/v1 for Xiaohongshu Creator Marketplace (Pugongying) Creator Profile through JustOneAPI with userId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_pgy_api_solar_cooperator_user_blogger_user_id"}}
---

# Xiaohongshu Creator Marketplace (Pugongying) Creator Profile

Use this focused JustOneAPI skill for creator Profile in Xiaohongshu Creator Marketplace (Pugongying). It targets `GET /api/xiaohongshu-pgy/api/solar/cooperator/user/blogger/userId/v1`. Required non-token inputs are `userId`. OpenAPI describes it as: Get Xiaohongshu Creator Marketplace (Pugongying) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.

## Endpoint Scope

- Platform key: `xiaohongshu-pgy`
- Endpoint key: `api/solar/cooperator/user/blogger/userId`
- Platform family: Xiaohongshu Creator Marketplace (Pugongying)
- Skill slug: `justoneapi-xiaohongshu-pgy-api-solar-cooperator-user-blogger-user-id`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `apiSolarCooperatorUserBloggerUserIdV1` | `v1` | `GET` | `/api/xiaohongshu-pgy/api/solar/cooperator/user/blogger/userId/v1` | Creator Profile |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `userId` | `query` | all | n/a | `string` | Blogger's user ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `apiSolarCooperatorUserBloggerUserIdV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `apiSolarCooperatorUserBloggerUserIdV1`.

```bash
node {baseDir}/bin/run.mjs --operation "apiSolarCooperatorUserBloggerUserIdV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"userId":"<userId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_cooperator_user_blogger_user_id&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_cooperator_user_blogger_user_id&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `apiSolarCooperatorUserBloggerUserIdV1` on `/api/xiaohongshu-pgy/api/solar/cooperator/user/blogger/userId/v1`.
- Echo the required lookup scope (`userId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu Creator Marketplace (Pugongying) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
