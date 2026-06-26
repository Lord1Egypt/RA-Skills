---
name: Facebook Post Search API
description: Call GET /api/facebook/search-post/v1 for Facebook Post Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_facebook_search_post"}}
---

# Facebook Post Search

Use this focused JustOneAPI skill for post Search in Facebook. It targets `GET /api/facebook/search-post/v1`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Facebook post Search data, including matched results, metadata, and ranking signals, for discovering relevant public posts for specific keywords and analyzing engagement and reach of public content on facebook.

## Endpoint Scope

- Platform key: `facebook`
- Endpoint key: `search-post`
- Platform family: Facebook
- Skill slug: `justoneapi-facebook-search-post`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchFacebookPostsV1` | `v1` | `GET` | `/api/facebook/search-post/v1` | Post Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `cursor` | `query` | n/a | all | `string` | Pagination cursor for fetching the next set of results |
| `endDate` | `query` | n/a | all | `string` | End date for the search range (inclusive), formatted as yyyy-MM-dd |
| `keyword` | `query` | all | n/a | `string` | Keyword to search for in public posts. Supports basic text matching |
| `startDate` | `query` | n/a | all | `string` | Start date for the search range (inclusive), formatted as yyyy-MM-dd |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchFacebookPostsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchFacebookPostsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchFacebookPostsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_search_post&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_search_post&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchFacebookPostsV1` on `/api/facebook/search-post/v1`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Facebook post Search data, including matched results, metadata, and ranking signals, for discovering relevant public posts for specific keywords and analyzing engagement and reach of public content on facebook.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
