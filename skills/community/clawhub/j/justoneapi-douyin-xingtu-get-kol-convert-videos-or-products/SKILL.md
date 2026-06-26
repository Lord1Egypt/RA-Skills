---
name: Douyin Creator Marketplace (Xingtu) Conversion Resources API
description: Call GET /api/douyin-xingtu/get-kol-convert-videos-or-products/v1 for Douyin Creator Marketplace (Xingtu) Conversion Resources through JustOneAPI with detailType, kolId, and page.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_get_kol_convert_videos_or_products"}}
---

# Douyin Creator Marketplace (Xingtu) Conversion Resources

Use this focused JustOneAPI skill for conversion Resources in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/get-kol-convert-videos-or-products/v1`. Required non-token inputs are `detailType`, `kolId`, and `page`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) conversion Resources data, including products tied to a Douyin Xingtu creator's conversion activity, for commerce analysis and campaign optimization.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `get-kol-convert-videos-or-products`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-get-kol-convert-videos-or-products`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getKolConvertVideosOrProductsV1` | `v1` | `GET` | `/api/douyin-xingtu/get-kol-convert-videos-or-products/v1` | Conversion Resources |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `acceptCache` | `query` | n/a | all | `boolean` | Enable cache |
| `detailType` | `query` | all | n/a | `string` | Resource type. Available Values: - `_1`: Video Data - `_2`: Product Data |
| `detailType` enum | values | n/a | n/a | n/a | `_1`, `_2` |
| `kolId` | `query` | all | n/a | `string` | KOL ID |
| `page` | `query` | all | n/a | `integer` | Page number |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getKolConvertVideosOrProductsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getKolConvertVideosOrProductsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getKolConvertVideosOrProductsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"kolId":"<kolId>","detailType":"_1","page":1}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_convert_videos_or_products&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_convert_videos_or_products&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getKolConvertVideosOrProductsV1` on `/api/douyin-xingtu/get-kol-convert-videos-or-products/v1`.
- Echo the required lookup scope (`detailType`, `kolId`, and `page`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) conversion Resources data, including products tied to a Douyin Xingtu creator's conversion activity, for commerce analysis and campaign optimization.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
