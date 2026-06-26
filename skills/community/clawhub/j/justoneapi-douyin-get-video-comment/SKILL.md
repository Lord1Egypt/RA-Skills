---
name: Douyin (TikTok China) Video Comments API
description: Call GET /api/douyin/get-video-comment/v1 for Douyin (TikTok China) Video Comments through JustOneAPI with awemeId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_get_video_comment"}}
---

# Douyin (TikTok China) Video Comments

Use this focused JustOneAPI skill for video Comments in Douyin (TikTok China). It targets `GET /api/douyin/get-video-comment/v1`. Required non-token inputs are `awemeId`. OpenAPI describes it as: Get Douyin (TikTok China) video Comments data, including authors, text, and likes, for sentiment analysis and engagement review.

## Endpoint Scope

- Platform key: `douyin`
- Endpoint key: `get-video-comment`
- Platform family: Douyin (TikTok China)
- Skill slug: `justoneapi-douyin-get-video-comment`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getVideoCommentV1` | `v1` | `GET` | `/api/douyin/get-video-comment/v1` | Video Comments |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `awemeId` | `query` | all | n/a | `string` | The unique video identifier (aweme_id) |
| `page` | `query` | n/a | all | `integer` | Page number (starting from 1) |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getVideoCommentV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getVideoCommentV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getVideoCommentV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"awemeId":"<awemeId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_comment&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_get_video_comment&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getVideoCommentV1` on `/api/douyin/get-video-comment/v1`.
- Echo the required lookup scope (`awemeId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douyin (TikTok China) video Comments data, including authors, text, and likes, for sentiment analysis and engagement review.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
