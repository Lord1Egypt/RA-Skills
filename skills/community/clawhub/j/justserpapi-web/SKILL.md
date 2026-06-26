---
name: Web Crawling API
description: Fetch raw HTML, rendered HTML, or clean Markdown from public webpages through Just Serp API.
author: Just Serp API
homepage: https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web&utm_content=project_link
metadata: {"openclaw":{"homepage":"https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web&utm_content=project_link","primaryEnv":"JUST_SERP_API_KEY","requires":{"bins":["node"],"env":["JUST_SERP_API_KEY"]},"skillKey":"justserpapi_web"}}
---

# Web Crawling

Use this skill when the user needs webpage retrieval rather than a search engine result. It fits crawling, scraping preparation, readable content extraction, and page structure inspection for a known URL.

## When To Use It

- The user already has a target webpage URL and wants its raw HTML, rendered HTML, or cleaned Markdown.
- The task is about content extraction, page inspection, scrape preparation, or converting a page into LLM-friendly text.
- The user can provide a direct `url` to crawl.
- The user needs page content from the source URL itself, not Google search results about that URL.

## Representative Operations

- `html`: Crawl Webpage (HTML) — Retrieve the raw HTML response for a page.
- `renderedHtml`: Crawl Webpage (Rendered HTML) — Retrieve DOM output after rendering for JavaScript-heavy pages.
- `markdown`: Crawl Webpage (Markdown) — Extract the main readable content as clean Markdown for summarization or downstream processing.

## Request Pattern

- 3 read-only `GET` operations are available in this skill.
- All operations require a direct `url` query parameter.
- No operation in this skill requires a request body.
- Choose `renderedHtml` for dynamic pages, `html` for raw source, and `markdown` for readable content extraction.

## How To Work

1. Read `generated/operations.md` before choosing an endpoint.
2. Start with one of these operations when it matches the user's request: `html`, `renderedHtml`, `markdown`.
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
- Project site: [Just Serp API](https://justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web&utm_content=project_link).
- Authentication details: [Just Serp API Docs](https://docs.justserpapi.com/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justserpapi_web&utm_content=project_link).

## Output Rules

- Start with what was fetched: raw HTML, rendered HTML, or cleaned Markdown.
- Echo the target URL so the crawl scope is explicit.
- For `markdown`, surface the extracted readable content or key sections before raw JSON.
- For HTML-oriented requests, mention whether the user asked for source HTML or rendered output.
- If the backend errors, include the backend payload and the exact operation ID.
