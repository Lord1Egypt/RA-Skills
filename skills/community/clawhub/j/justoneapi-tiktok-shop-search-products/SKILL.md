---
name: TikTok Shop Product Search API
description: Call GET /api/tiktok-shop/search-products/v1 for TikTok Shop Product Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_tiktok_shop_search_products"}}
---

# TikTok Shop Product Search

Use this focused JustOneAPI skill for product Search in TikTok Shop. It targets `GET /api/tiktok-shop/search-products/v1`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get TikTok Shop product Search data, including title, price, and sales, for market research and trend analysis, competitor product discovery, and monitoring product popularity in specific regions.

## Endpoint Scope

- Platform key: `tiktok-shop`
- Endpoint key: `search-products`
- Platform family: TikTok Shop
- Skill slug: `justoneapi-tiktok-shop-search-products`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchProductsV1` | `v1` | `GET` | `/api/tiktok-shop/search-products/v1` | Product Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | Search keyword |
| `offset` | `query` | n/a | all | `integer` | Search result offset |
| `pageToken` | `query` | n/a | all | `string` | Pagination token for the next page |
| `region` | `query` | n/a | all | `string` | Target region for product search. Available Values: - `US`: United States - `GB`: United Kingdom - `SG`: Singapore - `MY`: Malaysia - `PH`: Philippines - `TH`: Thailand - `VN`: Vietnam - `ID`: Indonesia |
| `region` enum | values | n/a | n/a | n/a | `GB`, `ID`, `MY`, `PH`, `SG`, `TH`, `US`, `VN` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchProductsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchProductsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchProductsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop_search_products&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop_search_products&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchProductsV1` on `/api/tiktok-shop/search-products/v1`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get TikTok Shop product Search data, including title, price, and sales, for market research and trend analysis, competitor product discovery, and monitoring product popularity in specific regions.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
