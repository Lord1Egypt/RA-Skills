---
name: Douyin Creator Marketplace (Xingtu) KOL Keyword Search API
description: Call GET /api/douyin-xingtu/search-kol-simple/v1 for Douyin Creator Marketplace (Xingtu) KOL Keyword Search through JustOneAPI with keyword, page, and platformSource.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu_search_kol_simple"}}
---

# Douyin Creator Marketplace (Xingtu) KOL Keyword Search

Use this focused JustOneAPI skill for kOL Keyword Search in Douyin Creator Marketplace (Xingtu). It targets `GET /api/douyin-xingtu/search-kol-simple/v1`. Required non-token inputs are `keyword`, `page`, and `platformSource`. OpenAPI describes it as: Get Douyin Creator Marketplace (Xingtu) kOL Keyword Search data, including matching creators and discovery data, for creator sourcing and shortlist building.

## Endpoint Scope

- Platform key: `douyin-xingtu`
- Endpoint key: `search-kol-simple`
- Platform family: Douyin Creator Marketplace (Xingtu)
- Skill slug: `justoneapi-douyin-xingtu-search-kol-simple`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchKolSimpleV1` | `v1` | `GET` | `/api/douyin-xingtu/search-kol-simple/v1` | KOL Keyword Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `acceptCache` | `query` | n/a | all | `boolean` | Enable cache |
| `keyword` | `query` | all | n/a | `string` | Search keywords |
| `page` | `query` | all | n/a | `integer` | Page number |
| `platformSource` | `query` | all | n/a | `string` | Platform source. Available Values: - `_1`: Douyin - `_2`: Toutiao - `_3`: Xigua |
| `platformSource` enum | values | n/a | n/a | n/a | `_1`, `_2`, `_3` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchKolSimpleV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchKolSimpleV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchKolSimpleV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>","platformSource":"_1","page":1}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_search_kol_simple&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu_search_kol_simple&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchKolSimpleV1` on `/api/douyin-xingtu/search-kol-simple/v1`.
- Echo the required lookup scope (`keyword`, `page`, and `platformSource`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin Creator Marketplace (Xingtu) kOL Keyword Search data, including matching creators and discovery data, for creator sourcing and shortlist building.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
