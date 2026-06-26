---
name: Twitter User Published Posts API
description: Call GET /api/twitter/get-user-posts/v1 for Twitter User Published Posts through JustOneAPI with restId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_twitter_get_user_posts"}}
---

# Twitter User Published Posts

Use this focused JustOneAPI skill for user Published Posts in Twitter. It targets `GET /api/twitter/get-user-posts/v1`. Required non-token inputs are `restId`. OpenAPI describes it as: Get Twitter user Published Posts data, including post content, timestamps, and engagement data, for account monitoring and content analysis.

## Endpoint Scope

- Platform key: `twitter`
- Endpoint key: `get-user-posts`
- Platform family: Twitter
- Skill slug: `justoneapi-twitter-get-user-posts`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getTwitterUserPostsV1` | `v1` | `GET` | `/api/twitter/get-user-posts/v1` | User Published Posts |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `cursor` | `query` | n/a | all | `string` | Pagination cursor for navigating through long timelines |
| `restId` | `query` | all | n/a | `string` | The unique numeric identifier (Rest ID) for the X user |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getTwitterUserPostsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getTwitterUserPostsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getTwitterUserPostsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"restId":"<restId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter_get_user_posts&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter_get_user_posts&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getTwitterUserPostsV1` on `/api/twitter/get-user-posts/v1`.
- Echo the required lookup scope (`restId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Twitter user Published Posts data, including post content, timestamps, and engagement data, for account monitoring and content analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
