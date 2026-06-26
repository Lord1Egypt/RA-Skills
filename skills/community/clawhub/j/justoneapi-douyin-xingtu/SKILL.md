---
name: Douyin Creator Marketplace (Xingtu) API
description: Analyze Douyin Creator Marketplace (Xingtu) workflows with JustOneAPI, including creator Profile, creator Link Structure, and creator Visibility Status across 46 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_douyin_xingtu"}}
---

# Douyin Creator Marketplace (Xingtu)

This skill wraps 46 Douyin Creator Marketplace (Xingtu) operations exposed by JustOneAPI. It is strongest for creator Profile, creator Link Structure, creator Visibility Status, and creator Channel Metrics. Expect common inputs such as `oAuthorId`, `acceptCache`, `kolId`, `platform`, `range`.

## When To Use It

- The user needs creator Profile or creator Link Structure on Douyin Creator Marketplace (Xingtu).
- The task lines up with creator Visibility Status rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `oAuthorId`, `acceptCache`, `kolId`, `platform`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `gwApiAuthorGetAuthorBaseInfoV1`: Creator Profile — Get Douyin Creator Marketplace (Xingtu) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning
- `gwApiDataSpAuthorLinkStructV1`: Creator Link Structure — Get Douyin Creator Marketplace (Xingtu) creator Link Structure data, including engagement and conversion metrics, for creator performance analysis
- `gwApiDataSpCheckAuthorDisplayV1`: Creator Visibility Status — Get Douyin Creator Marketplace (Xingtu) creator Visibility Status data, including availability status, discovery eligibility, and campaign display signals, for creator evaluation, campaign planning, and marketplace research
- `gwApiAuthorGetAuthorPlatformChannelInfoV2V1`: Creator Channel Metrics — Get Douyin Creator Marketplace (Xingtu) creator Channel Metrics data, including platform distribution and channel performance data used, for creator evaluation

## Request Pattern

- 46 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `oAuthorId`, `acceptCache`, `kolId`, `platform`, `range`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `gwApiAuthorGetAuthorBaseInfoV1`, `gwApiDataSpAuthorLinkStructV1`, `gwApiDataSpCheckAuthorDisplayV1`, `gwApiAuthorGetAuthorPlatformChannelInfoV2V1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_douyin_xingtu&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Douyin Creator Marketplace (Xingtu) task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `gwApiAuthorGetAuthorBaseInfoV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `oAuthorId`, `acceptCache`, `kolId`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
