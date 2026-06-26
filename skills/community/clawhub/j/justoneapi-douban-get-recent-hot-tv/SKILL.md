---
name: Douban Movie Recent Hot Tv API
description: Call GET /api/douban/get-recent-hot-tv/v1 for Douban Movie Recent Hot Tv through JustOneAPI.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douban_get_recent_hot_tv"}}
---

# Douban Movie Recent Hot Tv

Use this focused JustOneAPI skill for recent Hot Tv in Douban Movie. It targets `GET /api/douban/get-recent-hot-tv/v1`. It has no required non-token parameters. OpenAPI describes it as: Get Douban recent Hot Tv data, including ratings, posters, and subject metadata, for series discovery and trend monitoring.

## Endpoint Scope

- Platform key: `douban`
- Endpoint key: `get-recent-hot-tv`
- Platform family: Douban Movie
- Skill slug: `justoneapi-douban-get-recent-hot-tv`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getRecentHotTvV1` | `v1` | `GET` | `/api/douban/get-recent-hot-tv/v1` | Recent Hot Tv |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `page` | `query` | n/a | all | `integer` | Page number for pagination |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getRecentHotTvV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getRecentHotTvV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getRecentHotTvV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"key":"value"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_recent_hot_tv&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_recent_hot_tv&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getRecentHotTvV1` on `/api/douban/get-recent-hot-tv/v1`.
- Prioritize fields that support this endpoint purpose: Get Douban recent Hot Tv data, including ratings, posters, and subject metadata, for series discovery and trend monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
