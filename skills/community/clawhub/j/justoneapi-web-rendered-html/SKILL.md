---
name: Web Page Rendered HTML Content API
description: Call GET /api/web/rendered-html/v1 for Web Page Rendered HTML Content through JustOneAPI with url.
author: JustOneAPI
homepage: https://api.justoneapi.com
metadata: {"openclaw":{"homepage":"https://api.justoneapi.com","primaryEnv":"JUST_ONE_API_TOKEN","requires":{"bins":["node"],"env":["JUST_ONE_API_TOKEN"]},"skillKey":"justoneapi_web_rendered_html"}}
---

# Web Page Rendered HTML Content

Use this focused JustOneAPI skill for rendered HTML Content in Web Page. It targets `GET /api/web/rendered-html/v1`. Required non-token inputs are `url`. OpenAPI describes it as: Get the Rendered HTML content of a web page.

## Endpoint Scope

- Platform key: `web`
- Endpoint key: `rendered-html`
- Platform family: Web Page
- Skill slug: `justoneapi-web-rendered-html`

| Operation | Version | Method | Path | OpenAPI summary |
| --- | --- | --- | --- | --- |
| `renderedHtmlV1` | `v1` | `GET` | `/api/web/rendered-html/v1` | Rendered HTML Content |

## Inputs

| Parameter | In | Required by | Optional by | Type | Notes |
| --- | --- | --- | --- | --- | --- |
| `url` | `query` | all | n/a | `string` | The URL of the web page to fetch |

Request body: none documented; send parameters through path or query arguments.

## Version Choice

Use `renderedHtmlV1` for the documented `v1` endpoint. There are no alternate versions grouped in this skill.

## Run This Endpoint

Supported operation IDs in this skill: `renderedHtmlV1`.

```bash
node {baseDir}/bin/run.mjs --operation "renderedHtmlV1" --token "$JUST_ONE_API_TOKEN" --params-json '{"url":"<url>"}'
```

Ask for any missing required parameter before calling the helper. Keep user-provided IDs, cursors, keywords, and filters unchanged.

## Environment

- Required: `JUST_ONE_API_TOKEN`
- Pass the token with `--token "$JUST_ONE_API_TOKEN"`; do not paste token values into chat messages, screenshots, or logs.
- Get a token from [Just One API Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_rendered_html&utm_content=project_link).
- Authentication details: [Just One API Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_web_rendered_html&utm_content=project_link).

## Output Focus

- State the operation ID and endpoint path used, for example `renderedHtmlV1` on `/api/web/rendered-html/v1`.
- Echo the required lookup scope (`url`) before summarizing results.
- Prioritize fields that support this endpoint purpose: Get the Rendered HTML content of a web page.
- Return raw JSON only after the short, endpoint-specific summary.
- If the backend errors, include the backend payload and the exact operation ID.
