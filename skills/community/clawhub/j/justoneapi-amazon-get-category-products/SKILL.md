---
name: Amazon Products By Category API
description: Call GET /api/amazon/get-category-products/v1 for Amazon Products By Category through JustOneAPI with categoryId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_amazon_get_category_products"}}
---

# Amazon Products By Category

Use this focused JustOneAPI skill for products By Category in Amazon. It targets `GET /api/amazon/get-category-products/v1`. Required non-token inputs are `categoryId`. OpenAPI describes it as: Get Amazon products By Category data, including title, price, and rating, for category-based product discovery and returns product information such as title, price, and rating.

## Endpoint Scope

- Platform key: `amazon`
- Endpoint key: `get-category-products`
- Platform family: Amazon
- Skill slug: `justoneapi-amazon-get-category-products`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getProductsByCategoryV1` | `v1` | `GET` | `/api/amazon/get-category-products/v1` | Products By Category |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `categoryId` | `query` | all | n/a | `string` | For example: https://amazon.com/s?node=172282 - the Amazon Category ID is 172282 |
| `country` | `query` | n/a | all | `string` | Country code for the Amazon product. Available Values: - `US`: United States - `AU`: Australia - `BR`: Brazil - `CA`: Canada - `CN`: China - `FR`: France - `DE`: Germany - `IN`: India - `IT`: Italy - `MX`: Mexico - `NL`: Netherlands - `SG`: Singapore - `ES`: Spain - `TR`: Turkey - `AE`: United Arab Emirates - `GB`: United Kingdom - `JP`: Japan - `SA`: Saudi Arabia - `PL`: Poland - `SE`: Sweden - `BE`: Belgium - `EG`: Egypt - `ZA`: South Africa - `IE`: Ireland |
| `country` enum | values | n/a | n/a | n/a | `AE`, `AU`, `BE`, `BR`, `CA`, `CN`, `DE`, `EG`, `ES`, `FR`, `GB`, `IE`, `IN`, `IT`, `JP`, `MX`, `NL`, `PL`, `SA`, `SE`, `SG`, `TR`, `US`, `ZA` |
| `page` | `query` | n/a | all | `integer` | Page number for pagination |
| `sortBy` | `query` | n/a | all | `string` | Sort by. Available Values: - `RELEVANCE`: Relevance - `LOWEST_PRICE`: Lowest Price - `HIGHEST_PRICE`: Highest Price - `REVIEWS`: Reviews - `NEWEST`: Newest - `BEST_SELLERS`: Best Sellers |
| `sortBy` enum | values | n/a | n/a | n/a | `BEST_SELLERS`, `HIGHEST_PRICE`, `LOWEST_PRICE`, `NEWEST`, `RELEVANCE`, `REVIEWS` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getProductsByCategoryV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getProductsByCategoryV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getProductsByCategoryV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"categoryId":"<categoryId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_category_products&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_category_products&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getProductsByCategoryV1` on `/api/amazon/get-category-products/v1`.
- Echo the required lookup scope (`categoryId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Amazon products By Category data, including title, price, and rating, for category-based product discovery and returns product information such as title, price, and rating.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
