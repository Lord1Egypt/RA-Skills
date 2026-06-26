---
name: Instagram Reels Search API
description: Call GET /api/instagram/search-reels/v1 for Instagram Reels Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_instagram_search_reels"}}
---

# Instagram Reels Search

Use this focused JustOneAPI skill for reels Search in Instagram. It targets `GET /api/instagram/search-reels/v1`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Instagram reels Search data, including post ID, caption, and author profile, for tracking trends and viral content via specific keywords or hashtags and discovering high-engagement reels within a particular niche.

## Endpoint Scope

- Platform key: `instagram`
- Endpoint key: `search-reels`
- Platform family: Instagram
- Skill slug: `justoneapi-instagram-search-reels`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchReelsV1` | `v1` | `GET` | `/api/instagram/search-reels/v1` | Reels Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `keyword` | `query` | all | n/a | `string` | The search keyword or hashtag to filter Reels |
| `paginationToken` | `query` | n/a | all | `string` | Token used for retrieving the next page of results |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchReelsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchReelsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchReelsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_search_reels&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_search_reels&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchReelsV1` on `/api/instagram/search-reels/v1`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Instagram reels Search data, including post ID, caption, and author profile, for tracking trends and viral content via specific keywords or hashtags and discovering high-engagement reels within a particular niche.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
