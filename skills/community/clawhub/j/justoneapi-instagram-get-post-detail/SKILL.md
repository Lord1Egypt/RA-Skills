---
name: Instagram Post Details API
description: Call GET /api/instagram/get-post-detail/v1 for Instagram Post Details through JustOneAPI with code.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_instagram_get_post_detail"}}
---

# Instagram Post Details

Use this focused JustOneAPI skill for post Details in Instagram. It targets `GET /api/instagram/get-post-detail/v1`. Required non-token inputs are `code`. OpenAPI describes it as: Get Instagram post Details data, including post caption, media content (images/videos), and publish time, for analyzing engagement metrics (likes/comments) for a specific post and archiving post content and media assets for content analysis.

## Endpoint Scope

- Platform key: `instagram`
- Endpoint key: `get-post-detail`
- Platform family: Instagram
- Skill slug: `justoneapi-instagram-get-post-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getInstagramPostDetailV1` | `v1` | `GET` | `/api/instagram/get-post-detail/v1` | Post Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `code` | `query` | all | n/a | `string` | The unique shortcode (slug) for the Instagram post (e.g., 'DRhvwVLAHAG') |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getInstagramPostDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getInstagramPostDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getInstagramPostDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"code":"<code>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_post_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_post_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getInstagramPostDetailV1` on `/api/instagram/get-post-detail/v1`.
- Echo the required lookup scope (`code`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Instagram post Details data, including post caption, media content (images/videos), and publish time, for analyzing engagement metrics (likes/comments) for a specific post and archiving post content and media assets for content analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
