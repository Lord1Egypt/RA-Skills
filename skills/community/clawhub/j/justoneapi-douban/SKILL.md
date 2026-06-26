---
name: Douban Movie API
description: Analyze Douban Movie workflows with JustOneAPI, including movie Reviews, review Details, and subject Details across 6 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douban"}}
---

# Douban Movie

This skill wraps 6 Douban Movie operations exposed by JustOneAPI. It is strongest for movie Reviews, review Details, subject Details, and comments. Expect common inputs such as `page`, `subjectId`, `sort`, `reviewId`.

## When To Use It

- The user needs movie Reviews or review Details on Douban Movie.
- The task lines up with subject Details rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `page`, `subjectId`, `sort`, `reviewId`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `getMovieReviewsV1`: Movie Reviews — Get Douban movie Reviews data, including review titles, ratings, and snippets, for audience sentiment analysis and review research
- `getMovieReviewDetailsV1`: Review Details — Get Douban movie Review Details data, including metadata, content fields, and engagement signals, for review archiving and detailed opinion analysis
- `getSubjectDetailV1`: Subject Details — Get Douban subject Details data, including title, rating, and cast, for title enrichment and catalog research
- `getMovieCommentsV1`: Comments — Get Douban movie Comments data, including ratings, snippets, and interaction counts, for quick sentiment sampling and review monitoring

## Request Pattern

- 6 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `page`, `subjectId`, `sort`, `reviewId`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getMovieReviewsV1`, `getMovieReviewDetailsV1`, `getSubjectDetailV1`, `getMovieCommentsV1`.
3. Pick the smallest matching operation instead of guessing.
4. Ask the user for any missing required parameter. Do not invent values.
5. Call the helper with:

```bash
node {baseDir}/bin/run.mjs --operation "<operation-id>" --token "$JUST_ONE_API_TOKEN" --params-json '{"key":"value"}'
```

## Environment

- Required: `JUST_ONE_API_TOKEN`
- This skill uses `JUST_ONE_API_TOKEN` only for authenticated Just One API requests.
- Keep `JUST_ONE_API_TOKEN` private. Do not paste it into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douban&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Douban Movie task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `getMovieReviewsV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `page`, `subjectId`, `sort`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
