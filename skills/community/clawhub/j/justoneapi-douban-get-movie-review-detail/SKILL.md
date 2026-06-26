---
name: Douban Movie Review Details API
description: Call GET /api/douban/get-movie-review-detail/v1 for Douban Movie Review Details through JustOneAPI with reviewId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douban_get_movie_review_detail"}}
---

# Douban Movie Review Details

Use this focused JustOneAPI skill for review Details in Douban Movie. It targets `GET /api/douban/get-movie-review-detail/v1`. Required non-token inputs are `reviewId`. OpenAPI describes it as: Get Douban movie Review Details data, including metadata, content fields, and engagement signals, for review archiving and detailed opinion analysis.

## Endpoint Scope

- Platform key: `douban`
- Endpoint key: `get-movie-review-detail`
- Platform family: Douban Movie
- Skill slug: `justoneapi-douban-get-movie-review-detail`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getMovieReviewDetailsV1` | `v1` | `GET` | `/api/douban/get-movie-review-detail/v1` | Review Details |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `reviewId` | `query` | all | n/a | `string` | The unique ID for a specific review on Douban |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getMovieReviewDetailsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getMovieReviewDetailsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getMovieReviewDetailsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"reviewId":"<reviewId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_review_detail&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_review_detail&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getMovieReviewDetailsV1` on `/api/douban/get-movie-review-detail/v1`.
- Echo the required lookup scope (`reviewId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douban movie Review Details data, including metadata, content fields, and engagement signals, for review archiving and detailed opinion analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
