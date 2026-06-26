---
name: YouTube API
description: Analyze YouTube workflows with JustOneAPI, including video Details and channel Videos.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_youtube"}}
---

# YouTube

This skill wraps 2 YouTube operations exposed by JustOneAPI. It is strongest for video Details and channel Videos. Expect common inputs such as `channelId`, `cursor`, `videoId`.

## When To Use It

- The user needs video Details or channel Videos on YouTube.
- The user can provide identifiers or filters such as `channelId`, `cursor`, `videoId`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `getYoutubeVideoDetailV1`: Video Details — Get YouTube video Details data, including its title, description, and view counts, for tracking video engagement and statistics, extracting video metadata for content analysis, and verifying video availability and status
- `getChannelVideosV1`: Channel Videos — Retrieve a list of videos from a specific YouTube channel, providing detailed insights into content performance and upload history

## Request Pattern

- 2 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `channelId`, `cursor`, `videoId`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getYoutubeVideoDetailV1`, `getChannelVideosV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_youtube&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the YouTube task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `getYoutubeVideoDetailV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `channelId`, `cursor`, `videoId`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
