---
name: TikTok Post Details API
description: Call GET /api/tiktok/get-post-detail/v1 for TikTok Post Details through JustOneAPI with postId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_tiktok_get_post_detail"}}
---

# TikTok Post Details

Use this focused JustOneAPI skill for post Details in TikTok. It targets `GET /api/tiktok/get-post-detail/v1`. Required non-token inputs are `postId`. OpenAPI describes it as: Get TikTok post Details data, including video ID, author information, and description text, for content performance analysis and metadata extraction and influencer evaluation via specific post metrics.

## Endpoint Scope

- Platform key: `tiktok`
- Endpoint key: `get-post-detail`
- Platform family: TikTok
- Skill slug: `justoneapi-tiktok-get-post-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getTiktokPostDetailV1` | `v1` | `GET` | `/api/tiktok/get-post-detail/v1` | Post Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `postId` | `query` | all | n/a | `string` | The unique ID of the TikTok post |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getTiktokPostDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getTiktokPostDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getTiktokPostDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"postId":"<postId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_get_post_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getTiktokPostDetailV1` on `/api/tiktok/get-post-detail/v1`.
- Echo the required lookup scope (`postId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get TikTok post Details data, including video ID, author information, and description text, for content performance analysis and metadata extraction and influencer evaluation via specific post metrics.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
