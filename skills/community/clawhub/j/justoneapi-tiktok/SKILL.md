---
name: TikTok API
description: Analyze TikTok workflows with JustOneAPI, including user Published Posts, post Details, and user Profile across 7 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_tiktok"}}
---

# TikTok

This skill wraps 7 TikTok operations exposed by JustOneAPI. It is strongest for user Published Posts, post Details, user Profile, and post Comments. Expect common inputs such as `cursor`, `awemeId`, `keyword`, `secUid`, `commentId`.

## When To Use It

- The user needs user Published Posts or post Details on TikTok.
- The task lines up with user Profile rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `cursor`, `awemeId`, `keyword`, `secUid`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `getUserPostV1`: User Published Posts — Get TikTok user Published Posts data, including video ID, description, and publish time, for user activity analysis and posting frequency tracking, influencer performance evaluation, and content trend monitoring for specific creators
- `getTiktokPostDetailV1`: Post Details — Get TikTok post Details data, including video ID, author information, and description text, for content performance analysis and metadata extraction and influencer evaluation via specific post metrics
- `getTiktokUserDetailV1`: User Profile — Get TikTok user Profile data, including nickname, unique ID, and avatar, for influencer profiling and audience analysis, account performance tracking and growth monitoring, and identifying verified status and official accounts
- `getPostCommentV1`: Post Comments — Get TikTok post Comments data, including comment ID, user information, and text content, for sentiment analysis of the audience's reaction to specific content and engagement measurement via comment volume and quality

## Request Pattern

- 7 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `cursor`, `awemeId`, `keyword`, `secUid`, `commentId`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getUserPostV1`, `getTiktokPostDetailV1`, `getTiktokUserDetailV1`, `getPostCommentV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the TikTok task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `getUserPostV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `cursor`, `awemeId`, `keyword`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
