---
name: Weibo Hot Search API
description: Call GET /api/weibo/hot-search/v1 for Weibo Hot Search through JustOneAPI.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weibo_hot_search"}}
---

# Weibo Hot Search

Use this focused JustOneAPI skill for hot Search in Weibo. It targets `GET /api/weibo/hot-search/v1`. It has no required non-token parameters. OpenAPI describes it as: Get Weibo hot Search data, including ranking data, for trend monitoring, newsroom workflows, and topic discovery.

## Endpoint Scope

- Platform key: `weibo`
- Endpoint key: `hot-search`
- Platform family: Weibo
- Skill slug: `justoneapi-weibo-hot-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `hotSearchV1` | `v1` | `GET` | `/api/weibo/hot-search/v1` | Hot Search |

## Inputs

No non-token path or query parameters are documented for this endpoint group.

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `hotSearchV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `hotSearchV1`.

```bash
node {baseDir}/bin/run.mjs --operation "hotSearchV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"key":"value"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_hot_search&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_hot_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `hotSearchV1` on `/api/weibo/hot-search/v1`.
- Prioritize fields that support this endpoint purpose: Get Weibo hot Search data, including ranking data, for trend monitoring, newsroom workflows, and topic discovery.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
