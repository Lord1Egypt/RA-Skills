---
name: Douyin E-commerce API
description: Analyze Douyin E-commerce workflows with JustOneAPI, including item Details.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_ec"}}
---

# Douyin E-commerce

This skill wraps 1 Douyin E-commerce operations exposed by JustOneAPI. It is strongest for item Details. Expect common inputs such as `itemId`.

## When To Use It

- The user needs item Details on Douyin E-commerce.
- The user can provide identifiers or filters such as `itemId`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `getDouyinEcItemDetailV1`: Item Details — Get Douyin E-commerce item details, including price, title, and stock, for product monitoring and competitive analysis

## Request Pattern

- 1 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `itemId`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getDouyinEcItemDetailV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_ec&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_ec&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Douyin E-commerce task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `getDouyinEcItemDetailV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `itemId`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
