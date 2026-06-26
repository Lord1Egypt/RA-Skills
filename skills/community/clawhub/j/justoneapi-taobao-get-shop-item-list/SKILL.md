---
name: Taobao and Tmall Shop Product List API
description: Call 3 get-shop-item-list versions for Taobao and Tmall Shop Product List through JustOneAPI with shopId and userId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_taobao_get_shop_item_list"}}
---

# Taobao and Tmall Shop Product List

Use this focused JustOneAPI skill for shop Product List in Taobao and Tmall. It targets 3 versioned paths under `/api/taobao/get-shop-item-list`. Required non-token inputs are `shopId` and `userId`. OpenAPI describes it as: Get Taobao and Tmall shop Product List data, including item titles, prices, and images, for seller research and catalog tracking.

## Endpoint Scope

- Platform key: `taobao`
- Endpoint key: `get-shop-item-list`
- Platform family: Taobao and Tmall
- Skill slug: `justoneapi-taobao-get-shop-item-list`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getTaobaoShopItemListV1` | `v1` | `GET` | `/api/taobao/get-shop-item-list/v1` | Shop Product List |
| `getShopItemListV2` | `v2` | `GET` | `/api/taobao/get-shop-item-list/v2` | Shop Product List |
| `getShopItemListV3` | `v3` | `GET` | `/api/taobao/get-shop-item-list/v3` | Shop Product List |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `page` | `query` | n/a | all | `integer` | Page number for pagination |
| `shopId` | `query` | `getShopItemListV2`, `getShopItemListV3` | n/a | `string` | Unique shop identifier on Taobao/Tmall (shop ID) |
| `sort` | `query` | n/a | all | `string` | Sort order for the result set. Available Values: - `_sale`: Sales - `_default`: Default |
| `sort` enum | values | n/a | n/a | n/a | `_bid`, `_default`, `_sale`, `bid`, `coefp`, `hotsell`, `oldstarts` |
| `userId` | `query` | all | n/a | `string` | Shop identifier. Also known as Seller ID or User ID (they refer to the same value) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

This skill groups 3 endpoint versions because their paths share `get-shop-item-list` after removing the trailing version segment.
Choose the version the user requested; if no version was requested, pick the operation whose required inputs match the data the user has.

- `getTaobaoShopItemListV1` (`v1`): required inputs `userId`.
- `getShopItemListV2` (`v2`): required inputs `userId` and `shopId`.
- `getShopItemListV3` (`v3`): required inputs `userId` and `shopId`.

## Run This Endpoint

Supported operation IDs in this skill: `getTaobaoShopItemListV1`, `getShopItemListV2`, `getShopItemListV3`.

```bash
node {baseDir}/bin/run.mjs --operation "getTaobaoShopItemListV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"userId":"<userId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_shop_item_list&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_shop_item_list&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getTaobaoShopItemListV1` on `/api/taobao/get-shop-item-list/v1`.
- Echo the required lookup scope (`shopId` and `userId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Taobao and Tmall shop Product List data, including item titles, prices, and images, for seller research and catalog tracking.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
