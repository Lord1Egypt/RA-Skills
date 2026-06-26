---
name: Taobao and Tmall Product Search API
description: Call GET /api/taobao/search-item-list/v1 for Taobao and Tmall Product Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_taobao_search_item_list"}}
---

# Taobao and Tmall Product Search

Use this focused JustOneAPI skill for product Search in Taobao and Tmall. It targets `GET /api/taobao/search-item-list/v1`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Taobao and Tmall product Search data, including titles, prices, and images, for product discovery.

## Endpoint Scope

- Platform key: `taobao`
- Endpoint key: `search-item-list`
- Platform family: Taobao and Tmall
- Skill slug: `justoneapi-taobao-search-item-list`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchItemListV1` | `v1` | `GET` | `/api/taobao/search-item-list/v1` | Product Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `endPrice` | `query` | n/a | all | `string` | Maximum price filter (inclusive) |
| `keyword` | `query` | all | n/a | `string` | Search keyword |
| `page` | `query` | n/a | all | `integer` | Page number for pagination |
| `sort` | `query` | n/a | all | `string` | Sort order for the result set. Available Values: - `_sale`: Sales - `_bid`: Price: High to Low - `bid`: Price: Low to High - `_coefp`: General |
| `sort` enum | values | n/a | n/a | n/a | `_bid`, `_coefp`, `_sale`, `bid` |
| `startPrice` | `query` | n/a | all | `string` | Minimum price filter (inclusive) |
| `tmall` | `query` | n/a | all | `boolean` | Whether to filter results to Tmall only |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchItemListV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchItemListV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchItemListV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_search_item_list&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_search_item_list&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchItemListV1` on `/api/taobao/search-item-list/v1`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Taobao and Tmall product Search data, including titles, prices, and images, for product discovery.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
