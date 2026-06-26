---
name: Xiaohongshu Creator Marketplace (Pugongying) API
description: Analyze Xiaohongshu Creator Marketplace (Pugongying) workflows with JustOneAPI, including creator Profile, data Summary, and follower Growth History across 24 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_xiaohongshu_pgy"}}
---

# Xiaohongshu Creator Marketplace (Pugongying)

This skill wraps 24 Xiaohongshu Creator Marketplace (Pugongying) operations exposed by JustOneAPI. It is strongest for creator Profile, data Summary, follower Growth History, and follower Summary. Expect common inputs such as `userId`, `acceptCache`, `kolId`, `business`, `dateType`.

## When To Use It

- The user needs creator Profile or data Summary on Xiaohongshu Creator Marketplace (Pugongying).
- The task lines up with follower Growth History rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `userId`, `acceptCache`, `kolId`, `business`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `apiSolarCooperatorUserBloggerUserIdV1`: Creator Profile — Get Xiaohongshu Creator Marketplace (Pugongying) creator Profile data, including audience and pricing data, for influencer vetting, benchmark analysis, and campaign planning
- `apiSolarKolDataV3DataSummaryV1`: Data Summary — Get Xiaohongshu Creator Marketplace (Pugongying) Summary data, including activity, engagement, and audience growth, for creator evaluation, campaign planning, and creator benchmarking
- `apiSolarKolDataUserIdFansOverallNewHistoryV1`: Follower Growth History — Get Xiaohongshu Creator Marketplace (Pugongying) follower Growth History data, including historical points, trend signals, and growth metrics, for trend tracking, audience analysis, and creator performance monitoring
- `apiSolarKolDataV3FansSummaryV1`: Follower Summary — Get Xiaohongshu Creator Marketplace (Pugongying) follower Summary data, including growth and engagement metrics, for audience analysis and creator benchmarking

## Request Pattern

- 24 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `userId`, `acceptCache`, `kolId`, `business`, `dateType`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `apiSolarCooperatorUserBloggerUserIdV1`, `apiSolarKolDataV3DataSummaryV1`, `apiSolarKolDataUserIdFansOverallNewHistoryV1`, `apiSolarKolDataV3FansSummaryV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_xiaohongshu_pgy&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Xiaohongshu Creator Marketplace (Pugongying) task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `apiSolarCooperatorUserBloggerUserIdV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `userId`, `acceptCache`, `kolId`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
