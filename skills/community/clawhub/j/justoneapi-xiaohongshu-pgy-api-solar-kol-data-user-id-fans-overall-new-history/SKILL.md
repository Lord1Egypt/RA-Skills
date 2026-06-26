---
name: Xiaohongshu Creator Marketplace (Pugongying) Follower Growth History API
description: Call GET /api/xiaohongshu-pgy/api/solar/kol/data/userId/fans_overall_new_history/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Growth History through JustOneAPI with userId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_pgy_api_solar_kol_data_user_id_fans_overall_new_history"}}
---

# Xiaohongshu Creator Marketplace (Pugongying) Follower Growth History

Use this focused JustOneAPI skill for follower Growth History in Xiaohongshu Creator Marketplace (Pugongying). It targets `GET /api/xiaohongshu-pgy/api/solar/kol/data/userId/fans_overall_new_history/v1`. Required non-token inputs are `userId`. OpenAPI describes it as: Get Xiaohongshu Creator Marketplace (Pugongying) follower Growth History data, including historical points, trend signals, and growth metrics, for trend tracking, audience analysis, and creator performance monitoring.

## Endpoint Scope

- Platform key: `xiaohongshu-pgy`
- Endpoint key: `api/solar/kol/data/userId/fans_overall_new_history`
- Platform family: Xiaohongshu Creator Marketplace (Pugongying)
- Skill slug: `justoneapi-xiaohongshu-pgy-api-solar-kol-data-user-id-fans-overall-new-history`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `apiSolarKolDataUserIdFansOverallNewHistoryV1` | `v1` | `GET` | `/api/xiaohongshu-pgy/api/solar/kol/data/userId/fans_overall_new_history/v1` | Follower Growth History |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `dateType` | `query` | n/a | all | `string` | Time range for data. Available Values: - `DAY_30`: Last 30 days - `DAY_90`: Last 90 days |
| `dateType` enum | values | n/a | n/a | n/a | `DAY_30`, `DAY_90` |
| `increaseType` | `query` | n/a | all | `string` | Type of growth data. Available Values: - `FANS_TOTAL`: Total fans - `FANS_INCREASE`: New fans increase |
| `increaseType` enum | values | n/a | n/a | n/a | `FANS_INCREASE`, `FANS_TOTAL` |
| `userId` | `query` | all | n/a | `string` | KOL's user ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `apiSolarKolDataUserIdFansOverallNewHistoryV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `apiSolarKolDataUserIdFansOverallNewHistoryV1`.

```bash
node {baseDir}/bin/run.mjs --operation "apiSolarKolDataUserIdFansOverallNewHistoryV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"userId":"<userId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_user_id_fans_overall_new_history&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_user_id_fans_overall_new_history&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `apiSolarKolDataUserIdFansOverallNewHistoryV1` on `/api/xiaohongshu-pgy/api/solar/kol/data/userId/fans_overall_new_history/v1`.
- Echo the required lookup scope (`userId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu Creator Marketplace (Pugongying) follower Growth History data, including historical points, trend signals, and growth metrics, for trend tracking, audience analysis, and creator performance monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
