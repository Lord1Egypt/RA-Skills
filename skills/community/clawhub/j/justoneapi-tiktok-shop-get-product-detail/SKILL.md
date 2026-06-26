---
name: TikTok Shop Product Details API
description: Call GET /api/tiktok-shop/get-product-detail/v1 for TikTok Shop Product Details through JustOneAPI with productId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_tiktok_shop_get_product_detail"}}
---

# TikTok Shop Product Details

Use this focused JustOneAPI skill for product Details in TikTok Shop. It targets `GET /api/tiktok-shop/get-product-detail/v1`. Required non-token inputs are `productId`. OpenAPI describes it as: Get TikTok Shop product Details data, including title, description, and price, for building product catalogs, price and stock monitoring, and in-depth product analysis.

## Endpoint Scope

- Platform key: `tiktok-shop`
- Endpoint key: `get-product-detail`
- Platform family: TikTok Shop
- Skill slug: `justoneapi-tiktok-shop-get-product-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getTiktokShopProductDetailV1` | `v1` | `GET` | `/api/tiktok-shop/get-product-detail/v1` | Product Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `productId` | `query` | all | n/a | `string` | TikTok Shop Product ID |
| `region` | `query` | n/a | all | `string` | Target region for product detail. Available Values: - `US`: United States - `GB`: United Kingdom - `SG`: Singapore - `MY`: Malaysia - `PH`: Philippines - `TH`: Thailand - `VN`: Vietnam - `ID`: Indonesia |
| `region` enum | values | n/a | n/a | n/a | `GB`, `ID`, `MY`, `PH`, `SG`, `TH`, `US`, `VN` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getTiktokShopProductDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getTiktokShopProductDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getTiktokShopProductDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"productId":"<productId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop_get_product_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop_get_product_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getTiktokShopProductDetailV1` on `/api/tiktok-shop/get-product-detail/v1`.
- Echo the required lookup scope (`productId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get TikTok Shop product Details data, including title, description, and price, for building product catalogs, price and stock monitoring, and in-depth product analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
