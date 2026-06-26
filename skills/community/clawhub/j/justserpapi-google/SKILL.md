---
name: Google Search API
description: Search Google web, news, maps, trends, shopping, scholar, finance, hotel, and media surfaces through Just Serp API.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_google"}}
---

# Google SERP

Use this skill for Google SERP research, search result collection, competitive intelligence, trend monitoring, local business lookups, and shopping or scholar analysis. It is the broad Google-facing skill for tasks that start from a keyword, a place, a domain, or a topic and need structured Google result data.

## When To Use It

- The user wants Google web search, news search, image search, video search, or mobile SERP output for a keyword.
- The task is about Google Maps, Local, Shopping, Trends, Scholar, Finance, Hotels, Lens, Jobs, or AI result surfaces.
- The user can provide filters such as `query`, `country`, `language`, `domain`, `page`, `geo`, or a Google Maps place identifier.
- The user needs API-backed Google result data for research, monitoring, ranking checks, or reporting instead of a freeform answer.

## Representative Operations

- `search`: Search SERP — Pull standard Google web results for keyword research and ranking checks.
- `mapsSearch`: Maps Search — Find Google Maps business results and local pack data for a query and location.
- `TrendsSearch`: Trends Search — Inspect time-series search interest and related trend signals.
- `ScholarSearch`: Scholar Search — Query academic search results and citation-oriented records.
- `shoppingSearch`: Shopping Search — Collect product listings, merchants, and pricing signals from Google Shopping.

## Request Pattern

- 31 read-only `GET` operations are available in this skill.
- Common inputs are `query`, `country`, `domain`, `language`, `geo`, `page`, `html`, and feature-specific identifiers.
- Most operations are query-only; none require a request body.
- Prefer the narrowest Google vertical that matches the task instead of using generic search for everything.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `search`, `mapsSearch`, `TrendsSearch`, `ScholarSearch`, `shoppingSearch`.
3. Pick the smallest matching operation instead of guessing.
4. Ask the user for any missing required parameter. Do not invent values.
5. Call the helper with:

```bash
node {baseDir}/bin/run.mjs --operation "<operation-id>" --api-key "$JUST_SERP_API_KEY" --params-json '{"key":"value"}'
```

## Environment

- Required: `JUST_SERP_API_KEY`
- This skill uses `JUST_SERP_API_KEY` only for authenticated Just Serp API requests.
- Keep `JUST_SERP_API_KEY` private. Do not paste it into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_google&utm_content=project_link).

## Output Rules

- Lead with the Google surface you used and the exact query or filters applied.
- For SERP-style responses, summarize the top result patterns before raw JSON.
- For Maps, Shopping, Scholar, or Trends requests, highlight the entity, metric, or ranking signals most relevant to the user's decision.
- If multiple Google verticals could answer the task, explain why the chosen endpoint was the best fit.
- If the backend errors, include the backend payload and the exact operation ID.
