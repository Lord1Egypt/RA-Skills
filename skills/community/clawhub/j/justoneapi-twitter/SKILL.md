---
name: Twitter API
description: Analyze Twitter workflows with JustOneAPI, including user Profile and user Published Posts.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_twitter"}}
---

# Twitter

This skill wraps 2 Twitter operations exposed by JustOneAPI. It is strongest for user Profile and user Published Posts. Expect common inputs such as `restId`, `cursor`.

## When To Use It

- The user needs user Profile or user Published Posts on Twitter.
- The user can provide identifiers or filters such as `restId`, `cursor`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `getTwitterUserDetailV1`: User Profile — Get Twitter user Profile data, including account metadata, audience metrics, and verification-related fields, for accessing user profile metadata (e.g., description, location, verification status) and collecting follower and following counts
- `getTwitterUserPostsV1`: User Published Posts — Get Twitter user Published Posts data, including post content, timestamps, and engagement data, for account monitoring and content analysis

## Request Pattern

- 2 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `restId`, `cursor`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getTwitterUserDetailV1`, `getTwitterUserPostsV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_twitter&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Twitter task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `getTwitterUserDetailV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `restId`, `cursor`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
