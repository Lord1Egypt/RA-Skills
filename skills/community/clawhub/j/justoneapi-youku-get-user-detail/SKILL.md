---
name: YOUKU User Profile API
description: Call GET /api/youku/get-user-detail/v1 for YOUKU User Profile through JustOneAPI with uid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_youku_get_user_detail"}}
---

# YOUKU User Profile

Use this focused JustOneAPI skill for user Profile in YOUKU. It targets `GET /api/youku/get-user-detail/v1`. Required non-token inputs are `uid`. OpenAPI describes it as: Get YOUKU user Profile data, including user ID, username, and avatar, for analyzing creator influence and audience size, monitoring account growth and verification status, and fetching basic user info for social crm.

## Endpoint Scope

- Platform key: `youku`
- Endpoint key: `get-user-detail`
- Platform family: YOUKU
- Skill slug: `justoneapi-youku-get-user-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getYoukuUserDetailV1` | `v1` | `GET` | `/api/youku/get-user-detail/v1` | User Profile |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `uid` | `query` | all | n/a | `string` | The unique identifier for the user |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getYoukuUserDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getYoukuUserDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getYoukuUserDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"uid":"<uid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_get_user_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku_get_user_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getYoukuUserDetailV1` on `/api/youku/get-user-detail/v1`.
- Echo the required lookup scope (`uid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get YOUKU user Profile data, including user ID, username, and avatar, for analyzing creator influence and audience size, monitoring account growth and verification status, and fetching basic user info for social crm.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
