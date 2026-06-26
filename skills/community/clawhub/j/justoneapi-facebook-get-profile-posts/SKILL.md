---
name: Facebook Get Profile Posts API
description: Call GET /api/facebook/get-profile-posts/v1 for Facebook Get Profile Posts through JustOneAPI with profileId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_facebook_get_profile_posts"}}
---

# Facebook Get Profile Posts

Use this focused JustOneAPI skill for get Profile Posts in Facebook. It targets `GET /api/facebook/get-profile-posts/v1`. Required non-token inputs are `profileId`. OpenAPI describes it as: Get public posts from a specific Facebook profile using its profile ID.

## Endpoint Scope

- Platform key: `facebook`
- Endpoint key: `get-profile-posts`
- Platform family: Facebook
- Skill slug: `justoneapi-facebook-get-profile-posts`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getProfilePostsV1` | `v1` | `GET` | `/api/facebook/get-profile-posts/v1` | Get Profile Posts |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `cursor` | `query` | n/a | all | `string` | Pagination cursor for fetching the next set of results |
| `profileId` | `query` | all | n/a | `string` | The unique Facebook profile ID |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getProfilePostsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getProfilePostsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getProfilePostsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"profileId":"<profileId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_get_profile_posts&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_get_profile_posts&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getProfilePostsV1` on `/api/facebook/get-profile-posts/v1`.
- Echo the required lookup scope (`profileId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get public posts from a specific Facebook profile using its profile ID.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
