---
name: WeChat Official Accounts API
description: Analyze WeChat Official Accounts workflows with JustOneAPI, including user Published Posts, article Engagement Metrics, and article Comments across 5 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weixin"}}
---

# WeChat Official Accounts

This skill wraps 5 WeChat Official Accounts operations exposed by JustOneAPI. It is strongest for user Published Posts, article Engagement Metrics, article Comments, and keyword Search. Expect common inputs such as `articleUrl`, `keyword`, `offset`, `searchType`, `sortType`.

## When To Use It

- The user needs user Published Posts or article Engagement Metrics on WeChat Official Accounts.
- The task lines up with article Comments rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `articleUrl`, `keyword`, `offset`, `searchType`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `getUserPost`: User Published Posts — Get WeChat Official Accounts user Published Posts data, including titles, publish times, and summaries, for account monitoring
- `getArticleFeedback`: Article Engagement Metrics — Get WeChat Official Accounts article Engagement Metrics data, including like, share, and comment metrics, for article performance tracking and benchmarking
- `getArticleComment`: Article Comments — Get WeChat Official Accounts article Comments data, including commenter details, comment text, and timestamps, for feedback analysis
- `searchWeixinV1`: Keyword Search — Get WeChat Official Accounts keyword Search data, including account names, titles, and publish times, for content discovery

## Request Pattern

- 5 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `articleUrl`, `keyword`, `offset`, `searchType`, `sortType`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getUserPost`, `getArticleFeedback`, `getArticleComment`, `searchWeixinV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weixin&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the WeChat Official Accounts task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `getUserPost`, explain why the returned fields answer the user's question.
- If the user gave filters such as `articleUrl`, `keyword`, `offset`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
