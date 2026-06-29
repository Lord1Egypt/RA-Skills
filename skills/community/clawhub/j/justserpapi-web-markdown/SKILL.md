---
name: Web Crawling Markdown API
description: Call GET /api/v1/web/markdown for Web Crawling Markdown through Just Serp API with url.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_markdown&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_markdown&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_web_markdown"}}
---

# Web Crawling Markdown

Use this focused Just Serp API skill for Web Crawling Markdown. It targets `GET /api/v1/web/markdown`. Required inputs are `url`. OpenAPI describes it as: Get webpage crawl data, including removing boilerplate, for readable extraction, documentation workflows, and LLM input.

## Endpoint Scope

- Group key: `web`
- Endpoint key: `markdown`
- Group family: Web Crawling
- Skill slug: `justserpapi-web-markdown`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `markdown` | `v1` | `GET` | `/api/v1/web/markdown` | Crawl Webpage (Markdown) |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `url` | `query` | all | n/a | `string` | The full URL of the webpage to crawl and convert to Markdown (e.g., 'https://www.example.com') |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `markdown` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `markdown`.

```bash
node {baseDir}/bin/run.mjs --operation "markdown" --api-key "$JUST_SERP_API_KEY" --params-json '{"url":"<url>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_markdown&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_markdown&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `markdown` on `/api/v1/web/markdown`.
- Echo the required lookup scope (`url`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get webpage crawl data, including removing boilerplate, for readable extraction, documentation workflows, and LLM input.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
