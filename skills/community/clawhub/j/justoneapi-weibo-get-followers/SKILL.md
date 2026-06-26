---
name: Weibo User Followers API
description: Call GET /api/weibo/get-followers/v1 for Weibo User Followers through JustOneAPI with uid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weibo_get_followers"}}
---

# Weibo User Followers

Use this focused JustOneAPI skill for user Followers in Weibo. It targets `GET /api/weibo/get-followers/v1`. Required non-token inputs are `uid`. OpenAPI describes it as: Get Weibo user Followers data, including profile metadata and verification signals, for network analysis and creator research.

## Endpoint Scope

- Platform key: `weibo`
- Endpoint key: `get-followers`
- Platform family: Weibo
- Skill slug: `justoneapi-weibo-get-followers`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getFollowersV1` | `v1` | `GET` | `/api/weibo/get-followers/v1` | User Followers |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `page` | `query` | n/a | all | `integer` | Page number, starting with 1 |
| `uid` | `query` | all | n/a | `string` | Weibo User ID (UID) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getFollowersV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getFollowersV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getFollowersV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"uid":"<uid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_followers&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_followers&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getFollowersV1` on `/api/weibo/get-followers/v1`.
- Echo the required lookup scope (`uid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Weibo user Followers data, including profile metadata and verification signals, for network analysis and creator research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
