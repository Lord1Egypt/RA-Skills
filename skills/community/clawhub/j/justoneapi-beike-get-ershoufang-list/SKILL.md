---
name: Beike Resale Housing List API
description: Call GET /api/beike/get-ershoufang-list/v1 for Beike Resale Housing List through JustOneAPI with cityId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_beike_get_ershoufang_list"}}
---

# Beike Resale Housing List

Use this focused JustOneAPI skill for resale Housing List in Beike. It targets `GET /api/beike/get-ershoufang-list/v1`. Required non-token inputs are `cityId`. OpenAPI describes it as: Get Beike resale Housing List data, including - Supports filtering by city/region, price range, and layout, for building search result pages for property portals and aggregating market data for regional housing trends.

## Endpoint Scope

- Platform key: `beike`
- Endpoint key: `get-ershoufang-list`
- Platform family: Beike
- Skill slug: `justoneapi-beike-get-ershoufang-list`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getErshoufangListV1` | `v1` | `GET` | `/api/beike/get-ershoufang-list/v1` | Resale Housing List |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `cityId` | `query` | all | n/a | `string` | The ID of the city (e.g., '110000' for Beijing) |
| `condition` | `query` | n/a | all | `string` | Filter conditions (e.g., region, price range, layout) |
| `offset` | `query` | n/a | all | `integer` | Pagination offset, starting from 0 (e.g., 0, 20, 40...) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getErshoufangListV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getErshoufangListV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getErshoufangListV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"cityId":"<cityId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_get_ershoufang_list&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_get_ershoufang_list&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getErshoufangListV1` on `/api/beike/get-ershoufang-list/v1`.
- Echo the required lookup scope (`cityId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Beike resale Housing List data, including - Supports filtering by city/region, price range, and layout, for building search result pages for property portals and aggregating market data for regional housing trends.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
