---
name: mrscraper
description: Read web pages as HTML or Markdown, take screenshots, extract brand data and JSON, search the web, and run AI scrapers through the MrScraper API
tags: [web-scraping, web-search, data-extraction, web-crawling, web-automation]

homepage: https://mrscraper.com/
vendor: MrScraper
support_email: support@mrscraper.com

required_env_vars: [MRSCRAPER_API_TOKEN]
primary_credential: MRSCRAPER_API_TOKEN

metadata: {"openclaw":{"requires":{"env":["MRSCRAPER_API_TOKEN"]},"primaryEnv":"MRSCRAPER_API_TOKEN"}}

network: {"allowed_hosts":["api.mrscraper.com","api.app.mrscraper.com"]}
---

# MrScraper

Read web pages as HTML or Markdown, take screenshots, extract brand data and JSON, search the web, and run AI scrapers through the MrScraper API

## Actions

This skill supports:

- Retrieving the raw HTML of public web pages, with optional browser rendering and a screenshot
- Retrieving pages as Markdown
- Capturing page screenshots
- Extracting a website's colors, typography, logos, and social links
- Extracting structured JSON from a page with a natural-language prompt
- Searching the web for ranked results
- Starting AI scraper runs from natural-language instructions
- Rerunning existing scraper configurations on one or multiple URLs
- Running manual workflow-based reruns
- Fetching paginated results and detailed results by ID

This skill is API-only and does not depend on bundled local scripts.

## Base URLs

- Scraper API (pages and web search): `https://api.mrscraper.com`
- Platform API: `https://api.app.mrscraper.com`

## Authentication

Use header-based auth on all endpoints:

```http
x-api-token: <MRSCRAPER_API_TOKEN>
accept: application/json
content-type: application/json
```

### How to get `MRSCRAPER_API_TOKEN`?

An API token lets your applications securely interact with MrScraper APIs and rerun scrapers created in the dashboard.

Follow these steps in the dashboard:

1. Click your **User Profile** at the top-right corner.
2. Select **API Tokens**.
3. Click **New Token**.
4. Enter a **name** and set an **expiration date**.
5. Click **Create**.
6. Copy the new token and store it securely as `MRSCRAPER_API_TOKEN`.
7. Use it in requests through the `x-api-token` header.

Security rule:

- Never expose tokens in client-side code (browser/mobile app bundles).
- Store tokens in environment variables or server-side secret managers.

Notes from the auth docs:

- The API key works for all V3 Platform endpoints.
- For access to endpoints on other hosts, contact `support@mrscraper.com`.

## Install and Runtime

- No local install step is required by this skill document.
- No bundled `scripts/` are required.
- Calls are direct HTTPS requests to the two base URLs above.

## Data and Scope

- Data is sent only to `api.app.mrscraper.com` and `api.mrscraper.com`.
- Responses may contain extracted page content and scrape metadata.
- This skill does not define hidden persistence or background jobs.
- Never expose tokens in logs, commits, or output.

## Endpoints

### 1. Scrape HTML (read a page)

- Method: `GET`
- URL: `https://api.mrscraper.com/`
- Auth: `x-api-token` header

Retrieve the raw HTML of a page. Browser rendering and a screenshot are optional. Send the inputs as URL-encoded query parameters. Leave out the optional ones you do not need; MrScraper's defaults then apply.

