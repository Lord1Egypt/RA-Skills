---
name: Xiaohongshu Creator Marketplace (Pugongying) Similar Creators API
description: Call GET /api/xiaohongshu-pgy/api/solar/kol/get_similar_kol/v1 for Xiaohongshu Creator Marketplace (Pugongying) Similar Creators through JustOneAPI with userId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_pgy_api_solar_kol_get_similar_kol"}}
---

# Xiaohongshu Creator Marketplace (Pugongying) Similar Creators

Use this focused JustOneAPI skill for similar Creators in Xiaohongshu Creator Marketplace (Pugongying). It targets `GET /api/xiaohongshu-pgy/api/solar/kol/get_similar_kol/v1`. Required non-token inputs are `userId`. OpenAPI describes it as: Get Xiaohongshu Creator Marketplace (Pugongying) similar Creators data, including audience signals, for creator discovery, benchmarking, and shortlist building.

## Endpoint Scope

- Platform key: `xiaohongshu-pgy`
- Endpoint key: `api/solar/kol/get_similar_kol`
- Platform family: Xiaohongshu Creator Marketplace (Pugongying)
- Skill slug: `justoneapi-xiaohongshu-pgy-api-solar-kol-get-similar-kol`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `apiSolarKolGetSimilarKolV1` | `v1` | `GET` | `/api/xiaohongshu-pgy/api/solar/kol/get_similar_kol/v1` | Similar Creators |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `pageNum` | `query` | n/a | all | `integer` | Page number for results |
| `userId` | `query` | all | n/a | `string` | KOL's user ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `apiSolarKolGetSimilarKolV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `apiSolarKolGetSimilarKolV1`.

```bash
node {baseDir}/bin/run.mjs --operation "apiSolarKolGetSimilarKolV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"userId":"<userId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_get_similar_kol&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy_api_solar_kol_get_similar_kol&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `apiSolarKolGetSimilarKolV1` on `/api/xiaohongshu-pgy/api/solar/kol/get_similar_kol/v1`.
- Echo the required lookup scope (`userId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Xiaohongshu Creator Marketplace (Pugongying) similar Creators data, including audience signals, for creator discovery, benchmarking, and shortlist building.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
