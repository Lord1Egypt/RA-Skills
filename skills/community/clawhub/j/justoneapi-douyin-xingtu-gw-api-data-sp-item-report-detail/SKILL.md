---
name: Douyin Creator Marketplace (Xingtu) Item Report Details API
description: Call GET /api/douyin-xingtu/gw/api/data_sp/item_report_detail/v1 for Douyin Creator Marketplace (Xingtu) Item Report Details through JustOneAPI with itemId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_gw_api_data_sp_item_report_detail"}}
---

# Douyin Creator Marketplace (Xingtu) Item Report Details

Use this focused JustOneAPI skill for item Report Details in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/gw/api/data_sp/item_report_detail/v1`. Required non-token inputs are `itemId`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) item Report Details data, including key metrics and report fields used, for item performance analysis.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `gw/api/data_sp/item_report_detail`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-gw-api-data-sp-item-report-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `gwApiDataSpItemReportDetailV1` | `v1` | `GET` | `/api/douyin-xingtu/gw/api/data_sp/item_report_detail/v1` | Item Report Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `itemId` | `query` | all | n/a | `string` | Item's unique ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `gwApiDataSpItemReportDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `gwApiDataSpItemReportDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "gwApiDataSpItemReportDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"itemId":"<itemId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_item_report_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_item_report_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `gwApiDataSpItemReportDetailV1` on `/api/douyin-xingtu/gw/api/data_sp/item_report_detail/v1`.
- Echo the required lookup scope (`itemId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) item Report Details data, including key metrics and report fields used, for item performance analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
