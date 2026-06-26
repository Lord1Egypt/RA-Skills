---
name: Kuaishou API
description: Analyze Kuaishou workflows with JustOneAPI, including user Search, user Published Videos, and video Details across 7 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_kuaishou"}}
---

# Kuaishou

This skill wraps 7 Kuaishou operations exposed by JustOneAPI. It is strongest for user Search, user Published Videos, video Details, and video Search. Expect common inputs such as `keyword`, `page`, `pcursor`, `userId`, `videoId`.

## When To Use It

- The user needs user Search or user Published Videos on Kuaishou.
- The task lines up with video Details rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `keyword`, `page`, `pcursor`, `userId`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `searchKuaishouUserV2`: User Search — Get Kuaishou user Search data, including profile names, avatars, and follower counts, for creator discovery and account research
- `getKuaishouUserVideoListV2`: User Published Videos — Get Kuaishou user Published Videos data, including covers, publish times, and engagement metrics, for creator monitoring and content performance analysis
- `getVideoDetailsV2`: Video Details — Get Kuaishou video Details data, including video URL, caption, and author info, for in-depth content performance analysis and building databases of viral videos
- `searchKuaishouVideoV2`: Video Search — Get Kuaishou video Search data, including video ID, cover image, and description, for competitive analysis and market trends and keywords monitoring and brand tracking

## Request Pattern

- 7 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `keyword`, `page`, `pcursor`, `userId`, `videoId`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `searchKuaishouUserV2`, `getKuaishouUserVideoListV2`, `getVideoDetailsV2`, `searchKuaishouVideoV2`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_kuaishou&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Kuaishou task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `searchKuaishouUserV2`, explain why the returned fields answer the user's question.
- If the user gave filters such as `keyword`, `page`, `pcursor`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
