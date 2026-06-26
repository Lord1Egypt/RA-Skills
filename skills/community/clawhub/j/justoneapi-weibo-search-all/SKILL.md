---
name: Weibo Keyword Search API
description: Call GET /api/weibo/search-all/v2 for Weibo Keyword Search through JustOneAPI with endDay, endHour, q, startDay, and startHour.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weibo_search_all"}}
---

# Weibo Keyword Search

Use this focused JustOneAPI skill for keyword Search in Weibo. It targets `GET /api/weibo/search-all/v2`. Required non-token inputs are `endDay`, `endHour`, `q`, `startDay`, and `startHour`. OpenAPI describes it as: Get Weibo keyword Search data, including authors, publish times, and engagement signals, for trend monitoring.

## Endpoint Scope

- Platform key: `weibo`
- Endpoint key: `search-all`
- Platform family: Weibo
- Skill slug: `justoneapi-weibo-search-all`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchAllV2` | `v2` | `GET` | `/api/weibo/search-all/v2` | Keyword Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `contains` | `query` | n/a | all | `string` | Contains filter for the result set. Available Values: - `ALL`: All - `PICTURE`: Has Picture - `VIDEO`: Has Video - `MUSIC`: Has Music - `LINK`: Has Link |
| `contains` enum | values | n/a | n/a | n/a | `ALL`, `LINK`, `MUSIC`, `PICTURE`, `VIDEO` |
| `endDay` | `query` | all | n/a | `string` | End Day (yyyy-MM-dd) |
| `endHour` | `query` | all | n/a | `integer` | End Hour (0-23) |
| `hotSort` | `query` | n/a | all | `boolean` | Hot sort, true for hot sort, false for time sort. Default is false |
| `page` | `query` | n/a | all | `integer` | Page number, starting with 1 |
| `q` | `query` | all | n/a | `string` | Search Keywords |
| `startDay` | `query` | all | n/a | `string` | Start Day (yyyy-MM-dd) |
| `startHour` | `query` | all | n/a | `integer` | Start Hour (0-23) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchAllV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchAllV2`.

```bash
node {baseDir}/bin/run.mjs --operation "searchAllV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"q":"<q>","startDay":"<startDay>","startHour":1,"endDay":"<endDay>","endHour":1}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_search_all&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo_search_all&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchAllV2` on `/api/weibo/search-all/v2`.
- Echo the required lookup scope (`endDay`, `endHour`, `q`, `startDay`, and `startHour`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Weibo keyword Search data, including authors, publish times, and engagement signals, for trend monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
