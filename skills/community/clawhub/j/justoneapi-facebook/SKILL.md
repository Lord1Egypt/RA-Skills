---
name: Facebook API
description: Analyze Facebook workflows with JustOneAPI, including post Search, get Profile ID, and get Profile Posts.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_facebook"}}
---

# Facebook

This skill wraps 3 Facebook operations exposed by JustOneAPI. It is strongest for post Search, get Profile ID, and get Profile Posts. Expect common inputs such as `cursor`, `endDate`, `keyword`, `profileId`, `startDate`.

## When To Use It

- The user needs post Search or get Profile ID on Facebook.
- The task lines up with get Profile Posts rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `cursor`, `endDate`, `keyword`, `profileId`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `searchFacebookPostsV1`: Post Search — Get Facebook post Search data, including matched results, metadata, and ranking signals, for discovering relevant public posts for specific keywords and analyzing engagement and reach of public content on facebook
- `getProfileIdV1`: Get Profile ID — Retrieve the unique Facebook profile ID from a given profile URL
- `getProfilePostsV1`: Get Profile Posts — Get public posts from a specific Facebook profile using its profile ID

## Request Pattern

- 3 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `cursor`, `endDate`, `keyword`, `profileId`, `startDate`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `searchFacebookPostsV1`, `getProfileIdV1`, `getProfilePostsV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_facebook&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Facebook task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `searchFacebookPostsV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `cursor`, `endDate`, `keyword`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
