---
name: Instagram API
description: Analyze Instagram workflows with JustOneAPI, including user Profile, post Details, and user Published Posts across 5 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_instagram"}}
---

# Instagram

This skill wraps 5 Instagram operations exposed by JustOneAPI. It is strongest for user Profile, post Details, user Published Posts, and reels Search. Expect common inputs such as `paginationToken`, `username`, `code`, `endCursor`, `hashtag`.

## When To Use It

- The user needs user Profile or post Details on Instagram.
- The task lines up with user Published Posts rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `paginationToken`, `username`, `code`, `endCursor`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `getInstagramUserDetailV1`: User Profile — Get Instagram user Profile data, including follower count, following count, and post count, for obtaining basic account metadata for influencer vetting, tracking follower growth and audience reach over time, and mapping user handles to specific profile stats
- `getInstagramPostDetailV1`: Post Details — Get Instagram post Details data, including post caption, media content (images/videos), and publish time, for analyzing engagement metrics (likes/comments) for a specific post and archiving post content and media assets for content analysis
- `getInstagramUserPostsV1`: User Published Posts — Get Instagram user Published Posts data, including post code, caption, and media type, for monitoring recent publishing activity of a specific user and building a historical record of content for auditing or analysis
- `searchReelsV1`: Reels Search — Get Instagram reels Search data, including post ID, caption, and author profile, for tracking trends and viral content via specific keywords or hashtags and discovering high-engagement reels within a particular niche

## Request Pattern

- 5 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `paginationToken`, `username`, `code`, `endCursor`, `hashtag`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getInstagramUserDetailV1`, `getInstagramPostDetailV1`, `getInstagramUserPostsV1`, `searchReelsV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_instagram&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Instagram task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `getInstagramUserDetailV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `paginationToken`, `username`, `code`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
