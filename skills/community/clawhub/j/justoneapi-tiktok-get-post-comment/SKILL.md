---
name: TikTok Post Comments API
description: Call GET /api/tiktok/get-post-comment/v1 for TikTok Post Comments through JustOneAPI with awemeId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_tiktok_get_post_comment"}}
---

# TikTok Post Comments

Use this focused JustOneAPI skill for post Comments in TikTok. It targets `GET /api/tiktok/get-post-comment/v1`. Required non-token inputs are `awemeId`. OpenAPI describes it as: Get TikTok post Comments data, including comment ID, user information, and text content, for sentiment analysis of the audience's reaction to specific content and engagement measurement via comment volume and quality.

## Endpoint Scope

- Platform key: `tiktok`
- Endpoint key: `get-post-comment`
- Platform family: TikTok
- Skill slug: `justoneapi-tiktok-get-post-comment`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getPostCommentV1` | `v1` | `GET` | `/api/tiktok/get-post-comment/v1` | Post Comments |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `awemeId` | `query` | all | n/a | `string` | The unique ID of the TikTok post (awemeId) |
| `cursor` | `query` | n/a | all | `string` | Pagination cursor. Start with '0' |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getPostCommentV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getPostCommentV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getPostCommentV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"awemeId":"<awemeId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_comment&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_comment&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getPostCommentV1` on `/api/tiktok/get-post-comment/v1`.
- Echo the required lookup scope (`awemeId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get TikTok post Comments data, including comment ID, user information, and text content, for sentiment analysis of the audience's reaction to specific content and engagement measurement via comment volume and quality.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
