---
name: Douban Movie Comments API
description: Call GET /api/douban/get-movie-comments/v1 for Douban Movie Comments through JustOneAPI with subjectId.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douban_get_movie_comments"}}
---

# Douban Movie Comments

Use this focused JustOneAPI skill for comments in Douban Movie. It targets `GET /api/douban/get-movie-comments/v1`. Required non-token inputs are `subjectId`. OpenAPI describes it as: Get Douban movie Comments data, including ratings, snippets, and interaction counts, for quick sentiment sampling and review monitoring.

## Endpoint Scope

- Platform key: `douban`
- Endpoint key: `get-movie-comments`
- Platform family: Douban Movie
- Skill slug: `justoneapi-douban-get-movie-comments`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `getMovieCommentsV1` | `v1` | `GET` | `/api/douban/get-movie-comments/v1` | Comments |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `page` | `query` | n/a | all | `integer` | Page number for pagination |
| `sort` | `query` | n/a | all | `string` | Sort order for the result set. Available Values: - `time`: Time - `new_score`: New Score |
| `sort` enum | values | n/a | n/a | n/a | `new_score`, `time` |
| `subjectId` | `query` | all | n/a | `string` | The unique ID for a movie or TV subject on Douban |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `getMovieCommentsV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `getMovieCommentsV1`.

```bash
node {baseDir}/bin/run.mjs --operation "getMovieCommentsV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"subjectId":"<subjectId>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_comments&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban_get_movie_comments&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `getMovieCommentsV1` on `/api/douban/get-movie-comments/v1`.
- Echo the required lookup scope (`subjectId`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get Douban movie Comments data, including ratings, snippets, and interaction counts, for quick sentiment sampling and review monitoring.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
