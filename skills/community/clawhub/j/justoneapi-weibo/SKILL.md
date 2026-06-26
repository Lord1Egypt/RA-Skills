---
name: Weibo API
description: Track Weibo hot search boards, keyword results, creator profiles, fan or follower graphs, and post or video detail endpoints through JustOneAPI.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_weibo"}}
---

# Weibo

Use this skill for newsroom-style trend checks, creator due diligence, comment digging, and Weibo account monitoring. It is strongest when the user cares about hot search rankings, time-window keyword search, account activity timelines, and audience graph lookups.

## When To Use It

- The user wants Weibo hot search rankings, topic discovery, or time-window keyword monitoring.
- The task is about a specific Weibo account, post, comment thread, follower graph, or TV video page.
- The user can provide Weibo identifiers such as `uid`, `id`, `mid`, or search filters such as `q`, `startDay`, and `endDay`.
- The user needs primary-source Weibo data for monitoring, archiving, creator research, or campaign analysis.

## Representative Operations

- `hotSearchV1`: Hot Search — Pull the current Weibo hot search board for trend desks, breaking-news watchlists, and topic scouting.
- `searchAllV2`: Keyword Search — Search Weibo posts inside a time window using `q`, `startDay`, `startHour`, `endDay`, and `endHour`.
- `getUserPublishedPostsV1`: User Published Posts — Review a creator's latest posts and timeline activity.
- `getFollowersV1`: User Followers — Inspect the outward social graph of a Weibo account for creator and network research.

## Request Pattern

- 10 read-only `GET` operations are available in this skill.
- Common filters are `uid`, `q`, `page`, `startDay`, `endDay`, `mid`, and `id`.
- Several operations are identifier lookups for accounts or posts; others are monitoring queries over a time window.
- No operation in this skill requires a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `hotSearchV1`, `searchAllV2`, `getUserPublishedPostsV1`, `getFollowersV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_weibo&utm_content=project_link).

## Output Rules

- Lead with the concrete Weibo finding: trend, account signal, post detail, or audience graph.
- For hot search or keyword search requests, restate the search window and filters before listing results.
- For account-level requests, surface verification, follower and fan counts, and the most relevant recent posts first.
- For post or video detail requests, pull out engagement counts, media references, and author context before raw JSON.
- If the backend errors, include the backend payload and the exact operation ID.
