---
name: Bilibili User Relation Stats API
description: Call GET /api/bilibili/get-user-relation-stat/v1 for Bilibili User Relation Stats through JustOneAPI with wmid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_bilibili_get_user_relation_stat"}}
---

# Bilibili User Relation Stats

Use this focused JustOneAPI skill for user Relation Stats in Bilibili. It targets `GET /api/bilibili/get-user-relation-stat/v1`. Required non-token inputs are `wmid`. OpenAPI describes it as: Get Bilibili user Relation Stats data, including following counts, for creator benchmarking and audience growth tracking.

## Endpoint Scope

- Platform key: `bilibili`
- Endpoint key: `get-user-relation-stat`
- Platform family: Bilibili
- Skill slug: `justoneapi-bilibili-get-user-relation-stat`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getUserRelationStat` | `v1` | `GET` | `/api/bilibili/get-user-relation-stat/v1` | User Relation Stats |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `wmid` | `query` | all | n/a | `string` | Bilibili User ID (WMID) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getUserRelationStat` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getUserRelationStat`.

```bash
node {baseDir}/bin/run.mjs --operation "getUserRelationStat" --token "$JUST_ONE_API_TOKEN" --params-json '{"wmid":"<wmid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_relation_stat&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_user_relation_stat&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getUserRelationStat` on `/api/bilibili/get-user-relation-stat/v1`.
- Echo the required lookup scope (`wmid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Bilibili user Relation Stats data, including following counts, for creator benchmarking and audience growth tracking.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
