---
name: Beike API
description: Analyze Beike workflows with JustOneAPI, including resale Housing Details, resale Housing List, and community List.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_beike"}}
---

# Beike

This skill wraps 3 Beike operations exposed by JustOneAPI. It is strongest for resale Housing Details, resale Housing List, and community List. Expect common inputs such as `cityId`, `condition`, `houseCode`, `limitOffset`, `offset`.

## When To Use It

- The user needs resale Housing Details or resale Housing List on Beike.
- The task lines up with community List rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `cityId`, `condition`, `houseCode`, `limitOffset`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `ershoufangDetailV1`: Resale Housing Details — Get Beike resale Housing Details data, including - Pricing (total and unit price), Physical attributes (area, and layout, for displaying a full property profile to users and detailed price comparison between specific listings
- `getErshoufangListV1`: Resale Housing List — Get Beike resale Housing List data, including - Supports filtering by city/region, price range, and layout, for building search result pages for property portals and aggregating market data for regional housing trends
- `communityListV1`: Community List — Get Beike community List data, including - Community name and unique ID and Average listing price and historical price trends, for identifying popular residential areas in a city and comparing average housing prices across different communities

## Request Pattern

- 3 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `cityId`, `condition`, `houseCode`, `limitOffset`, `offset`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `ershoufangDetailV1`, `getErshoufangListV1`, `communityListV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_beike&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Beike task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `ershoufangDetailV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `cityId`, `condition`, `houseCode`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
