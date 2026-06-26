---
name: Xiaohongshu Creator Marketplace (Pugongying) Note Performance Metrics API
description: Call GET /api/xiaohongshu-pgy/get-kol-note-rate/v1 for Xiaohongshu Creator Marketplace (Pugongying) Note Performance Metrics through JustOneAPI with kolId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_pgy_get_kol_note_rate"}}
---

# Xiaohongshu Creator Marketplace (Pugongying) Note Performance Metrics

Use this focused JustOneAPI skill for note Performance Metrics in Xiaohongshu Creator Marketplace (Pugongying). It targets `GET /api/xiaohongshu-pgy/get-kol-note-rate/v1`. Required non-token inputs are `kolId`. OpenAPI describes it as: Get Xiaohongshu Creator Marketplace (Pugongying) note performance metrics data, including core metrics, trend signals, and performance indicators, for content efficiency analysis, creator benchmarking, and campaign planning.

## Endpoint Scope

- Platform key: `xiaohongshu-pgy`
- Endpoint key: `get-kol-note-rate`
- Platform family: Xiaohongshu Creator Marketplace (Pugongying)
- Skill slug: `justoneapi-xiaohongshu-pgy-get-kol-note-rate`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getKolNoteRateV1` | `v1` | `GET` | `/api/xiaohongshu-pgy/get-kol-note-rate/v1` | Note Performance Metrics |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `acceptCache` | `query` | n/a | all | `boolean` | Enable cache |
| `adSwitch` | `query` | n/a | all | `string` | Ad filter. Available Values: - `_1`: Full traffic (All notes) - `_0`: Natural traffic (Organic notes) |
| `adSwitch` enum | values | n/a | n/a | n/a | `_0`, `_1` |
| `business` | `query` | n/a | all | `string` | Business type. Available Values: - `_0`: Normal notes - `_1`: Cooperation notes |
| `business` enum | values | n/a | n/a | n/a | `_0`, `_1` |
| `dateType` | `query` | n/a | all | `string` | Date type. Available Values: - `_1`: Last 30 days - `_2`: Last 90 days |
| `dateType` enum | values | n/a | n/a | n/a | `_1`, `_2` |
| `kolId` | `query` | all | n/a | `string` | KOL ID |
| `noteType` | `query` | n/a | all | `string` | Note type. Available Values: - `_1`: Photo and Text - `_2`: Video - `_3`: Photo and Video |
| `noteType` enum | values | n/a | n/a | n/a | `_1`, `_2`, `_3` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getKolNoteRateV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getKolNoteRateV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getKolNoteRateV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"kolId":"<kolId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_note_rate&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_note_rate&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getKolNoteRateV1` on `/api/xiaohongshu-pgy/get-kol-note-rate/v1`.
- Echo the required lookup scope (`kolId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu Creator Marketplace (Pugongying) note performance metrics data, including core metrics, trend signals, and performance indicators, for content efficiency analysis, creator benchmarking, and campaign planning.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
