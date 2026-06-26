---
name: TikTok Comment Replies API
description: Call GET /api/tiktok/get-post-sub-comment/v1 for TikTok Comment Replies through JustOneAPI with awemeId and commentId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_tiktok_get_post_sub_comment"}}
---

# TikTok Comment Replies

Use this focused JustOneAPI skill for comment Replies in TikTok. It targets `GET /api/tiktok/get-post-sub-comment/v1`. Required non-token inputs are `awemeId` and `commentId`. OpenAPI describes it as: Get TikTok comment Replies data, including reply ID, user information, and text content, for understanding detailed user interactions and threaded discussions and identifying influencers or active participants within a comment section.

## Endpoint Scope

- Platform key: `tiktok`
- Endpoint key: `get-post-sub-comment`
- Platform family: TikTok
- Skill slug: `justoneapi-tiktok-get-post-sub-comment`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getPostSubCommentV1` | `v1` | `GET` | `/api/tiktok/get-post-sub-comment/v1` | Comment Replies |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `awemeId` | `query` | all | n/a | `string` | The unique ID of the TikTok post |
| `commentId` | `query` | all | n/a | `string` | The unique ID of the comment to retrieve replies for |
| `cursor` | `query` | n/a | all | `string` | Pagination cursor. Start with '0' |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getPostSubCommentV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getPostSubCommentV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getPostSubCommentV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"awemeId":"<awemeId>","commentId":"<commentId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_sub_comment&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_sub_comment&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getPostSubCommentV1` on `/api/tiktok/get-post-sub-comment/v1`.
- Echo the required lookup scope (`awemeId` and `commentId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get TikTok comment Replies data, including reply ID, user information, and text content, for understanding detailed user interactions and threaded discussions and identifying influencers or active participants within a comment section.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
