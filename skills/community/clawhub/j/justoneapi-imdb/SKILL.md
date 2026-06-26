---
name: IMDb API
description: Analyze IMDb workflows with JustOneAPI, including release Expectation, extended Details, and top Cast and Crew across 19 operations.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_imdb"}}
---

# IMDb

This skill wraps 19 IMDb operations exposed by JustOneAPI. It is strongest for release Expectation, extended Details, top Cast and Crew, and base Info. Expect common inputs such as `languageCountry`, `id`, `acceptCache`, `category`, `limit`.

## When To Use It

- The user needs release Expectation or extended Details on IMDb.
- The task lines up with top Cast and Crew rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `languageCountry`, `id`, `acceptCache`, `category`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `titleReleaseExpectationQuery`: Release Expectation — Get IMDb title Release Expectation data, including production status, release dates, and anticipation signals, for release monitoring and title research
- `titleExtendedDetailsQuery`: Extended Details — Get IMDb title Extended Details data, including title info, images, and genres, for title enrichment and catalog research
- `titleTopCastAndCrew`: Top Cast and Crew — Get IMDb title Top Cast and Crew data, including names, roles, and profile references, for talent research and title enrichment
- `titleBaseQuery`: Base Info — Get IMDb title Base Info data, including title text, release year, and type, for catalog enrichment and title lookup workflows

## Request Pattern

- 19 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `languageCountry`, `id`, `acceptCache`, `category`, `limit`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `titleReleaseExpectationQuery`, `titleExtendedDetailsQuery`, `titleTopCastAndCrew`, `titleBaseQuery`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the IMDb task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `titleReleaseExpectationQuery`, explain why the returned fields answer the user's question.
- If the user gave filters such as `languageCountry`, `id`, `acceptCache`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
