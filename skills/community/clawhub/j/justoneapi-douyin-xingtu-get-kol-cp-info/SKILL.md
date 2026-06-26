---
name: Douyin Creator Marketplace (Xingtu) Cost Performance Analysis API
description: Call GET /api/douyin-xingtu/get-kol-cp-info/v1 for Douyin Creator Marketplace (Xingtu) Cost Performance Analysis through JustOneAPI with kolId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_get_kol_cp_info"}}
---

# Douyin Creator Marketplace (Xingtu) Cost Performance Analysis

Use this focused JustOneAPI skill for cost Performance Analysis in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/get-kol-cp-info/v1`. Required non-token inputs are `kolId`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) cost Performance Analysis data, including pricing, exposure, and engagement efficiency indicators, for creator evaluation, campaign planning, and marketplace research.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `get-kol-cp-info`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-get-kol-cp-info`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getKolCpInfoV1` | `v1` | `GET` | `/api/douyin-xingtu/get-kol-cp-info/v1` | Cost Performance Analysis |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `acceptCache` | `query` | n/a | all | `boolean` | Enable cache |
| `kolId` | `query` | all | n/a | `string` | KOL ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getKolCpInfoV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getKolCpInfoV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getKolCpInfoV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"kolId":"<kolId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_cp_info&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_get_kol_cp_info&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getKolCpInfoV1` on `/api/douyin-xingtu/get-kol-cp-info/v1`.
- Echo the required lookup scope (`kolId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) cost Performance Analysis data, including pricing, exposure, and engagement efficiency indicators, for creator evaluation, campaign planning, and marketplace research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
