---
name: YOUKU API
description: Analyze YOUKU workflows with JustOneAPI, including video Search, video Details, and user Profile.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_youku"}}
---

# YOUKU

This skill wraps 3 YOUKU operations exposed by JustOneAPI. It is strongest for video Search, video Details, and user Profile. Expect common inputs such as `keyword`, `page`, `uid`, `videoId`.

## When To Use It

- The user needs video Search or video Details on YOUKU.
- The task lines up with user Profile rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `keyword`, `page`, `uid`, `videoId`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `searchVideoV1`: Video Search — Get YOUKU video Search data, including video ID, title, and cover image, for keyword-based video discovery, monitoring specific topics or trends on youku, and analyzing search results for market research
- `getYoukuVideoDetailV1`: Video Details — Get YOUKU video Details data, including video ID, title, and description, for fetching comprehensive metadata for a single video, tracking engagement metrics like play counts and likes, and integrating detailed video info into third-party dashboards
- `getYoukuUserDetailV1`: User Profile — Get YOUKU user Profile data, including user ID, username, and avatar, for analyzing creator influence and audience size, monitoring account growth and verification status, and fetching basic user info for social crm

## Request Pattern

- 3 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `keyword`, `page`, `uid`, `videoId`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `searchVideoV1`, `getYoukuVideoDetailV1`, `getYoukuUserDetailV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youku&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the YOUKU task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `searchVideoV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `keyword`, `page`, `uid`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
