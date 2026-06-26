---
name: Twitter User Profile API
description: Call GET /api/twitter/get-user-detail/v1 for Twitter User Profile through JustOneAPI with restId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_twitter_get_user_detail"}}
---

# Twitter User Profile

Use this focused JustOneAPI skill for user Profile in Twitter. It targets `GET /api/twitter/get-user-detail/v1`. Required non-token inputs are `restId`. OpenAPI describes it as: Get Twitter user Profile data, including account metadata, audience metrics, and verification-related fields, for accessing user profile metadata (e.g., description, location, verification status) and collecting follower and following counts.

## Endpoint Scope

- Platform key: `twitter`
- Endpoint key: `get-user-detail`
- Platform family: Twitter
- Skill slug: `justoneapi-twitter-get-user-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getTwitterUserDetailV1` | `v1` | `GET` | `/api/twitter/get-user-detail/v1` | User Profile |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `restId` | `query` | all | n/a | `string` | The unique numeric identifier (Rest ID) for the X user |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getTwitterUserDetailV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getTwitterUserDetailV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getTwitterUserDetailV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"restId":"<restId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter_get_user_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter_get_user_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getTwitterUserDetailV1` on `/api/twitter/get-user-detail/v1`.
- Echo the required lookup scope (`restId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Twitter user Profile data, including account metadata, audience metrics, and verification-related fields, for accessing user profile metadata (e.g., description, location, verification status) and collecting follower and following counts.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
