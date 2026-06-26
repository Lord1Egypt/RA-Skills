---
name: Reddit Keyword Search API
description: Call GET /api/reddit/search/v1 for Reddit Keyword Search through JustOneAPI with keyword.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_reddit_search"}}
---

# Reddit Keyword Search

Use this focused JustOneAPI skill for keyword Search in Reddit. It targets `GET /api/reddit/search/v1`. Required non-token inputs are `keyword`. OpenAPI describes it as: Get Reddit keyword Search data, including titles, authors, and subreddit context, for topic discovery and monitoring.

## Endpoint Scope

- Platform key: `reddit`
- Endpoint key: `search`
- Platform family: Reddit
- Skill slug: `justoneapi-reddit-search`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchRedditV1` | `v1` | `GET` | `/api/reddit/search/v1` | Keyword Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `after` | `query` | n/a | all | `string` | Pagination token to retrieve the next set of results |
| `keyword` | `query` | all | n/a | `string` | Search query keywords |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchRedditV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchRedditV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchRedditV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"keyword":"<keyword>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_search&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_search&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchRedditV1` on `/api/reddit/search/v1`.
- Echo the required lookup scope (`keyword`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Reddit keyword Search data, including titles, authors, and subreddit context, for topic discovery and monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
