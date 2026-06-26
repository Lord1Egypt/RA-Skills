---
name: Instagram User Published Posts API
description: Call GET /api/instagram/get-user-posts/v1 for Instagram User Published Posts through JustOneAPI with username.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_instagram_get_user_posts"}}
---

# Instagram User Published Posts

Use this focused JustOneAPI skill for user Published Posts in Instagram. It targets `GET /api/instagram/get-user-posts/v1`. Required non-token inputs are `username`. OpenAPI describes it as: Get Instagram user Published Posts data, including post code, caption, and media type, for monitoring recent publishing activity of a specific user and building a historical record of content for auditing or analysis.

## Endpoint Scope

- Platform key: `instagram`
- Endpoint key: `get-user-posts`
- Platform family: Instagram
- Skill slug: `justoneapi-instagram-get-user-posts`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getInstagramUserPostsV1` | `v1` | `GET` | `/api/instagram/get-user-posts/v1` | User Published Posts |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `paginationToken` | `query` | n/a | all | `string` | Token used for retrieving the next page of results |
| `username` | `query` | all | n/a | `string` | The Instagram username whose published posts are to be retrieved |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getInstagramUserPostsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getInstagramUserPostsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getInstagramUserPostsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"username":"<username>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_user_posts&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_user_posts&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getInstagramUserPostsV1` on `/api/instagram/get-user-posts/v1`.
- Echo the required lookup scope (`username`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Instagram user Published Posts data, including post code, caption, and media type, for monitoring recent publishing activity of a specific user and building a historical record of content for auditing or analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
