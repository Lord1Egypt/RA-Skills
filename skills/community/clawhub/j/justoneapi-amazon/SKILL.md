---
name: Amazon API
description: Analyze Amazon workflows with JustOneAPI, including product Details, product Top Reviews, and best Sellers across 4 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_amazon"}}
---

# Amazon

This skill wraps 4 Amazon operations exposed by JustOneAPI. It is strongest for product Details, product Top Reviews, best Sellers, and products By Category. Expect common inputs such as `country`, `asin`, `page`, `category`, `categoryId`.

## When To Use It

- The user needs product Details or product Top Reviews on Amazon.
- The task lines up with best Sellers rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `country`, `asin`, `page`, `category`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `getAmazonProductDetailV1`: Product Details — Get Amazon product Details data, including title, brand, and price, for building product catalogs and enriching item content (e.g., images), price monitoring and availability tracking, and e-commerce analytics and competitor tracking
- `getProductTopReviewsV1`: Product Top Reviews — Get Amazon product Top Reviews data, including most helpful) public reviews, for sentiment analysis and consumer feedback tracking, product research and quality assessment, and monitoring competitor customer experience
- `getBestSellersV1`: Best Sellers — Get Amazon best Sellers data, including rank positions, product metadata, and pricing, for identifying trending products in specific categories, market share analysis and category research, and tracking sales rank and popularity over time
- `getProductsByCategoryV1`: Products By Category — Get Amazon products By Category data, including title, price, and rating, for category-based product discovery and returns product information such as title, price, and rating

## Request Pattern

- 4 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `country`, `asin`, `page`, `category`, `categoryId`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `getAmazonProductDetailV1`, `getProductTopReviewsV1`, `getBestSellersV1`, `getProductsByCategoryV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_amazon&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Amazon task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `getAmazonProductDetailV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `country`, `asin`, `page`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
