---
name: Bilibili User Profile API
description: Call GET /api/bilibili/get-user-detail/v2 for Bilibili User Profile through JustOneAPI with uid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_bilibili_get_user_detail"}}
---

# Bilibili User Profile

Use this focused JustOneAPI skill for user Profile in Bilibili. It targets `GET /api/bilibili/get-user-detail/v2`. Required non-token inputs are `uid`. OpenAPI describes it as: Get Bilibili user Profile data, including account metadata, audience metrics, and verification-related fields, for analyzing creator's profile, level, and verification status and verifying user identity and social presence on bilibili.

## Endpoint Scope

- Platform key: `bilibili`
- Endpoint key: `get-user-detail`
- Platform family: Bilibili
- Skill slug: `justoneapi-bilibili-get-user-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getUserDetailV2` | `v2` | `GET` | `/api/bilibili/get-user-detail/v2` | User Profile |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `uid` | `query` | all | n/a | `string` | Bilibili User ID (UID) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getUserDetailV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getUserDetailV2`.

```bash
node {baseDir}/bin/run.mjs --operation "getUserDetailV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"uid":"<uid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getUserDetailV2` on `/api/bilibili/get-user-detail/v2`.
- Echo the required lookup scope (`uid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Bilibili user Profile data, including account metadata, audience metrics, and verification-related fields, for analyzing creator's profile, level, and verification status and verifying user identity and social presence on bilibili.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
