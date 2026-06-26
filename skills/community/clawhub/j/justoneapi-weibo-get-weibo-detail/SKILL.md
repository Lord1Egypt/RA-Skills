---
name: Weibo Post Details API
description: Call GET /api/weibo/get-weibo-detail/v1 for Weibo Post Details through JustOneAPI with id.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weibo_get_weibo_detail"}}
---

# Weibo Post Details

Use this focused JustOneAPI skill for post Details in Weibo. It targets `GET /api/weibo/get-weibo-detail/v1`. Required non-token inputs are `id`. OpenAPI describes it as: Get Weibo post Details data, including media, author metadata, and engagement counts, for post analysis, archiving, and campaign monitoring.

## Endpoint Scope

- Platform key: `weibo`
- Endpoint key: `get-weibo-detail`
- Platform family: Weibo
- Skill slug: `justoneapi-weibo-get-weibo-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getWeiboDetailsV1` | `v1` | `GET` | `/api/weibo/get-weibo-detail/v1` | Post Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `id` | `query` | all | n/a | `string` | Weibo post ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getWeiboDetailsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getWeiboDetailsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getWeiboDetailsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"id":"<id>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_weibo_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_get_weibo_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getWeiboDetailsV1` on `/api/weibo/get-weibo-detail/v1`.
- Echo the required lookup scope (`id`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Weibo post Details data, including media, author metadata, and engagement counts, for post analysis, archiving, and campaign monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
