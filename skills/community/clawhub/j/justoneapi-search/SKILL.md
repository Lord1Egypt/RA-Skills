---
name: Social Media API
description: Analyze Social Media workflows with JustOneAPI, including cross-Platform Search.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_search"}}
---

# Social Media

This skill wraps 1 Social Media operations exposed by JustOneAPI. It is strongest for cross-Platform Search. Expect common inputs such as `end`, `keyword`, `nextCursor`, `source`, `start`.

## When To Use It

- The user needs cross-Platform Search on Social Media.
- The user can provide identifiers or filters such as `end`, `keyword`, `nextCursor`, `source`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `searchCrossPlatformV1`: Cross-Platform Search — Get cross-platform social media search data, including Xiaohongshu, Douyin, Kuaishou, WeChat, Bilibili, Weibo and Zhihu results, for trend research and monitoring

## Request Pattern

- 1 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `end`, `keyword`, `nextCursor`, `source`, `start`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `searchCrossPlatformV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_search&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_search&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Social Media task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `searchCrossPlatformV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `end`, `keyword`, `nextCursor`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
