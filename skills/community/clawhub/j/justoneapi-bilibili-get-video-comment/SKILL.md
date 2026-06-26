---
name: Bilibili Video Comments API
description: Call GET /api/bilibili/get-video-comment/v2 for Bilibili Video Comments through JustOneAPI with aid.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_bilibili_get_video_comment"}}
---

# Bilibili Video Comments

Use this focused JustOneAPI skill for video Comments in Bilibili. It targets `GET /api/bilibili/get-video-comment/v2`. Required non-token inputs are `aid`. OpenAPI describes it as: Get Bilibili video Comments data, including commenter profiles, text, and likes, for sentiment analysis and comment moderation workflows.

## Endpoint Scope

- Platform key: `bilibili`
- Endpoint key: `get-video-comment`
- Platform family: Bilibili
- Skill slug: `justoneapi-bilibili-get-video-comment`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getVideoCommentV2` | `v2` | `GET` | `/api/bilibili/get-video-comment/v2` | Video Comments |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `aid` | `query` | all | n/a | `string` | Bilibili Archive ID (AID) |
| `cursor` | `query` | n/a | all | `string` | Pagination cursor |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getVideoCommentV2` for the documented `v2` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getVideoCommentV2`.

```bash
node {baseDir}/bin/run.mjs --operation "getVideoCommentV2" --token "$JUST_ONE_API_TOKEN" --params-json '{"aid":"<aid>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_comment&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili_get_video_comment&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getVideoCommentV2` on `/api/bilibili/get-video-comment/v2`.
- Echo the required lookup scope (`aid`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Bilibili video Comments data, including commenter profiles, text, and likes, for sentiment analysis and comment moderation workflows.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
