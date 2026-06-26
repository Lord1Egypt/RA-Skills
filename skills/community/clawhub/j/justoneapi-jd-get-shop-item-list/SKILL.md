---
name: JD.com Shop Product List API
description: Call GET /api/jd/get-shop-item-list/v1 for JD.com Shop Product List through JustOneAPI with shopId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_jd_get_shop_item_list"}}
---

# JD.com Shop Product List

Use this focused JustOneAPI skill for shop Product List in JD.com. It targets `GET /api/jd/get-shop-item-list/v1`. Required non-token inputs are `shopId`. OpenAPI describes it as: Get JD.com shop Product List data, including item titles, prices, and images, for catalog tracking and seller research.

## Endpoint Scope

- Platform key: `jd`
- Endpoint key: `get-shop-item-list`
- Platform family: JD.com
- Skill slug: `justoneapi-jd-get-shop-item-list`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getJdShopItemListV1` | `v1` | `GET` | `/api/jd/get-shop-item-list/v1` | Shop Product List |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `page` | `query` | n/a | all | `string` | Page number for paginated comments |
| `shopId` | `query` | all | n/a | `string` | A unique shop identifier on JD.com (Shop ID) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getJdShopItemListV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getJdShopItemListV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getJdShopItemListV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"shopId":"<shopId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_shop_item_list&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_jd_get_shop_item_list&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getJdShopItemListV1` on `/api/jd/get-shop-item-list/v1`.
- Echo the required lookup scope (`shopId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get JD.com shop Product List data, including item titles, prices, and images, for catalog tracking and seller research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
