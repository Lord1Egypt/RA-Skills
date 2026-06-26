---
name: Xiaohongshu Creator Marketplace (Pugongying) Data Summary API
description: Call GET /api/xiaohongshu-pgy/get-kol-data-summary/v2 for Xiaohongshu Creator Marketplace (Pugongying) Data Summary through JustOneAPI with business and kolId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_pgy_get_kol_data_summary"}}
---

# Xiaohongshu Creator Marketplace (Pugongying) Data Summary

Use this focused JustOneAPI skill for data Summary in Xiaohongshu Creator Marketplace (Pugongying). It targets `GET /api/xiaohongshu-pgy/get-kol-data-summary/v2`. Required non-token inputs are `business` and `kolId`. OpenAPI describes it as: Get Xiaohongshu Creator Marketplace (Pugongying) summary data, including activity, engagement, and audience growth, for creator evaluation, campaign planning, and creator benchmarking.

## Endpoint Scope

- Platform key: `xiaohongshu-pgy`
- Endpoint key: `get-kol-data-summary`
- Platform family: Xiaohongshu Creator Marketplace (Pugongying)
- Skill slug: `justoneapi-xiaohongshu-pgy-get-kol-data-summary`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getKolDataSummaryV2` | `v2` | `GET` | `/api/xiaohongshu-pgy/get-kol-data-summary/v2` | Data Summary |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `acceptCache` | `query` | n/a | all | `boolean` | Enable cache |
| `business` | `query` | all | n/a | `string` | Business type. Available Values: - `_0`: Normal notes - `_1`: Cooperation notes |
| `business` enum | values | n/a | n/a | n/a | `_0`, `_1` |
| `kolId` | `query` | all | n/a | `string` | KOL ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getKolDataSummaryV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getKolDataSummaryV2`.

```bash
node {baseDir}/bin/run.mjs --operation "getKolDataSummaryV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"kolId":"<kolId>","business":"_0"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_data_summary&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_data_summary&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getKolDataSummaryV2` on `/api/xiaohongshu-pgy/get-kol-data-summary/v2`.
- Echo the required lookup scope (`business` and `kolId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu Creator Marketplace (Pugongying) summary data, including activity, engagement, and audience growth, for creator evaluation, campaign planning, and creator benchmarking.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
