---
name: Taobao and Tmall Product Details API
description: Call 5 get-item-detail versions for Taobao and Tmall Product Details through JustOneAPI with itemId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_taobao_get_item_detail"}}
---

# Taobao and Tmall Product Details

Use this focused JustOneAPI skill for product Details in Taobao and Tmall. It targets 5 versioned paths under `/api/taobao/get-item-detail`. Required non-token inputs are `itemId`. OpenAPI describes it as: Get Taobao and Tmall product Details data, including pricing, images, and shop details, for product research, catalog monitoring, and ecommerce analysis.

## Endpoint Scope

- Platform key: `taobao`
- Endpoint key: `get-item-detail`
- Platform family: Taobao and Tmall
- Skill slug: `justoneapi-taobao-get-item-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getTaobaoItemDetailV1` | `v1` | `GET` | `/api/taobao/get-item-detail/v1` | Product Details |
| `getItemDetailV2` | `v2` | `GET` | `/api/taobao/get-item-detail/v2` | Product Details |
| `getItemDetailV4` | `v4` | `GET` | `/api/taobao/get-item-detail/v4` | Product Details |
| `getItemDetailV5` | `v5` | `GET` | `/api/taobao/get-item-detail/v5` | Product Details |
| `getItemDetailV9` | `v9` | `GET` | `/api/taobao/get-item-detail/v9` | Product Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `itemId` | `query` | all | n/a | `string` | AUnique product identifier on Taobao/Tmall (item ID) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

This skill groups 5 endpoint versions because their paths share `get-item-detail` after removing the trailing version segment.
Choose the version the user requested; if no version was requested, pick the operation whose required inputs match the data the user has.

- `getTaobaoItemDetailV1` (`v1`): required inputs `itemId`.
- `getItemDetailV2` (`v2`): required inputs `itemId`.
- `getItemDetailV4` (`v4`): required inputs `itemId`.
- `getItemDetailV5` (`v5`): required inputs `itemId`.
- `getItemDetailV9` (`v9`): required inputs `itemId`.

## Run This Endpoint

Supported operation IDs in this skill: `getTaobaoItemDetailV1`, `getItemDetailV2`, `getItemDetailV4`, `getItemDetailV5`, `getItemDetailV9`.

```bash
node {baseDir}/bin/run.mjs --operation "getTaobaoItemDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"itemId":"<itemId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_item_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao_get_item_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getTaobaoItemDetailV1` on `/api/taobao/get-item-detail/v1`.
- Echo the required lookup scope (`itemId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Taobao and Tmall product Details data, including pricing, images, and shop details, for product research, catalog monitoring, and ecommerce analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
