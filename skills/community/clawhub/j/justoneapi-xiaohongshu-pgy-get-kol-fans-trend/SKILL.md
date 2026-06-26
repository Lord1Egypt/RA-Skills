---
name: Xiaohongshu Creator Marketplace (Pugongying) Follower Growth History API
description: Call GET /api/xiaohongshu-pgy/get-kol-fans-trend/v1 for Xiaohongshu Creator Marketplace (Pugongying) Follower Growth History through JustOneAPI with dateType, increaseType, and kolId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_pgy_get_kol_fans_trend"}}
---

# Xiaohongshu Creator Marketplace (Pugongying) Follower Growth History

Use this focused JustOneAPI skill for follower Growth History in Xiaohongshu Creator Marketplace (Pugongying). It targets `GET /api/xiaohongshu-pgy/get-kol-fans-trend/v1`. Required non-token inputs are `dateType`, `increaseType`, and `kolId`. OpenAPI describes it as: Get Xiaohongshu Creator Marketplace (Pugongying) follower growth history data, including historical audience changes over time, for creator evaluation, campaign planning, and creator benchmarking.

## Endpoint Scope

- Platform key: `xiaohongshu-pgy`
- Endpoint key: `get-kol-fans-trend`
- Platform family: Xiaohongshu Creator Marketplace (Pugongying)
- Skill slug: `justoneapi-xiaohongshu-pgy-get-kol-fans-trend`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getKolFansTrendV1` | `v1` | `GET` | `/api/xiaohongshu-pgy/get-kol-fans-trend/v1` | Follower Growth History |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `acceptCache` | `query` | n/a | all | `boolean` | Enable cache |
| `dateType` | `query` | all | n/a | `string` | Date type. Available Values: - `_1`: Last 30 days - `_2`: Last 60 days |
| `dateType` enum | values | n/a | n/a | n/a | `_1`, `_2` |
| `increaseType` | `query` | all | n/a | `string` | Increase type. Available Values: - `_1`: Total fans - `_2`: New fans increase |
| `increaseType` enum | values | n/a | n/a | n/a | `_1`, `_2` |
| `kolId` | `query` | all | n/a | `string` | KOL ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getKolFansTrendV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getKolFansTrendV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getKolFansTrendV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"kolId":"<kolId>","dateType":"_1","increaseType":"_1"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_fans_trend&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_get_kol_fans_trend&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getKolFansTrendV1` on `/api/xiaohongshu-pgy/get-kol-fans-trend/v1`.
- Echo the required lookup scope (`dateType`, `increaseType`, and `kolId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu Creator Marketplace (Pugongying) follower growth history data, including historical audience changes over time, for creator evaluation, campaign planning, and creator benchmarking.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
