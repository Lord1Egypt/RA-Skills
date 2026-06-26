---
name: Kuaishou User Profile API
description: Call GET /api/kuaishou/get-user-detail/v1 for Kuaishou User Profile through JustOneAPI with userId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_kuaishou_get_user_detail"}}
---

# Kuaishou User Profile

Use this focused JustOneAPI skill for user Profile in Kuaishou. It targets `GET /api/kuaishou/get-user-detail/v1`. Required non-token inputs are `userId`. OpenAPI describes it as: Get Kuaishou user Profile data, including account metadata, audience metrics, and verification-related fields, for creator research and building creator profiles and monitoring audience growth and account status.

## Endpoint Scope

- Platform key: `kuaishou`
- Endpoint key: `get-user-detail`
- Platform family: Kuaishou
- Skill slug: `justoneapi-kuaishou-get-user-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getUserProfileV1` | `v1` | `GET` | `/api/kuaishou/get-user-detail/v1` | User Profile |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `userId` | `query` | all | n/a | `string` | The unique user ID on Kuaishou |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getUserProfileV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getUserProfileV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getUserProfileV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"userId":"<userId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_user_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou_get_user_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getUserProfileV1` on `/api/kuaishou/get-user-detail/v1`.
- Echo the required lookup scope (`userId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Kuaishou user Profile data, including account metadata, audience metrics, and verification-related fields, for creator research and building creator profiles and monitoring audience growth and account status.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
