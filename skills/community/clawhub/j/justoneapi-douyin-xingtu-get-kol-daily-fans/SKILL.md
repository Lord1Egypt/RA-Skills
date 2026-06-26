---
name: Douyin Creator Marketplace (Xingtu) Follower Growth Trend API
description: Call GET /api/douyin-xingtu/get-kol-daily-fans/v1 for Douyin Creator Marketplace (Xingtu) Follower Growth Trend through JustOneAPI with endDate, kolId, and startDate.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_get_kol_daily_fans"}}
---

# Douyin Creator Marketplace (Xingtu) Follower Growth Trend

Use this focused JustOneAPI skill for follower Growth Trend in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/get-kol-daily-fans/v1`. Required non-token inputs are `endDate`, `kolId`, and `startDate`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) follower Growth Trend data, including historical audience changes over time, for creator evaluation, campaign planning, and marketplace research.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `get-kol-daily-fans`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-get-kol-daily-fans`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getKolDailyFansV1` | `v1` | `GET` | `/api/douyin-xingtu/get-kol-daily-fans/v1` | Follower Growth Trend |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `acceptCache` | `query` | n/a | all | `boolean` | Enable cache |
| `endDate` | `query` | all | n/a | `string` | End Date (yyyy-MM-dd) |
| `kolId` | `query` | all | n/a | `string` | KOL ID |
| `startDate` | `query` | all | n/a | `string` | Start Date (yyyy-MM-dd) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getKolDailyFansV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getKolDailyFansV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getKolDailyFansV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"kolId":"<kolId>","startDate":"<startDate>","endDate":"<endDate>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_daily_fans&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_daily_fans&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getKolDailyFansV1` on `/api/douyin-xingtu/get-kol-daily-fans/v1`.
- Echo the required lookup scope (`endDate`, `kolId`, and `startDate`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) follower Growth Trend data, including historical audience changes over time, for creator evaluation, campaign planning, and marketplace research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
