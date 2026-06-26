---
name: Amazon Product Details API
description: Call GET /api/amazon/get-product-detail/v1 for Amazon Product Details through JustOneAPI with asin.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_amazon_get_product_detail"}}
---

# Amazon Product Details

Use this focused JustOneAPI skill for product Details in Amazon. It targets `GET /api/amazon/get-product-detail/v1`. Required non-token inputs are `asin`. OpenAPI describes it as: Get Amazon product Details data, including title, brand, and price, for building product catalogs and enriching item content (e.g., images), price monitoring and availability tracking, and e-commerce analytics and competitor tracking.

## Endpoint Scope

- Platform key: `amazon`
- Endpoint key: `get-product-detail`
- Platform family: Amazon
- Skill slug: `justoneapi-amazon-get-product-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getAmazonProductDetailV1` | `v1` | `GET` | `/api/amazon/get-product-detail/v1` | Product Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `asin` | `query` | all | n/a | `string` | ASIN (Amazon Standard Identification Number) |
| `country` | `query` | n/a | all | `string` | Country code for the Amazon product. Available Values: - `US`: United States - `AU`: Australia - `BR`: Brazil - `CA`: Canada - `CN`: China - `FR`: France - `DE`: Germany - `IN`: India - `IT`: Italy - `MX`: Mexico - `NL`: Netherlands - `SG`: Singapore - `ES`: Spain - `TR`: Turkey - `AE`: United Arab Emirates - `GB`: United Kingdom - `JP`: Japan - `SA`: Saudi Arabia - `PL`: Poland - `SE`: Sweden - `BE`: Belgium - `EG`: Egypt - `ZA`: South Africa - `IE`: Ireland |
| `country` enum | values | n/a | n/a | n/a | `AE`, `AU`, `BE`, `BR`, `CA`, `CN`, `DE`, `EG`, `ES`, `FR`, `GB`, `IE`, `IN`, `IT`, `JP`, `MX`, `NL`, `PL`, `SA`, `SE`, `SG`, `TR`, `US`, `ZA` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getAmazonProductDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getAmazonProductDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getAmazonProductDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"asin":"<asin>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_product_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon_get_product_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getAmazonProductDetailV1` on `/api/amazon/get-product-detail/v1`.
- Echo the required lookup scope (`asin`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Amazon product Details data, including title, brand, and price, for building product catalogs and enriching item content (e.g., images), price monitoring and availability tracking, and e-commerce analytics and competitor tracking.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
