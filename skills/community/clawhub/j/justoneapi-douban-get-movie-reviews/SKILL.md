---
name: Douban Movie Movie Reviews API
description: Call GET /api/douban/get-movie-reviews/v1 for Douban Movie Movie Reviews through JustOneAPI with subjectId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douban_get_movie_reviews"}}
---

# Douban Movie Movie Reviews

Use this focused JustOneAPI skill for movie Reviews in Douban Movie. It targets `GET /api/douban/get-movie-reviews/v1`. Required non-token inputs are `subjectId`. OpenAPI describes it as: Get Douban movie Reviews data, including review titles, ratings, and snippets, for audience sentiment analysis and review research.

## Endpoint Scope

- Platform key: `douban`
- Endpoint key: `get-movie-reviews`
- Platform family: Douban Movie
- Skill slug: `justoneapi-douban-get-movie-reviews`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getMovieReviewsV1` | `v1` | `GET` | `/api/douban/get-movie-reviews/v1` | Movie Reviews |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `page` | `query` | n/a | all | `integer` | Page number for pagination |
| `sort` | `query` | n/a | all | `string` | Sort order for the result set. Available Values: - `time`: Time - `hotest`: Hotest |
| `sort` enum | values | n/a | n/a | n/a | `hotest`, `time` |
| `subjectId` | `query` | all | n/a | `string` | The unique ID for a movie or TV subject on Douban |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getMovieReviewsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getMovieReviewsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getMovieReviewsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"subjectId":"<subjectId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_reviews&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_reviews&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getMovieReviewsV1` on `/api/douban/get-movie-reviews/v1`.
- Echo the required lookup scope (`subjectId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douban movie Reviews data, including review titles, ratings, and snippets, for audience sentiment analysis and review research.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
