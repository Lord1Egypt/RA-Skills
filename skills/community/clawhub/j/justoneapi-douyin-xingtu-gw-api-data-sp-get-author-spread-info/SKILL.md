---
name: Douyin Creator Marketplace (Xingtu) Spread Metrics API
description: Call GET /api/douyin-xingtu/gw/api/data_sp/get_author_spread_info/v1 for Douyin Creator Marketplace (Xingtu) Spread Metrics through JustOneAPI with oAuthorId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_gw_api_data_sp_get_author_spread_info"}}
---

# Douyin Creator Marketplace (Xingtu) Spread Metrics

Use this focused JustOneAPI skill for spread Metrics in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/gw/api/data_sp/get_author_spread_info/v1`. Required non-token inputs are `oAuthorId`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) spread metrics data, including exposure, spread, and related performance indicators, for creator evaluation, campaign planning, and marketplace research.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `gw/api/data_sp/get_author_spread_info`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-gw-api-data-sp-get-author-spread-info`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `gwApiDataSpGetAuthorSpreadInfoV1` | `v1` | `GET` | `/api/douyin-xingtu/gw/api/data_sp/get_author_spread_info/v1` | Spread Metrics |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `flowType` | `query` | n/a | all | `string` | Flow type filter. Available Values: - `EXCLUDE`: Exclude - `INCLUDE`: Include |
| `flowType` enum | values | n/a | n/a | n/a | `EXCLUDE`, `INCLUDE` |
| `oAuthorId` | `query` | all | n/a | `string` | Author's unique ID |
| `onlyAssign` | `query` | n/a | all | `boolean` | Whether to only include assigned videos |
| `platform` | `query` | n/a | all | `string` | Platform type. Available Values: - `SHORT_VIDEO`: Short video - `LIVE_STREAMING`: Live streaming - `PICTURE_TEXT`: Picture and text - `SHORT_DRAMA`: Short drama |
| `platform` enum | values | n/a | n/a | n/a | `LIVE_STREAMING`, `PICTURE_TEXT`, `SHORT_DRAMA`, `SHORT_VIDEO` |
| `range` | `query` | n/a | all | `string` | Time range. Available Values: - `DAY_30`: Last 30 days - `DAY_90`: Last 90 days |
| `range` enum | values | n/a | n/a | n/a | `DAY_30`, `DAY_90` |
| `type` | `query` | n/a | all | `string` | Video type. Available Values: - `PERSONAL_VIDEO`: Personal video - `XINTU_VIDEO`: Xingtu video |
| `type` enum | values | n/a | n/a | n/a | `PERSONAL_VIDEO`, `XINTU_VIDEO` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `gwApiDataSpGetAuthorSpreadInfoV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `gwApiDataSpGetAuthorSpreadInfoV1`.

```bash
node {baseDir}/bin/run.mjs --operation "gwApiDataSpGetAuthorSpreadInfoV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"oAuthorId":"<oAuthorId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_spread_info&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_gw_api_data_sp_get_author_spread_info&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `gwApiDataSpGetAuthorSpreadInfoV1` on `/api/douyin-xingtu/gw/api/data_sp/get_author_spread_info/v1`.
- Echo the required lookup scope (`oAuthorId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) spread metrics data, including exposure, spread, and related performance indicators, for creator evaluation, campaign planning, and marketplace research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
