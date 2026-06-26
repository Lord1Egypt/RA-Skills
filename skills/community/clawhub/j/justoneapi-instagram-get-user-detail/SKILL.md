---
name: Instagram User Profile API
description: Call GET /api/instagram/get-user-detail/v1 for Instagram User Profile through JustOneAPI with username.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_instagram_get_user_detail"}}
---

# Instagram User Profile

Use this focused JustOneAPI skill for user Profile in Instagram. It targets `GET /api/instagram/get-user-detail/v1`. Required non-token inputs are `username`. OpenAPI describes it as: Get Instagram user Profile data, including follower count, following count, and post count, for obtaining basic account metadata for influencer vetting, tracking follower growth and audience reach over time, and mapping user handles to specific profile stats.

## Endpoint Scope

- Platform key: `instagram`
- Endpoint key: `get-user-detail`
- Platform family: Instagram
- Skill slug: `justoneapi-instagram-get-user-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getInstagramUserDetailV1` | `v1` | `GET` | `/api/instagram/get-user-detail/v1` | User Profile |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `username` | `query` | all | n/a | `string` | The Instagram username whose profile details are to be retrieved |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getInstagramUserDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getInstagramUserDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getInstagramUserDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"username":"<username>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_user_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_get_user_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getInstagramUserDetailV1` on `/api/instagram/get-user-detail/v1`.
- Echo the required lookup scope (`username`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Instagram user Profile data, including follower count, following count, and post count, for obtaining basic account metadata for influencer vetting, tracking follower growth and audience reach over time, and mapping user handles to specific profile stats.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
