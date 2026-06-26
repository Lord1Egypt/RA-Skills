---
name: Instagram Hashtag Posts Search API
description: Call GET /api/instagram/search-hashtag-posts/v1 for Instagram Hashtag Posts Search through JustOneAPI with hashtag.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_instagram_search_hashtag_posts"}}
---

# Instagram Hashtag Posts Search

Use this focused JustOneAPI skill for hashtag Posts Search in Instagram. It targets `GET /api/instagram/search-hashtag-posts/v1`. Required non-token inputs are `hashtag`. OpenAPI describes it as: Get Instagram hashtag Posts Search data, including caption, author profile, and publish time, for competitive analysis of trending topics and hashtags and monitoring community discussions and public opinion on specific tags.

## Endpoint Scope

- Platform key: `instagram`
- Endpoint key: `search-hashtag-posts`
- Platform family: Instagram
- Skill slug: `justoneapi-instagram-search-hashtag-posts`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `searchHashtagPostsV1` | `v1` | `GET` | `/api/instagram/search-hashtag-posts/v1` | Hashtag Posts Search |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `endCursor` | `query` | n/a | all | `string` | Cursor used for retrieving the next page of results |
| `hashtag` | `query` | all | n/a | `string` | The hashtag or keyword to search for |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `searchHashtagPostsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `searchHashtagPostsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "searchHashtagPostsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"hashtag":"<hashtag>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_search_hashtag_posts&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram_search_hashtag_posts&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `searchHashtagPostsV1` on `/api/instagram/search-hashtag-posts/v1`.
- Echo the required lookup scope (`hashtag`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Instagram hashtag Posts Search data, including caption, author profile, and publish time, for competitive analysis of trending topics and hashtags and monitoring community discussions and public opinion on specific tags.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
