---
name: Douyin E-commerce Item Details API
description: Call GET /api/douyin-ec/get-item-detail/v1 for Douyin E-commerce Item Details through JustOneAPI with itemId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_ec_get_item_detail"}}
---

# Douyin E-commerce Item Details

Use this focused JustOneAPI skill for item Details in Douyin E-commerce. It targets `GET /api/douyin-ec/get-item-detail/v1`. Required non-token inputs are `itemId`. OpenAPI describes it as: Get Douyin E-commerce item details, including price, title, and stock, for product monitoring and competitive analysis.

## Endpoint Scope

- Platform key: `douyin-ec`
- Endpoint key: `get-item-detail`
- Platform family: Douyin E-commerce
- Skill slug: `justoneapi-douyin-ec-get-item-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getDouyinEcItemDetailV1` | `v1` | `GET` | `/api/douyin-ec/get-item-detail/v1` | Item Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `itemId` | `query` | all | n/a | `string` | The unique ID of the item on Douyin E-commerce |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getDouyinEcItemDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getDouyinEcItemDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getDouyinEcItemDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"itemId":"<itemId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_ec_get_item_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_ec_get_item_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getDouyinEcItemDetailV1` on `/api/douyin-ec/get-item-detail/v1`.
- Echo the required lookup scope (`itemId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin E-commerce item details, including price, title, and stock, for product monitoring and competitive analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
