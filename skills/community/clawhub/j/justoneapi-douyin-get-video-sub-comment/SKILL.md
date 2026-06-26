---
name: Douyin (TikTok China) Comment Replies API
description: Call GET /api/douyin/get-video-sub-comment/v1 for Douyin (TikTok China) Comment Replies through JustOneAPI with commentId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_get_video_sub_comment"}}
---

# Douyin (TikTok China) Comment Replies

Use this focused JustOneAPI skill for comment Replies in Douyin (TikTok China). It targets `GET /api/douyin/get-video-sub-comment/v1`. Required non-token inputs are `commentId`. OpenAPI describes it as: Get Douyin (TikTok China) comment Replies data, including text, authors, and timestamps, for thread analysis and feedback research.

## Endpoint Scope

- Platform key: `douyin`
- Endpoint key: `get-video-sub-comment`
- Platform family: Douyin (TikTok China)
- Skill slug: `justoneapi-douyin-get-video-sub-comment`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getVideoSubCommentV1` | `v1` | `GET` | `/api/douyin/get-video-sub-comment/v1` | Comment Replies |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `commentId` | `query` | all | n/a | `string` | The unique identifier of the top-level comment |
| `page` | `query` | n/a | all | `integer` | Page number (starting from 1) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getVideoSubCommentV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getVideoSubCommentV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getVideoSubCommentV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"commentId":"<commentId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_sub_comment&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_sub_comment&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getVideoSubCommentV1` on `/api/douyin/get-video-sub-comment/v1`.
- Echo the required lookup scope (`commentId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin (TikTok China) comment Replies data, including text, authors, and timestamps, for thread analysis and feedback research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
