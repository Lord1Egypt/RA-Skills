---
name: Toutiao API
description: Analyze Toutiao workflows with JustOneAPI, including article Details, user Profile, and app Keyword Search across 4 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_toutiao"}}
---

# Toutiao

This skill wraps 4 Toutiao operations exposed by JustOneAPI. It is strongest for article Details, user Profile, app Keyword Search, and web Keyword Search. Expect common inputs such as `keyword`, `id`, `page`, `searchId`, `userId`.

## When To Use It

- The user needs article Details or user Profile on Toutiao.
- The task lines up with app Keyword Search rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `keyword`, `id`, `page`, `searchId`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `getToutiaoArticleDetailV1`: Article Details — Get Toutiao article Details data, including article ID, title, and author information, for content performance analysis and media monitoring and verifying article authenticity and metadata retrieval
- `getToutiaoUserDetailV1`: User Profile — Get Toutiao user Profile data, including user ID, nickname, and avatar, for influencer profiling and audience analysis and monitoring creator performance and growth
- `searchToutiaoV1`: App Keyword Search — Get Toutiao app Keyword Search data, including matching articles, videos, and authors, for topic discovery and monitoring
- `searchV2`: Web Keyword Search — Get Toutiao web Keyword Search data, including this is the PC version of the search API. Note that it currently only supports retrieving the first page of results, for first-page discovery of articles, videos, and authors for trend research and monitoring

## Request Pattern

- 4 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `keyword`, `id`, `page`, `searchId`, `userId`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getToutiaoArticleDetailV1`, `getToutiaoUserDetailV1`, `searchToutiaoV1`, `searchV2`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_toutiao&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Toutiao task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `getToutiaoArticleDetailV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `keyword`, `id`, `page`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
