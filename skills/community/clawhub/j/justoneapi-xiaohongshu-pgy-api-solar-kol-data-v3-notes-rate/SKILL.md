---
name: Xiaohongshu Creator Marketplace (Pugongying) Note Performance Metrics API
description: Call GET /api/xiaohongshu-pgy/api/solar/kol/dataV3/notesRate/v1 for Xiaohongshu Creator Marketplace (Pugongying) Note Performance Metrics through JustOneAPI with userId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_pgy_api_solar_kol_data_v3_notes_rate"}}
---

# Xiaohongshu Creator Marketplace (Pugongying) Note Performance Metrics

Use this focused JustOneAPI skill for note Performance Metrics in Xiaohongshu Creator Marketplace (Pugongying). It targets `GET /api/xiaohongshu-pgy/api/solar/kol/dataV3/notesRate/v1`. Required non-token inputs are `userId`. OpenAPI describes it as: Get Xiaohongshu Creator Marketplace (Pugongying) note performance metrics data, including core metrics, trend signals, and performance indicators, for content efficiency analysis, creator benchmarking, and campaign planning.

## Endpoint Scope

- Platform key: `xiaohongshu-pgy`
- Endpoint key: `api/solar/kol/dataV3/notesRate`
- Platform family: Xiaohongshu Creator Marketplace (Pugongying)
- Skill slug: `justoneapi-xiaohongshu-pgy-api-solar-kol-data-v3-notes-rate`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `apiSolarKolDataV3NotesRateV1` | `v1` | `GET` | `/api/xiaohongshu-pgy/api/solar/kol/dataV3/notesRate/v1` | Note Performance Metrics |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `advertiseSwitch` | `query` | n/a | all | `string` | Advertisement filter. Available Values: - `ALL`: All notes - `ORGANIC_ONLY`: Organic notes only |
| `advertiseSwitch` enum | values | n/a | n/a | n/a | `ALL`, `ORGANIC_ONLY` |
| `business` | `query` | n/a | all | `string` | Business type. Available Values: - `DAILY_NOTE`: Daily notes - `COOPERATE_NOTE`: Cooperative notes |
| `business` enum | values | n/a | n/a | n/a | `COOPERATE_NOTE`, `DAILY_NOTE` |
| `dateType` | `query` | n/a | all | `string` | Time range for data. Available Values: - `DAY_30`: Last 30 days - `DAY_90`: Last 90 days |
| `dateType` enum | values | n/a | n/a | n/a | `DAY_30`, `DAY_90` |
| `noteType` | `query` | n/a | all | `string` | Type of note. Available Values: - `PHOTO_TEXT_AND_VIDEO`: Photo and Video - `PHOTO_TEXT`: Photo and Text - `VIDEO`: Video only |
| `noteType` enum | values | n/a | n/a | n/a | `PHOTO_TEXT`, `PHOTO_TEXT_AND_VIDEO`, `VIDEO` |
| `userId` | `query` | all | n/a | `string` | KOL's user ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `apiSolarKolDataV3NotesRateV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `apiSolarKolDataV3NotesRateV1`.

```bash
node {baseDir}/bin/run.mjs --operation "apiSolarKolDataV3NotesRateV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"userId":"<userId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v3_notes_rate&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_data_v3_notes_rate&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `apiSolarKolDataV3NotesRateV1` on `/api/xiaohongshu-pgy/api/solar/kol/dataV3/notesRate/v1`.
- Echo the required lookup scope (`userId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu Creator Marketplace (Pugongying) note performance metrics data, including core metrics, trend signals, and performance indicators, for content efficiency analysis, creator benchmarking, and campaign planning.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
