---
name: Amazon Best Sellers API
description: Call GET /api/amazon/get-best-sellers/v1 for Amazon Best Sellers through JustOneAPI with category.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_amazon_get_best_sellers"}}
---

# Amazon Best Sellers

Use this focused JustOneAPI skill for best Sellers in Amazon. It targets `GET /api/amazon/get-best-sellers/v1`. Required non-token inputs are `category`. OpenAPI describes it as: Get Amazon best Sellers data, including rank positions, product metadata, and pricing, for identifying trending products in specific categories, market share analysis and category research, and tracking sales rank and popularity over time.

## Endpoint Scope

- Platform key: `amazon`
- Endpoint key: `get-best-sellers`
- Platform family: Amazon
- Skill slug: `justoneapi-amazon-get-best-sellers`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getBestSellersV1` | `v1` | `GET` | `/api/amazon/get-best-sellers/v1` | Best Sellers |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `category` | `query` | all | n/a | `string` | Best sellers category to return products for (e.g. 'baby-products' or 'baby-products/166777011'). The value is derived from the URL path of the Amazon Best Sellers page, such as: https://www.amazon.com/Best-Sellers-Baby-Baby-Toddler-Feeding-Supplies/zgbs/baby-products/166777011 |
| `country` | `query` | n/a | all | `string` | Country code for the Amazon product. Available Values: - `US`: United States - `AU`: Australia - `BR`: Brazil - `CA`: Canada - `CN`: China - `FR`: France - `DE`: Germany - `IN`: India - `IT`: Italy - `MX`: Mexico - `NL`: Netherlands - `SG`: Singapore - `ES`: Spain - `TR`: Turkey - `AE`: United Arab Emirates - `GB`: United Kingdom - `JP`: Japan - `SA`: Saudi Arabia - `PL`: Poland - `SE`: Sweden - `BE`: Belgium - `EG`: Egypt - `ZA`: South Africa - `IE`: Ireland |
| `country` enum | values | n/a | n/a | n/a | `AE`, `AU`, `BE`, `BR`, `CA`, `CN`, `DE`, `EG`, `ES`, `FR`, `GB`, `IE`, `IN`, `IT`, `JP`, `MX`, `NL`, `PL`, `SA`, `SE`, `SG`, `TR`, `US`, `ZA` |
| `page` | `query` | n/a | all | `integer` | Page number for pagination |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getBestSellersV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getBestSellersV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getBestSellersV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"category":"<category>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_best_sellers&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_best_sellers&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getBestSellersV1` on `/api/amazon/get-best-sellers/v1`.
- Echo the required lookup scope (`category`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Amazon best Sellers data, including rank positions, product metadata, and pricing, for identifying trending products in specific categories, market share analysis and category research, and tracking sales rank and popularity over time.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