#### Query parameters:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `url` | `string` | Yes | URL of the page to scrape. Must include the protocol (https://). |
| `browserRendering` | `boolean` | No | Controls whether the page is loaded in a browser. Leave it out to load the page without a browser first and switch to a browser automatically if the request is blocked. Set true to always load the page in a browser, which JavaScript-heavy sites, SPAs, and pages that load content dynamically need. Set false to never use a browser. |
| `timeout` | `integer` | No | Maximum seconds to wait for the scrape before the request times out, from 1 to 330. Increase for slow or complex pages. Defaults to 300. |
| `warmStart` | `boolean` | No | Opens the site's home page first to warm the session before loading the target URL. Useful for sites that expect a normal browsing session before deeper pages. |
| `blockResources` | `boolean` | No | Blocks images, fonts, and stylesheets from loading. Speeds up scraping and reduces bandwidth usage. |
| `waitForSelector` | `string` | No | Waits until a specific CSS selector or text appears on the page before returning it, such as #results. Up to 500 characters. Useful for content that loads asynchronously after the initial page load. |
| `geoCode` | `string` | No | Two-letter country code to load the page from, such as us or gb. Defaults to the United States. |
| `maxAge` | `integer` | Yes | Serves a cached result of the same request when it is newer than this age, in milliseconds, such as 86400000 for 1 day. Up to 604800000 (7 days). 0, the default, always scrapes fresh. A cached result costs the same tokens as the original scrape. Send `0` unless the user accepts a cached result. |
| `maxRetries` | `integer` | No | Maximum number of retries for the request. Omit for no limit. |
| `screenshot` | `string` | No | Also captures a screenshot of the rendered page as a base64-encoded PNG: `full` captures the entire scroll height, `top` captures the first viewport, and `<width>x<height>` sets the viewport size in pixels with an optional `-<zoom>` percent, such as `1280x800` or `1920x1080-75`. Width and height range from 100 to 3840, zoom from 25 to 300. Setting it forces browser rendering. Leave it out for no screenshot. |
| `html` | `boolean` | Yes | Always `true`. |
| `markdown` | `boolean` | Yes | Always `false`. |
| `saveResult` | `boolean` | Yes | Always `true`, so the page is saved to your MrScraper results. |

#### Request examples:

```bash
curl --location 'https://api.mrscraper.com/?url=https%3A%2F%2Fwww.scrapethissite.com%2Fpages%2Fsimple%2F&maxAge=0&html=true&markdown=false&saveResult=true' \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>"
```

With browser rendering, a selector to wait for, a country, and a screenshot of the first viewport:

```bash
curl --location 'https://api.mrscraper.com/?url=https%3A%2F%2Fwww.scrapethissite.com%2Fpages%2Fsimple%2F&browserRendering=true&waitForSelector=.country&geoCode=gb&maxAge=0&screenshot=top&html=true&markdown=false&saveResult=true' \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>"
```

#### Response example:

```html
<!doctype html>
<html>
  <head>...</head>
  <body>...</body>
</html>
```

With `screenshot`, the response is JSON:

```json
{
  "html": "<!doctype html>...",
  "screenshot": "iVBORw0KGgo..."
}
```

#### Notes:

- Send booleans as `true` or `false` and country codes in lowercase.
- A request can take up to `timeout` (300 seconds when unset); allow 30 seconds more for the response.
- Use it for publicly accessible pages; it does not sign in to websites.

### 2. Scrape Markdown

- Method: `GET`
- URL: `https://api.mrscraper.com/`
- Auth: `x-api-token` header

Retrieve a page as Markdown. Browser rendering is optional. Send the inputs as URL-encoded query parameters. Leave out the optional ones you do not need; MrScraper's defaults then apply.

#### Query parameters:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `url` | `string` | Yes | URL of the page to scrape. Must include the protocol (https://). |
| `browserRendering` | `boolean` | No | Controls whether the page is loaded in a browser. Leave it out to load the page without a browser first and switch to a browser automatically if the request is blocked. Set true to always load the page in a browser, which JavaScript-heavy sites, SPAs, and pages that load content dynamically need. Set false to never use a browser. |
| `timeout` | `integer` | No | Maximum seconds to wait for the scrape before the request times out, from 1 to 330. Increase for slow or complex pages. Defaults to 300. |
| `geoCode` | `string` | No | Two-letter country code to load the page from, such as us or gb. Defaults to the United States. |
| `warmStart` | `boolean` | No | Opens the site's home page first to warm the session before loading the target URL. Useful for sites that expect a normal browsing session before deeper pages. |
| `blockResources` | `boolean` | No | Blocks images, fonts, and stylesheets from loading. Speeds up scraping and reduces bandwidth usage. |
| `waitForSelector` | `string` | No | Waits until a specific CSS selector or text appears on the page before returning it, such as #results. Up to 500 characters. Useful for content that loads asynchronously after the initial page load. |
| `maxAge` | `integer` | Yes | Serves a cached result of the same request when it is newer than this age, in milliseconds, such as 86400000 for 1 day. Up to 604800000 (7 days). 0, the default, always scrapes fresh. A cached result costs the same tokens as the original scrape. Send `0` unless the user accepts a cached result. |
| `maxRetries` | `integer` | No | Maximum number of retries for the request. Omit for no limit. |
| `markdown` | `boolean` | Yes | Always `true`. |
| `html` | `boolean` | Yes | Always `false`. |
| `screenshot` | `boolean` | Yes | Always `false`. |
| `saveResult` | `boolean` | Yes | Always `true`, so the page is saved to your MrScraper results. |

