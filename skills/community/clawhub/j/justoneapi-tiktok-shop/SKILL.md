---
name: TikTok Shop API
description: Analyze TikTok Shop workflows with JustOneAPI, including product Search and product Details.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_tiktok_shop"}}
---

# TikTok Shop

This skill wraps 2 TikTok Shop operations exposed by JustOneAPI. It is strongest for product Search and product Details. Expect common inputs such as `region`, `keyword`, `offset`, `pageToken`, `productId`.

## When To Use It

- The user needs product Search or product Details on TikTok Shop.
- The user can provide identifiers or filters such as `region`, `keyword`, `offset`, `pageToken`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `searchProductsV1`: Product Search — Get TikTok Shop product Search data, including title, price, and sales, for market research and trend analysis, competitor product discovery, and monitoring product popularity in specific regions
- `getTiktokShopProductDetailV1`: Product Details — Get TikTok Shop product Details data, including title, description, and price, for building product catalogs, price and stock monitoring, and in-depth product analysis

## Request Pattern

- 2 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `region`, `keyword`, `offset`, `pageToken`, `productId`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `searchProductsV1`, `getTiktokShopProductDetailV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_tiktok_shop&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the TikTok Shop task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `searchProductsV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `region`, `keyword`, `offset`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
