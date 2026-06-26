---
name: Weibo Post Comments API
description: Call GET /api/weibo/get-post-comments/v1 for Weibo Post Comments through JustOneAPI with mid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weibo_get_post_comments"}}
---

# Weibo Post Comments

Use this focused JustOneAPI skill for post Comments in Weibo. It targets `GET /api/weibo/get-post-comments/v1`. Required non-token inputs are `mid`. OpenAPI describes it as: Get Weibo post Comments data, including text, authors, and timestamps, for feedback analysis.

## Endpoint Scope

- Platform key: `weibo`
- Endpoint key: `get-post-comments`
- Platform family: Weibo
- Skill slug: `justoneapi-weibo-get-post-comments`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getWeiboPostCommentsV1` | `v1` | `GET` | `/api/weibo/get-post-comments/v1` | Post Comments |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `maxId` | `query` | n/a | all | `string` | Pagination cursor returned by the previous response |
| `mid` | `query` | all | n/a | `string` | Weibo post mid |
| `sort` | `query` | n/a | all | `string` | Sort order for the result set. Available Values: - `TIME`: Time - `HOT`: Hot |
| `sort` enum | values | n/a | n/a | n/a | `HOT`, `TIME` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getWeiboPostCommentsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getWeiboPostCommentsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getWeiboPostCommentsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"mid":"<mid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_post_comments&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_post_comments&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getWeiboPostCommentsV1` on `/api/weibo/get-post-comments/v1`.
- Echo the required lookup scope (`mid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Weibo post Comments data, including text, authors, and timestamps, for feedback analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
