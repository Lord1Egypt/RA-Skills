---
name: Weibo User Fans API
description: Call GET /api/weibo/get-fans/v1 for Weibo User Fans through JustOneAPI with uid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weibo_get_fans"}}
---

# Weibo User Fans

Use this focused JustOneAPI skill for user Fans in Weibo. It targets `GET /api/weibo/get-fans/v1`. Required non-token inputs are `uid`. OpenAPI describes it as: Get Weibo user Fans data, including profile metadata and verification signals, for audience analysis and influencer research.

## Endpoint Scope

- Platform key: `weibo`
- Endpoint key: `get-fans`
- Platform family: Weibo
- Skill slug: `justoneapi-weibo-get-fans`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getFansV1` | `v1` | `GET` | `/api/weibo/get-fans/v1` | User Fans |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `page` | `query` | n/a | all | `integer` | Page number, starting with 1 |
| `uid` | `query` | all | n/a | `string` | Weibo User ID (UID) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getFansV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getFansV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getFansV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"uid":"<uid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_fans&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_fans&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getFansV1` on `/api/weibo/get-fans/v1`.
- Echo the required lookup scope (`uid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Weibo user Fans data, including profile metadata and verification signals, for audience analysis and influencer research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
