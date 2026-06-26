---
name: Facebook Get Profile ID API
description: Call GET /api/facebook/get-profile-id/v1 for Facebook Get Profile ID through JustOneAPI with url.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_facebook_get_profile_id"}}
---

# Facebook Get Profile ID

Use this focused JustOneAPI skill for get Profile ID in Facebook. It targets `GET /api/facebook/get-profile-id/v1`. Required non-token inputs are `url`. OpenAPI describes it as: Retrieve the unique Facebook profile ID from a given profile URL.

## Endpoint Scope

- Platform key: `facebook`
- Endpoint key: `get-profile-id`
- Platform family: Facebook
- Skill slug: `justoneapi-facebook-get-profile-id`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getProfileIdV1` | `v1` | `GET` | `/api/facebook/get-profile-id/v1` | Get Profile ID |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `url` | `query` | all | n/a | `string` | The path part of the Facebook profile URL. Do not include `https://www.facebook.com`. Example: `/people/To-Bite/pfbid021XLeDjjZjsoWse1H43VEgb3i1uCLTpBvXSvrnL2n118YPtMF5AZkBrZobhWWdHTHl/` |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getProfileIdV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getProfileIdV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getProfileIdV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"url":"<url>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_get_profile_id&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook_get_profile_id&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getProfileIdV1` on `/api/facebook/get-profile-id/v1`.
- Echo the required lookup scope (`url`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Retrieve the unique Facebook profile ID from a given profile URL.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
