---
name: Web Crawling Html API
description: Call GET /api/v1/web/html for Web Crawling Html through Just Serp API with url.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_html&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_html&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_web_html"}}
---

# Web Crawling Html

Use this focused Just Serp API skill for Web Crawling Html. It targets `GET /api/v1/web/html`. Required inputs are `url`. OpenAPI describes it as: Get webpage crawl data, including returns full raw HTML content, fast and cost-efficient, and optimized for static page crawling, for scraping, metadata extraction, and page structure analysis.

## Endpoint Scope

- Group key: `web`
- Endpoint key: `html`
- Group family: Web Crawling
- Skill slug: `justserpapi-web-html`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `html` | `v1` | `GET` | `/api/v1/web/html` | Crawl Webpage (HTML) |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `url` | `query` | all | n/a | `string` | The full URL of the webpage to crawl (e.g., 'https://www.example.com') |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `html` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `html`.

```bash
node {baseDir}/bin/run.mjs --operation "html" --api-key "$JUST_SERP_API_KEY" --params-json '{"url":"<url>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, URLs, keywords, and filters unchanged.

## Environment

- Required: `JUST_SERP_API_KEY`
- Pass the API key with `--api-key "$JUST_SERP_API_KEY"`; do not paste key values into chat messages, screenshots, or logs.
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_html&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web_html&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `html` on `/api/v1/web/html`.
- Echo the required lookup scope (`url`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get webpage crawl data, including returns full raw HTML content, fast and cost-efficient, and optimized for static page crawling, for scraping, metadata extraction, and page structure analysis.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
