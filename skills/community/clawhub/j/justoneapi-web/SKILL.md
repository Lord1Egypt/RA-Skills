---
name: Web Page API
description: Analyze Web Page workflows with JustOneAPI, including hTML Content, rendered HTML Content, and markdown Content.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_web"}}
---

# Web Page

This skill wraps 3 Web Page operations exposed by JustOneAPI. It is strongest for hTML Content, rendered HTML Content, and markdown Content. Expect common inputs such as `url`.

## When To Use It

- The user needs hTML Content or rendered HTML Content on Web Page.
- The task lines up with markdown Content rather than a generic cross-platform workflow.
- The user can provide identifiers or filters such as `url`.
- The user wants an exact API-backed answer instead of a freeform summary.

## Representative Operations

- `htmlV1`: HTML Content — Get the HTML content of a web page
- `renderedHtmlV1`: Rendered HTML Content — Get the Rendered HTML content of a web page
- `markdownV1`: Markdown Content — Get the Markdown content of a web page

## Request Pattern

- 3 operations are available in this skill.
- HTTP methods used here: `GET`.
- The most common non-token parameters are `url`.
- All operations in this skill are parameter-driven requests; none require a request body.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `htmlV1`, `renderedHtmlV1`, `markdownV1`.
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
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web&utm_content=project_link).

## Output Rules

- Start with a plain-language answer tied to the Web Page task the user asked for.
- Include the most decision-relevant fields from the selected endpoint before dumping raw JSON.
- When using `htmlV1`, explain why the returned fields answer the user's question.
- If the user gave filters such as `url`, echo those back so the scope is explicit.
- If the backend errors, include the backend payload and the exact operation ID.