#### Request example:

```bash
curl --location 'https://api.mrscraper.com/?url=https%3A%2F%2Fwww.scrapethissite.com%2Fpages%2Fsimple%2F&maxAge=0&markdown=true&html=false&screenshot=false&saveResult=true' \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>"
```

#### Response example:

```markdown
# Page title

Page text...
```

#### Notes:

- The response is the page as Markdown text.
- A request can take up to `timeout` (300 seconds when unset); allow 30 seconds more for the response.

### 3. Get Screenshot

- Method: `GET`
- URL: `https://api.mrscraper.com/`
- Auth: `x-api-token` header

Capture a base64 PNG screenshot of the full page, the top viewport, or a custom viewport size. Browser rendering is always enabled. Send the inputs as URL-encoded query parameters. Leave out the optional ones you do not need; MrScraper's defaults then apply.

#### Query parameters:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `url` | `string` | Yes | URL of the page to scrape. Must include the protocol (https://). |
| `screenshot` | `string` | Yes | Screenshot area: `full` captures the entire scroll height (the default), `top` captures the first viewport, and `<width>x<height>` sets the viewport size in pixels with an optional `-<zoom>` percent, such as `1280x800` or `1920x1080-75`. Width and height range from 100 to 3840, zoom from 25 to 300. The image is a base64-encoded PNG. Send `full` unless another area is needed. |
| `timeout` | `integer` | No | Maximum seconds to wait for the scrape before the request times out, from 1 to 330. Increase for slow or complex pages. Defaults to 300. |
| `geoCode` | `string` | No | Two-letter country code to load the page from, such as us or gb. Defaults to the United States. |
| `waitForSelector` | `string` | No | Waits until a specific CSS selector or text appears on the page before returning it, such as #results. Up to 500 characters. Useful for content that loads asynchronously after the initial page load. |
| `maxAge` | `integer` | Yes | Serves a cached result of the same request when it is newer than this age, in milliseconds, such as 86400000 for 1 day. Up to 604800000 (7 days). 0, the default, always scrapes fresh. A cached result costs the same tokens as the original scrape. Send `0` unless the user accepts a cached result. |
| `maxRetries` | `integer` | No | Maximum number of retries for the request. Omit for no limit. |
| `browserRendering` | `boolean` | Yes | Always `true`. |
| `html` | `boolean` | Yes | Always `false`. |
| `markdown` | `boolean` | Yes | Always `false`. |
| `saveResult` | `boolean` | Yes | Always `true`, so the page is saved to your MrScraper results. |

#### Request example:

```bash
curl --location 'https://api.mrscraper.com/?url=https%3A%2F%2Fwww.scrapethissite.com%2Fpages%2Fsimple%2F&screenshot=full&maxAge=0&browserRendering=true&html=false&markdown=false&saveResult=true' \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>"
```

#### Response example:

```json
{
  "screenshot": "iVBORw0KGgo..."
}
```

#### Notes:

- Decode `screenshot` from base64 to get the image.
- A request can take up to `timeout` (300 seconds when unset); allow 30 seconds more for the response.

### 4. Scrape Brand

- Method: `GET`
- URL: `https://api.mrscraper.com/`
- Auth: `x-api-token` header

Extract a website's colors, typography, logos, and social links as JSON. Send the inputs as URL-encoded query parameters.

