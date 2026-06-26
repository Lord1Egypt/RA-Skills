---
name: Beike Community List API
description: Call GET /api/beike/community/list/v1 for Beike Community List through JustOneAPI with cityId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_beike_community_list"}}
---

# Beike Community List

Use this focused JustOneAPI skill for community List in Beike. It targets `GET /api/beike/community/list/v1`. Required non-token inputs are `cityId`. OpenAPI describes it as: Get Beike community List data, including - Community name and unique ID and Average listing price and historical price trends, for identifying popular residential areas in a city and comparing average housing prices across different communities.

## Endpoint Scope

- Platform key: `beike`
- Endpoint key: `community/list`
- Platform family: Beike
- Skill slug: `justoneapi-beike-community-list`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `communityListV1` | `v1` | `GET` | `/api/beike/community/list/v1` | Community List |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `cityId` | `query` | all | n/a | `string` | The ID of the city (e.g., '110000' for Beijing) |
| `condition` | `query` | n/a | all | `string` | Filter conditions for communities |
| `limitOffset` | `query` | n/a | all | `integer` | Pagination offset, starting from 0 (e.g., 0, 20, 40...) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `communityListV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `communityListV1`.

```bash
node {baseDir}/bin/run.mjs --operation "communityListV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"cityId":"<cityId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_community_list&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike_community_list&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `communityListV1` on `/api/beike/community/list/v1`.
- Echo the required lookup scope (`cityId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Beike community List data, including - Community name and unique ID and Average listing price and historical price trends, for identifying popular residential areas in a city and comparing average housing prices across different communities.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
