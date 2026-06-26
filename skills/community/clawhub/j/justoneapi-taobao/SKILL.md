---
name: Taobao and Tmall API
description: Analyze Taobao and Tmall workflows with JustOneAPI, including product Details, product Reviews, and shop Product List across 10 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_taobao"}}
---

# Taobao and Tmall

This skill wraps 10 Taobao and Tmall operations exposed by JustOneAPI. It is strongest for product Details, product Reviews, shop Product List, and product Search. Expect common inputs such as `itemId`, `page`, `sort`, `userId`, `shopId`.

## When To Use It

- The user needs product Details or product Reviews on Taobao and Tmall.
- The task lines up with shop Product List rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `itemId`, `page`, `sort`, `userId`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `getTaobaoItemDetailV1`: Product Details — Get Taobao and Tmall product Details data, including pricing, images, and shop details, for product research, catalog monitoring, and ecommerce analysis
- `getItemCommentV3`: Product Reviews — Get Taobao and Tmall product Reviews data, including ratings, timestamps, and reviewer signals, for feedback analysis and product research
- `getTaobaoShopItemListV1`: Shop Product List — Get Taobao and Tmall shop Product List data, including item titles, prices, and images, for seller research and catalog tracking
- `searchItemListV1`: Product Search — Get Taobao and Tmall product Search data, including titles, prices, and images, for product discovery

## Request Pattern

- 10 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `itemId`, `page`, `sort`, `userId`, `shopId`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getTaobaoItemDetailV1`, `getItemCommentV3`, `getTaobaoShopItemListV1`, `searchItemListV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_taobao&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Taobao and Tmall task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `getTaobaoItemDetailV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `itemId`, `page`, `sort`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
