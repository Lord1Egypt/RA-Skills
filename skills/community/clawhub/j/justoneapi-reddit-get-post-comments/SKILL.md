---
name: Reddit Post Comments API
description: Call GET /api/reddit/get-post-comments/v1 for Reddit Post Comments through JustOneAPI with postId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_reddit_get_post_comments"}}
---

# Reddit Post Comments

Use this focused JustOneAPI skill for post Comments in Reddit. It targets `GET /api/reddit/get-post-comments/v1`. Required non-token inputs are `postId`. OpenAPI describes it as: Get Reddit post Comments data, including text, authors, and timestamps, for discussion analysis and moderation research.

## Endpoint Scope

- Platform key: `reddit`
- Endpoint key: `get-post-comments`
- Platform family: Reddit
- Skill slug: `justoneapi-reddit-get-post-comments`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getRedditPostCommentsV1` | `v1` | `GET` | `/api/reddit/get-post-comments/v1` | Post Comments |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `cursor` | `query` | n/a | all | `string` | Pagination token for the next page of results |
| `postId` | `query` | all | n/a | `string` | The unique identifier of the Reddit post |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getRedditPostCommentsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getRedditPostCommentsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getRedditPostCommentsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"postId":"<postId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_get_post_comments&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_get_post_comments&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getRedditPostCommentsV1` on `/api/reddit/get-post-comments/v1`.
- Echo the required lookup scope (`postId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Reddit post Comments data, including text, authors, and timestamps, for discussion analysis and moderation research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
