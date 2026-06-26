---
name: Bilibili API
description: Analyze Bilibili workflows with JustOneAPI, including video Details, user Published Videos, and user Profile across 9 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_bilibili"}}
---

# Bilibili

This skill wraps 9 Bilibili operations exposed by JustOneAPI. It is strongest for video Details, user Published Videos, user Profile, and video Danmaku. Expect common inputs such as `aid`, `bvid`, `cid`, `page`, `uid`.

## When To Use It

- The user needs video Details or user Published Videos on Bilibili.
- The task lines up with user Profile rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `aid`, `bvid`, `cid`, `page`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `getBilibiliVideoDetailV2`: Video Details — Get Bilibili video Details data, including metadata (title, tags, and publishing time), for tracking video performance and engagement metrics and analyzing content metadata and uploader information
- `getBilibiliUserVideoListV2`: User Published Videos — Get Bilibili user Published Videos data, including titles, covers, and publish times, for creator monitoring and content performance analysis
- `getUserDetailV2`: User Profile — Get Bilibili user Profile data, including account metadata, audience metrics, and verification-related fields, for analyzing creator's profile, level, and verification status and verifying user identity and social presence on bilibili
- `getVideoDanmuV2`: Video Danmaku — Get Bilibili video Danmaku data, including timeline positions and comment text, for audience reaction analysis and subtitle-style comment review

## Request Pattern

- 9 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `aid`, `bvid`, `cid`, `page`, `uid`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getBilibiliVideoDetailV2`, `getBilibiliUserVideoListV2`, `getUserDetailV2`, `getVideoDanmuV2`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_bilibili&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Bilibili task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `getBilibiliVideoDetailV2`, explain why the returned fields answer the user's question.
- If the user gave filters such as `aid`, `bvid`, `cid`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
