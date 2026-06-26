---
name: Reddit Post Details API
description: Call GET /api/reddit/get-post-detail/v1 for Reddit Post Details through JustOneAPI with postId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_reddit_get_post_detail"}}
---

# Reddit Post Details

Use this focused JustOneAPI skill for post Details in Reddit. It targets `GET /api/reddit/get-post-detail/v1`. Required non-token inputs are `postId`. OpenAPI describes it as: Get Reddit post Details data, including author details, subreddit info, and engagement counts, for content analysis, moderation research, and monitoring.

## Endpoint Scope

- Platform key: `reddit`
- Endpoint key: `get-post-detail`
- Platform family: Reddit
- Skill slug: `justoneapi-reddit-get-post-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getRedditPostDetailV1` | `v1` | `GET` | `/api/reddit/get-post-detail/v1` | Post Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `postId` | `query` | all | n/a | `string` | The unique identifier of the Reddit post (e.g., 't3_1q4aqti') |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getRedditPostDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getRedditPostDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getRedditPostDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"postId":"<postId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_get_post_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_reddit_get_post_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getRedditPostDetailV1` on `/api/reddit/get-post-detail/v1`.
- Echo the required lookup scope (`postId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Reddit post Details data, including author details, subreddit info, and engagement counts, for content analysis, moderation research, and monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