#### Query parameters:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `action` | `string` | Yes | Always `brand-scraping`. |
| `url` | `string` | Yes | URL of the page to scrape. Must include the protocol (https://). |
| `bundle` | `string` | Yes | Always `none`. |

#### Request example:

```bash
curl --location 'https://api.mrscraper.com/?action=brand-scraping&url=https%3A%2F%2Fmrscraper.com&bundle=none' \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>"
```

#### Notes:

- The response is JSON; the brand is in `data.brand`.
- Allow up to 120 seconds for the response.

### 5. Scrape JSON

- Method: `GET` (`POST` for a request URL over about 8,000 characters)
- URL: `https://api.mrscraper.com/`
- Auth: `x-api-token` header

Extract structured JSON from a page using a natural-language prompt. Append Json Schema: and a JSON schema to shape the output. Send the inputs as URL-encoded query parameters. Leave out the optional ones you do not need; MrScraper's defaults then apply.

#### Query parameters:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `url` | `string` | Yes | URL of the page to scrape. Must include the protocol (https://). |
| `prompt` | `string` | No | Description of the data shape you want back, for example fields like title, price, and rating. The prompt only parses the scraped content; it cannot instruct the scraper itself. To shape the output with a JSON schema, append it to the prompt as a Json Schema: section. Defaults to "Extract all data as complete as possible." |
| `html` | `boolean` | Yes | Returns the raw HTML of the scraped page in the response. On by default; set false to leave it out. |
| `screenshot` | `boolean` | Yes | Captures a screenshot of the rendered page as a base64-encoded image. Useful for verifying what the scraper actually saw. Off by default. |
| `browserRendering` | `boolean` | No | Controls whether the page is loaded in a browser. Leave it out to load the page without a browser first and switch to a browser automatically if the request is blocked. Set true to always load the page in a browser, which JavaScript-heavy sites, SPAs, and pages that load content dynamically need. Set false to never use a browser. |
| `waitForSelector` | `string` | No | Waits until a specific CSS selector or text appears on the page before returning it, such as #results. Up to 500 characters. Useful for content that loads asynchronously after the initial page load. |
| `warmStart` | `boolean` | No | Opens the site's home page first to warm the session before loading the target URL. Useful for sites that expect a normal browsing session before deeper pages. |
| `blockResources` | `boolean` | No | Blocks images, fonts, and stylesheets from loading. Speeds up scraping and reduces bandwidth usage. |
| `timeout` | `integer` | No | Maximum seconds to wait for the scrape before the request times out, from 1 to 330. Increase for slow or complex pages. Defaults to 300. |
| `geoCode` | `string` | No | Two-letter country code to load the page from, such as us or gb. Defaults to the United States. |
| `maxAge` | `integer` | Yes | Serves a cached result of the same request when it is newer than this age, in milliseconds, such as 86400000 for 1 day. Up to 604800000 (7 days). 0, the default, always scrapes fresh. A cached result costs the same tokens as the original scrape. Send `0` unless the user accepts a cached result. |
| `maxRetries` | `integer` | No | Maximum number of retries for the request. Omit for no limit. |
| `agent` | `string` | Yes | Always `general`. |
| `saveResult` | `boolean` | Yes | Always `true`, so the page is saved to your MrScraper results. |

#### Request example:

```bash
curl --location 'https://api.mrscraper.com/?url=https%3A%2F%2Fbooks.toscrape.com%2Fcatalogue%2Fa-light-in-the-attic_1000%2Findex.html&prompt=Extract+title%2C+price%2C+and+rating&html=true&screenshot=false&maxAge=0&agent=general&saveResult=true' \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>"
```

When the request URL would exceed about 8,000 characters (a long prompt or JSON schema), send a `POST` to `https://api.mrscraper.com/` with `url`, `prompt`, and `agent` in a JSON body and the other parameters in the query string:

```bash
curl -X POST 'https://api.mrscraper.com/?html=true&screenshot=false&maxAge=0&saveResult=true' \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "prompt": "Extract title, price, and rating. Json Schema: {\"type\": \"object\", \"properties\": {\"title\": {\"type\": \"string\"}, \"price\": {\"type\": \"string\"}, \"rating\": {\"type\": \"string\"}}}",
    "agent": "general"
  }'
```

#### Response example:

```json
{
  "data": {
    "title": "A Light in the Attic",
    "price": "£51.77",
    "rating": "Three"
  },
  "html": "<!DOCTYPE html>..."
}
```

#### Notes:

- The extracted fields are in `data`; `html` is included unless `html=false`, and `screenshot` (base64) when `screenshot=true`.
- A request can take up to `timeout` (300 seconds when unset); allow 30 seconds more for the response.

### 6. Web Search

- Method: `GET`
- URL: `https://api.mrscraper.com/`
- Auth: `x-api-token` header

Search the web and return ranked results with titles, URLs, descriptions, and sources. Send the inputs as URL-encoded query parameters of a `GET` request to `https://api.mrscraper.com/`. Leave out the optional ones you do not need; MrScraper's defaults then apply.

#### Query parameters:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `action` | `string` | Yes | Always `websearch`. |
| `query` | `string` | Yes | The search query, from 1 to 1000 characters. |
| `country` | `string` | No | Two-letter country code to run the search from. Defaults to the United States. |
| `numResults` | `integer` | No | How many results to return, from 10 to 100. The search may return fewer. Defaults to 10. |

#### Request example:

```bash
curl --location 'https://api.mrscraper.com/?action=websearch&query=web+scraping+api' \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>"
```

To search from another country or get more results, add for example `&country=gb&numResults=20`.

#### Response example:

```json
{
  "success": true,
  "message": "Search completed",
  "data": [
    {
      "rank": 1,
      "title": "Web Scraping API | MrScraper",
      "url": "https://mrscraper.com/",
      "description": "Extract structured data from any website with AI.",
      "source": "MrScraper"
    }
  ],
  "tokenUsage": 1
}
```

#### Notes:

- Results are in `data`, ordered by `rank`.
- Read the pages you select with Scrape HTML or Scrape Markdown (sections 1 and 2).

### 7. Create AI Scraper

- Method: `POST`
- Host: `https://api.app.mrscraper.com`
- Path: `/api/v1/scrapers-ai`
- Auth: `x-api-token`

Create a new AI scraper run from natural-language instructions.

#### Payload parameters (for `agent`: `general` or `agent`: `listing`):

| Field          | Type     | Required | Default  | Description                                                |
| -------------- | -------- | -------- | -------- | ---------------------------------------------------------- |
| `url`          | string   | Yes      | —        | Target URL                                                 |
| `message`      | string   | Yes      | —        | Extraction instruction                                     |
| `agent`        | string   | No       | general  | The AI agent type to use for scraping: `general`, `listing`, or `map`  |
| `proxyCountry` | string   | No       | None     | ISO country code for proxy-based scraping                  |

#### Payload parameters (for `agent`: `map`):

| Field             | Type     | Required | Default   | Description                                                                                                   |
| ----------------- | -------- | -------- | --------- | ------------------------------------------------------------------------------------------------------------- |
| `url`             | `string` | Yes      | —         | Target URL                                           |
| `agent`           | `string` | No       | map       | The AI agent type to use for scraping (for this case it is `map`)                                             |
| `maxDepth`        | `number` | No       | 2         | Maximum depth level for crawling links from the starting URL.<br>0 = only the starting URL, 1 = +direct links |
| `maxPages`        | `number` | No       | 50        | Maximum number of pages to scrape during the crawling process.                                                |
| `limit`           | `number` | No       | 1000      | Maximum number of data records to extract across all pages. Scraping stops when this limit is reached.        |
| `includePatterns` | `string` | No       | ""        | Regex patterns to include (separate multiple with `\|\|`)    |
| `excludePatterns` | `string` | No       | ""        | Regex patterns to exclude (separate multiple with `\|\|`)                                      |

#### Request example:

```bash
curl -X POST "https://api.app.mrscraper.com/api/v1/scrapers-ai" \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
    "message": "Extract title, price, stocks, and rating",
    "agent": "general"
  }'
```

#### Response example:

```json
{
  "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
  "createdAt": "2019-08-24T14:15:22Z",
  "createdById": "e13e432a-5323-4484-a91d-b5969bc564d9",
  "updatedAt": "2019-08-24T14:15:22Z",
  "updatedById": "d8bc6076-4141-4a88-80b9-0eb31643066f",
  "deletedAt": "2019-08-24T14:15:22Z",
  "deletedById": "8ef578ad-7f1e-4656-b48b-b1b4a9aaa1cb",
  "userId": "2c4a230c-5085-4924-a3e1-25fb4fc5965b",
  "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
  "type": "AI",
  "url": "http://example.com",
  "status": "Finished",
  "error": "string",
  "tokenUsage": 0,
  "runtime": 0,
  "data": {}, // MAIN SCRAPED DATA
  "htmlPath": "string",
  "recordingPath": "string",
  "screenshotPath": "string",
  "dataPath": "string"
}
```

#### Notes:

- Choose agent type correctly as each agent is specialized for specified use cases. Use `general` for most standard web scraping tasks. The go to agent if the user doesn't specify or the connected LLM is not confident about the type of page. But mostly used for scraping product page, but handles any type of page very well as well. Use `listing` for scraping listing pages like product listings, job listings, etc. Choose this if the connected LLM can confidently identify whether the given URL is a listing page. Use `map` for crawling and getting all subdomain or subpages of a website. Choose this if the user specifies that the given URL is a website and not a specific page. For `map` agent type, there is a special args that can be used to configure the scraping process.
- For the `map` agent, you can use special arguments to control crawling:<br>`maxDepth` (lower values 1–2 for focused scraping, max 3 recommended),<br>`maxPages` (limits total pages regardless of depth),<br>`limit` (caps total records extracted),<br>and `includePatterns`/`excludePatterns` (regex patterns separated by `||` to specify which URLs to crawl or skip, e.g., `*/products/*||*/blog/*` or `*/cart/*||*.pdf`).<br>If `includePatterns` is an empty string, all URLs are included. If `excludePatterns` is an empty string, no URLs are excluded.

### 8. Rerun AI Scraper

- Method: `POST`
- Host: `https://api.app.mrscraper.com`
- Path: `/api/v1/scrapers-ai-rerun`
- Auth: `x-api-token`

Reruns an existing scraper configuration on a new URL.

#### Payload parameters:

| Field        | Type     | Required | Default | Description                                  |
| ------------ | -------- | -------- | ------- | -------------------------------------------- |
| `scraperId`  | `string` | Yes      | —       | Scraper ID retrieved from created AI scraper |
| `url`        | `string` | Yes      | —       | Target URL                                   |

#### Optional payload parameters for `map` agent:

| Field             | Type   | Required | Default | Description                                                               |
|-------------------|--------|----------|---------|---------------------------------------------------------------------------|
| `maxDepth`        | number | No       | 2       | Crawl depth                                                               |
| `maxPages`        | number | No       | 50      | Maximum pages to crawl                                                    |
| `limit`           | number | No       | 1000    | Result limit                                                              |
| `includePatterns` | string | No       | ""      | Regex patterns to include (separate multiple with `\|\|`)                 |
| `excludePatterns` | string | No       | ""      | Regex patterns to exclude (separate multiple with `\|\|`)                 |

#### Request example:

```bash
curl -X POST "https://api.app.mrscraper.com/api/v1/scrapers-ai-rerun" \
  -H "accept: application/json" \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
    "url": "https://shopee.sg/"
  }'
```

#### Response example:

```json
{
  "message": "Successful operation!",
  "data": {
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    "createdAt": "2019-08-24T14:15:22Z",
    "createdById": "e13e432a-5323-4484-a91d-b5969bc564d9",
    "updatedAt": "2019-08-24T14:15:22Z",
    "updatedById": "d8bc6076-4141-4a88-80b9-0eb31643066f",
    "deletedAt": "2019-08-24T14:15:22Z",
    "deletedById": "8ef578ad-7f1e-4656-b48b-b1b4a9aaa1cb",
    "userId": "2c4a230c-5085-4924-a3e1-25fb4fc5965b",
    "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
    "type": "Rerun-AI",
    "url": "http://example.com",
    "status": "Finished",
    "error": "string",
    "tokenUsage": 0,
    "runtime": 0,
    "data": {}, // MAIN SCRAPED DATA
    "htmlPath": "string",
    "recordingPath": "string",
    "screenshotPath": "string",
    "dataPath": "string",
    "htmlContent": "string"
  }
}
```

### 9. Bulk Rerun AI Scraper

- Method: `POST`
- Host: `https://api.app.mrscraper.com`
- Path: `/api/v1/scrapers-ai-rerun/bulk`
- Auth: `x-api-token`

Runs one scraper configuration over multiple URLs.

#### Payload parameters:

| Field       | Type            | Required | Default | Description                       |
| ----------- | --------------- | -------- | ------- | --------------------------------- |
| `scraperId` | `string`        | Yes      | —       | Existing AI scraper configuration ID |
| `urls`      | `array[string]` | Yes      | —       | Target URLs to run                |

#### Request example:

```bash
curl -X POST "https://api.app.mrscraper.com/api/v1/scrapers-ai-rerun/bulk" \
  -H "x-api-token: " \
  -H "Content-Type: application/json" \
  -d '{
    "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
    "urls": [
      "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
      "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
      "https://books.toscrape.com/catalogue/soumission_998/index.html"
    ]
  }'
```

#### Response example:

```json
{
  "message": "Bulk rerun started successfully",
  "data": {
    "bulkResultId": "f89f8f58-3c9a-42e5-a72e-59fa6c389f09",
    "status": "Running",
    "totalUrls": 3
  }
}
```

### 10. Rerun Manual Scraper

- Method: `POST`
- Host: `https://api.app.mrscraper.com`
- Path: `/api/v1/scrapers-manual-rerun`
- Auth: `x-api-token`

Executes a rerun using a manual browser workflow.

#### Creating a Manual Scraper

Before calling the manual rerun endpoint, you need to create and save a manual scraper from the dashboard. Follow these steps:

1. Open the `MrScraper` dashboard and go to `Scraper`.
2. Click `New Manual Scraper +`.
3. Enter your target URL.
4. Add workflow steps that match your site's behavior (e.g., `Input`, `Click`, `Delay`, `Extract`, `Inject JavaScript`).
5. Configure pagination if needed (using options like `Query Pagination`, `Directory Pagination`, or `Next Page Link`).
6. Test and save the scraper, then copy its `scraperId` to use in API reruns.

#### Payload parameters:

| Field        | Type           | Required | Default | Description                                                                                                      |
|--------------|----------------|----------|---------|------------------------------------------------------------------------------------------------------------------|
| `scraperId`  | `string`       | Yes      | —       | ID of the manual scraper to rerun.                                                                               |
| `url`        | `string`       | Yes      | —       | Target URL for the rerun.                                                                                        |
| `workflow`   | `array<object>`| No       | None    | Allows overriding the saved workflow steps. By default, uses the workflow saved during manual creation.|

#### Request example:

```bash
curl -X POST "https://api.app.mrscraper.com/api/v1/scrapers-manual-rerun" \
  -H "accept: application/json" \
  -H "x-api-token: " \
  -H "Content-Type: application/json" \
  -d '{
    "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
    "url": "https://books.toscrape.com/",
    "workflow": [
      {
        "type": "extract",
        "data": {
          "extraction_type": "text",
          "attribute": null,
          "name": "book",
          "selector": "h3 a"
        }
      }
    ],
    "paginator": {
      "type": "query_pagination",
      "max_page": 1,
      "enabled": false
    }
  }'
```

#### Response example:

```json
{
  "message": "Successful operation!",
  "data": {
    "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
    "createdAt": "2019-08-24T14:15:22Z",
    "createdById": "e13e432a-5323-4484-a91d-b5969bc564d9",
    "updatedAt": "2019-08-24T14:15:22Z",
    "updatedById": "d8bc6076-4141-4a88-80b9-0eb31643066f",
    "deletedAt": "2019-08-24T14:15:22Z",
    "deletedById": "8ef578ad-7f1e-4656-b48b-b1b4a9aaa1cb",
    "userId": "2c4a230c-5085-4924-a3e1-25fb4fc5965b",
    "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
    "type": "Rerun-AI",
    "url": "http://example.com",
    "status": "Finished",
    "error": "string",
    "tokenUsage": 0,
    "runtime": 0,
    "data": {}, // MAIN SCRAPED DATA
    "htmlPath": "string",
    "recordingPath": "string",
    "screenshotPath": "string",
    "dataPath": "string",
    "htmlContent": "string"
  }
}
```

### 11. Bulk Rerun Manual Scraper

- Method: `POST`
- Host: `https://api.app.mrscraper.com`
- Path: `/api/v1/scrapers-manual-rerun/bulk`
- Auth: `x-api-token`

Runs one scraper configuration over multiple URLs.

#### Payload parameters:

| Field       | Type            | Required | Default | Description                       |
| ----------- | --------------- | -------- | ------- | --------------------------------- |
| `scraperId` | `string`        | Yes      | —       | Existing manual scraper configuration ID |
| `urls`      | `array[string]` | Yes      | —       | Target URLs to run                |

#### Request example:

```bash
curl -X POST "https://api.app.mrscraper.com/api/v1/scrapers-manual-rerun/bulk" \
  -H "x-api-token: " \
  -H "Content-Type: application/json" \
  -d '{
    "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
    "urls": [
      "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
      "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
      "https://books.toscrape.com/catalogue/soumission_998/index.html"
    ]
  }'
```

#### Response example:

```json
{
  "message": "Bulk rerun started successfully",
  "data": {
    "bulkResultId": "f89f8f58-3c9a-42e5-a72e-59fa6c389f09",
    "status": "Running",
    "totalUrls": 3
  }
}
```

### 12. Fetch Results

- Method: `GET`
- Host: `https://api.app.mrscraper.com`
- Path: `/api/v1/results`
- Auth: `x-api-token`

Returns paginated scrape results.

#### Query parameters:

| Field             | Type   | Required | Default     | Description               |
|-------------------|--------|----------|-------------|---------------------------|
| `sortField`       | string | Yes      | `updatedAt` | Sort column               |
| `sortOrder`       | string | Yes      | `DESC`      | Sort direction            |
| `page`            | number | Yes      | 1           | Page number               |
| `pageSize`        | number | Yes      | 10          | Items per page            |
| `search`          | string | No       | None        | Search keyword            |
| `dateRangeColumn` | string | No       | `createdAt` | Date field to filter      |
| `startAt`         | string | No       | None        | Date range start (ISO)    |
| `endAt`           | string | No       | None        | Date range end (ISO)      |

#### Notes:

- `sortField` options: `createdAt`, `updatedAt`, `id`, `type`, `url`, `status`, `error`, `tokenUsage`, `runtime`
- `sortOrder` options: `ASC`, `DESC`
- `dateRangeColumn` options: `createdAt`, `updatedAt`

#### Request example:

```bash
curl -X GET "https://api.app.mrscraper.com/api/v1/results?sortField=updatedAt&sortOrder=DESC&pageSize=10&page=1" \
  -H "accept: application/json" \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>"
```

#### Response example:

```json
{
  "message": "Successful fetch",
  "data": [
    {
      "createdAt": "2025-11-11T09:50:09.722Z",
      "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
      "userId": "2c4a230c-5085-4924-a3e1-25fb4fc5965b",
      "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
      "type": "AI",
      "url": "http://example.com",
      "status": "Finished",
      "error": "string",
      "tokenUsage": 5,
      "runtime": 0,
      "data": "{ \"title\": \"Product A\", \"price\": \"$10\" }",
      "htmlPath": "string",
      "recordingPath": "string",
      "screenshotPath": "string",
      "dataPath": "string"
    }
  ],
  "meta": {
    "page": 1,
    "pageSize": 10,
    "total": 1,
    "totalPage": 1
  }
}
```

### 13. Fetch Detailed Result by ID

- Method: `GET`
- Host: `https://api.app.mrscraper.com`
- Path: `/api/v1/results/{id}`
- Auth: `x-api-token`

Returns one detailed result object for a specific result ID.

#### Query parameters:

| Field | Type     | Required | Default | Description |
| ----- | -------- | -------- | ------- | ----------- |
| `id`  | `string` | Yes      | —       | Result ID   |

#### Request example:

```bash
curl -X GET "https://api.app.mrscraper.com/api/v1/results/497f6eca-6276-4993-bfeb-53cbbbba6f08" \
  -H "accept: application/json" \
  -H "x-api-token: <MRSCRAPER_API_TOKEN>"
```

#### Response example:

```json
{
  "message": "Successful fetch",
  "data": [
    {
      "createdAt": "2025-11-11T09:50:09.722Z",
      "id": "497f6eca-6276-4993-bfeb-53cbbbba6f08",
      "userId": "2c4a230c-5085-4924-a3e1-25fb4fc5965b",
      "scraperId": "6695bf87-aaa6-46b0-b1ee-88586b222b0b",
      "type": "AI",
      "url": "http://example.com",
      "status": "Finished",
      "error": "string",
      "tokenUsage": 5,
      "runtime": 0,
      "data": "string",
      "htmlPath": "string",
      "recordingPath": "string",
      "screenshotPath": "string",
      "dataPath": "string"
    }
  ]
}
```

## Errors

Standard platform API errors:

| Status | Meaning                      |
| ------ | ---------------------------- |
| `400`  | Invalid request payload      |
| `401`  | Missing or invalid API token |
| `404`  | Scraper or result not found  |
| `429`  | Rate limit exceeded          |
| `500`  | Internal scraper error       |

Error format:

```json
{
  "message": "string",
  "error": "string",
  "statusCode": "number"
}
```

## Operating Rules

- Validate required fields before every call.
- Use pagination for large result sets.
- Retry on `429` with exponential backoff.
- Never expose credentials in outputs.
