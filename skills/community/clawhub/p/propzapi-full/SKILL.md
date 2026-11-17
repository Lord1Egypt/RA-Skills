---
name: propzapi-full
version: 0.2.0
description: Generate images from HTML/CSS templates and capture webpage screenshots via propzapi.com. Render OG images, social cards, certificates, invoices and charts by filling {{variables}} in a template, snapshot any live URL, and manage your template library — one JSON call, no headless browser to run.
license: MIT-0
author: propzapi
homepage: https://propzapi.com
repository: https://github.com/paperandbeyond23-gif/propzapi-skills
tags:
  - propzapi
  - image-generation
  - image-api
  - og-image
  - social-image
  - screenshot
  - html-to-image
  - templates
  - api
  - mcp
metadata:
  openclaw:
    primaryEnv: PROPZAPI_KEY
    homepage: https://propzapi.com
    requires:
      env:
        - PROPZAPI_KEY
---

# propzapi-full

Generate images from templates and capture webpage screenshots via [propzapi.com](https://propzapi.com). Use when the user wants to **produce an image programmatically** — an Open Graph / social share card, a certificate, an invoice, a receipt, a data chart, a banner — or a screenshot of a live page, rather than a hand-drawn or AI-diffused picture.

Templates are HTML/CSS with `{{variables}}` and Jinja logic (`{% if %}`, `{% for %}`, filters). Fill the variables with one JSON call and get back a rendered PNG/JPEG/WEBP/PDF at a stable URL — no headless browser to run, no fonts to install.

## When to use this skill

Each render spends 1 propzapi credit (image generation and screenshots), so this skill activates when the request is genuinely about producing an image or capturing a page — not when an image merely comes up in passing.

**DO use when the user:**

- Wants an image built from a template + data (OG image, social card, certificate, invoice, chart) → `generate_image`
- Wants a screenshot / snapshot of a live URL → `screenshot`
- Asks what templates are available → `list_templates`
- Wants to define a new reusable template from HTML/CSS → `create_template`
- Needs a signed render URL to drop straight into a `<meta og:image>` tag → `embed_url`

**Do NOT use when:**

- The user wants a photo-realistic or artistic image conjured from a text prompt — that's a diffusion model, not a template renderer
- The user only wants to talk about a design without producing a file

When intent is ambiguous, confirm whether they want a template render or a page screenshot before calling.

## Tools

### `generate_image` — render an image from a template
Fill a template's `{{variables}}` and render to an image. Args: `template` (a `tpl_...` id or a built-in template name), `modifications` (dict of variable → value fills), `format` (`png` | `jpeg` | `webp` | `pdf`, default `png`), `scale` (multiplier, e.g. `2`), `quality` (1–100 for jpeg/webp). Costs 1 credit, billed on delivery. Returns `{url, width, height, format, bytes}`.

### `screenshot` — snapshot a live webpage
Capture any URL as an image. Args: `url` (required), `full_page` (bool), `width`, `height`, `format` (`png` | `jpeg` | `webp` | `pdf`, default `png`). Costs 1 credit. Returns `{url, ...}`.

### `list_templates` — available templates
The built-in and custom templates you can render (includes 13 built-ins, with data charts — bar/line/donut). No args. Free. Returns `{count, data:[{template, name, width, height, variables}]}`.

### `create_template` — define a reusable template
Register your own HTML/CSS template. Args: `name`, `html`, `width`, `height`, `variables` (list). Free. Returns the created template with its `tpl_...` id.

### `embed_url` — signed render URL for `<meta og:image>`
Sign a GET render URL so a template renders on request straight from a page's `<head>`. Args: `template`, `modifications`, `format`. Free to sign.

## Authentication

Set `PROPZAPI_KEY` to your propzapi key. It's sent as the `X-API-Key` header — the base URL is hardcoded, so the key never reaches any other host.

```bash
export PROPZAPI_KEY="your_key"
```

Get a free key (50-image trial, no card required) at <https://propzapi.com/app>. You can also mint one with `POST /v1/register` → `{api_key, plan, credits}`.

## Pricing

Each rendered image or screenshot costs 1 credit — the response returns the exact charge in the `X-Credits-Cost` header, and your balance in `X-Credits-Remaining`. Listing and creating templates is free.

| Plan | Price | Images / mo |
|---|---|---|
| Free trial | $0 | 50 |
| Starter | $29/mo | 1,000 |
| Growth | $79/mo | 3,500 |
| Pro | $199/mo | 12,000 |

Prefer pay-as-you-go? Credit packs: **$5 / 150 images** and **$15 / 500 images**. Manage plans at <https://propzapi.com/pricing>.

## Errors

All functions return a Python dict. On success it's the API response; on failure it has an `error` key:

- `{"error": "auth_required", ...}` — `PROPZAPI_KEY` not set (includes `signup_url`)
- `{"error": "auth_invalid", ...}` — key rejected; mint a new one at `/app`
- `{"error": "out_of_credits", ...}` — image credits exhausted; includes `upgrade_url`
- `{"error": "not_found", ...}` — no match for that template id
- `{"error": "rate_limit_exceeded", ...}` — plan request limit or too many free keys from this IP
- `{"error": "upstream_unavailable", ...}` — the render backend was briefly unreachable; retry
- `{"error": "invalid_argument", ...}` — missing `template`/`url` or a bad `format` value
- `{"error": "network" | "HTTP <code>" | "unexpected", ...}` — transport / other failures

## API reference

- Docs: <https://propzapi.com/docs>
- OpenAPI spec: <https://api.propzapi.com/openapi.json>
- MCP server: <https://api.propzapi.com/mcp> — tools `generate_image`, `screenshot_url`, `list_templates`
- Pricing: <https://propzapi.com/pricing>

## Independence

propzapi is an independent developer tool for rendering images from templates and capturing webpage screenshots. Images render from HTML/CSS you supply or select; you are responsible for the content you render and for the rights to any assets, fonts, and pages you screenshot. Comply with the laws of your jurisdiction and the terms of any site you capture.
