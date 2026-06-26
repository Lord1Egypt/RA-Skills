---
name: Douyin (TikTok China) API
description: Analyze Douyin (TikTok China) workflows with JustOneAPI, including user Profile, user Published Videos, and video Details across 8 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin"}}
---

# Douyin (TikTok China)

This skill wraps 8 Douyin (TikTok China) operations exposed by JustOneAPI. It is strongest for user Profile, user Published Videos, video Details, and video Search. Expect common inputs such as `page`, `keyword`, `secUid`, `awemeId`, `commentId`.

## When To Use It

- The user needs user Profile or user Published Videos on Douyin (TikTok China).
- The task lines up with video Details rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `page`, `keyword`, `secUid`, `awemeId`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `getUserDetailV3`: User Profile — Get Douyin (TikTok China) user Profile data, including follower counts, verification status, and bio details, for creator research and account analysis
- `getUserVideoListV3`: User Published Videos — Get Douyin (TikTok China) user Published Videos data, including captions, covers, and publish times, for account monitoring
- `getDouyinVideoDetailV2`: Video Details — Get Douyin (TikTok China) video Details data, including author details, publish time, and engagement counts, for video research, archiving, and performance analysis
- `searchVideoV4`: Video Search — Get Douyin (TikTok China) video Search data, including metadata and engagement signals, for content discovery, trend research, and competitive monitoring

## Request Pattern

- 8 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `page`, `keyword`, `secUid`, `awemeId`, `commentId`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getUserDetailV3`, `getUserVideoListV3`, `getDouyinVideoDetailV2`, `searchVideoV4`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Douyin (TikTok China) task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `getUserDetailV3`, explain why the returned fields answer the user's question.
- If the user gave filters such as `page`, `keyword`, `secUid`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
