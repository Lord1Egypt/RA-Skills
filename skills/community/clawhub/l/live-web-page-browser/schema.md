# Live Web Page Browser Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `live-web-page-browser`

x402 availability: not enabled for this product.

## `cancel_crawl`

Action slug: `cancel-crawl`

Price: `5` credits

Cancel a running crawl job

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `job_id` | `string` | yes | See the product schema for accepted values. |

Sample parameters:

```json
{
  "job_id": "example job id"
}
```

Generated JSON parameter schema:

```json
{
  "job_id": {
    "type": "string"
  }
}
```

## `get_crawl_result`

Action slug: `get-crawl-result`

Price: `5` credits

Get the status and records of a crawl job started with start_crawl

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `job_id` | `string` | yes | See the product schema for accepted values. |

Sample parameters:

```json
{
  "job_id": "example job id"
}
```

Generated JSON parameter schema:

```json
{
  "job_id": {
    "type": "string"
  }
}
```

## `get_instructions`

Action slug: `get-instructions`

Price: `5` credits

Get tool instructions and available actions.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `get_url_html_content`

Action slug: `get-url-html-content`

Price: `5` credits

Get page HTML content

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser` | `string` | no | Browser that renders the page. Omit to use the default Chrome browser. Set to "kitesurf" to use the Kitesurf browser engine. |
| `url` | `string` | yes | {"format": "uri"} |

Sample parameters:

```json
{
  "browser": "kitesurf",
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "browser": {
    "description": "Browser that renders the page. Omit to use the default Chrome browser. Set to \"kitesurf\" to use the Kitesurf browser engine.",
    "enum": [
      "kitesurf"
    ],
    "type": "string"
  },
  "url": {
    "format": "uri",
    "type": "string"
  }
}
```

## `get_url_json`

Action slug: `get-url-json`

Price: `5` credits

Extract structured JSON from a page using AI. Provide a prompt and/or a response_format JSON schema to guide extraction.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser` | `string` | no | Browser that renders the page. Omit to use the default Chrome browser. Set to "kitesurf" to use the Kitesurf browser engine. |
| `prompt` | `string` | no | Natural-language instruction for what to extract |
| `response_format` | `object` | no | Optional JSON-schema response format to constrain the output |
| `url` | `string` | yes | {"format": "uri"} |

Sample parameters:

```json
{
  "browser": "kitesurf",
  "prompt": "example prompt",
  "response_format": {
    "json_schema": "example json schema",
    "type": "example type"
  },
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "browser": {
    "description": "Browser that renders the page. Omit to use the default Chrome browser. Set to \"kitesurf\" to use the Kitesurf browser engine.",
    "enum": [
      "kitesurf"
    ],
    "type": "string"
  },
  "prompt": {
    "description": "Natural-language instruction for what to extract",
    "type": "string"
  },
  "response_format": {
    "description": "Optional JSON-schema response format to constrain the output",
    "properties": {
      "json_schema": {},
      "type": {
        "type": "string"
      }
    },
    "required": [
      "type"
    ],
    "type": "object"
  },
  "url": {
    "format": "uri",
    "type": "string"
  }
}
```

## `get_url_links`

Action slug: `get-url-links`

Price: `5` credits

Get the list of links on a page

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser` | `string` | no | Browser that renders the page. Omit to use the default Chrome browser. Set to "kitesurf" to use the Kitesurf browser engine. |
| `url` | `string` | yes | {"format": "uri"} |
| `visibleLinksOnly` | `boolean` | no | Only return links that are visible in the rendered page |

Sample parameters:

```json
{
  "browser": "kitesurf",
  "url": "https://example.com",
  "visibleLinksOnly": true
}
```

Generated JSON parameter schema:

```json
{
  "browser": {
    "description": "Browser that renders the page. Omit to use the default Chrome browser. Set to \"kitesurf\" to use the Kitesurf browser engine.",
    "enum": [
      "kitesurf"
    ],
    "type": "string"
  },
  "url": {
    "format": "uri",
    "type": "string"
  },
  "visibleLinksOnly": {
    "description": "Only return links that are visible in the rendered page",
    "type": "boolean"
  }
}
```

## `get_url_markdown`

Action slug: `get-url-markdown`

Price: `5` credits

Get page converted into Markdown

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser` | `string` | no | Browser that renders the page. Omit to use the default Chrome browser. Set to "kitesurf" to use the Kitesurf browser engine. |
| `url` | `string` | yes | {"format": "uri"} |

Sample parameters:

```json
{
  "browser": "kitesurf",
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "browser": {
    "description": "Browser that renders the page. Omit to use the default Chrome browser. Set to \"kitesurf\" to use the Kitesurf browser engine.",
    "enum": [
      "kitesurf"
    ],
    "type": "string"
  },
  "url": {
    "format": "uri",
    "type": "string"
  }
}
```

## `get_url_pdf`

Action slug: `get-url-pdf`

Price: `5` credits

Render a page to PDF

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser` | `string` | no | Browser that renders the page. Omit to use the default Chrome browser. Set to "kitesurf" to use the Kitesurf browser engine. |
| `url` | `string` | yes | {"format": "uri"} |

Sample parameters:

```json
{
  "browser": "kitesurf",
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "browser": {
    "description": "Browser that renders the page. Omit to use the default Chrome browser. Set to \"kitesurf\" to use the Kitesurf browser engine.",
    "enum": [
      "kitesurf"
    ],
    "type": "string"
  },
  "url": {
    "format": "uri",
    "type": "string"
  }
}
```

## `get_url_screenshot`

Action slug: `get-url-screenshot`

Price: `5` credits

Get page screenshot

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser` | `string` | no | Browser that renders the page. Omit to use the default Chrome browser. Set to "kitesurf" to use the Kitesurf browser engine. |
| `url` | `string` | yes | {"format": "uri"} |
| `viewport` | `object` | no | See the product schema for accepted values. |

Sample parameters:

```json
{
  "browser": "kitesurf",
  "url": "https://example.com",
  "viewport": {
    "height": 600,
    "width": 800
  }
}
```

Generated JSON parameter schema:

```json
{
  "browser": {
    "description": "Browser that renders the page. Omit to use the default Chrome browser. Set to \"kitesurf\" to use the Kitesurf browser engine.",
    "enum": [
      "kitesurf"
    ],
    "type": "string"
  },
  "url": {
    "format": "uri",
    "type": "string"
  },
  "viewport": {
    "properties": {
      "height": {
        "default": 600,
        "type": "number"
      },
      "width": {
        "default": 800,
        "type": "number"
      }
    },
    "type": "object"
  }
}
```

## `get_url_snapshot`

Action slug: `get-url-snapshot`

Price: `5` credits

Get page HTML content and a screenshot in a single call

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser` | `string` | no | Browser that renders the page. Omit to use the default Chrome browser. Set to "kitesurf" to use the Kitesurf browser engine. |
| `url` | `string` | yes | {"format": "uri"} |

Sample parameters:

```json
{
  "browser": "kitesurf",
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "browser": {
    "description": "Browser that renders the page. Omit to use the default Chrome browser. Set to \"kitesurf\" to use the Kitesurf browser engine.",
    "enum": [
      "kitesurf"
    ],
    "type": "string"
  },
  "url": {
    "format": "uri",
    "type": "string"
  }
}
```

## `kill_browser_session`

Action slug: `kill-browser-session`

Price: `5` credits

Close (kill) a Browser Run session by its session ID

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `session_id` | `string` | yes | See the product schema for accepted values. |

Sample parameters:

```json
{
  "session_id": "example session id"
}
```

Generated JSON parameter schema:

```json
{
  "session_id": {
    "type": "string"
  }
}
```

## `list_browser_sessions`

Action slug: `list-browser-sessions`

Price: `5` credits

List active Browser Run sessions for the account

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `scrape_url_elements`

Action slug: `scrape-url-elements`

Price: `5` credits

Scrape elements from a page by CSS selector

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser` | `string` | no | Browser that renders the page. Omit to use the default Chrome browser. Set to "kitesurf" to use the Kitesurf browser engine. |
| `elements` | `array` | yes | CSS selectors of the elements to scrape |
| `url` | `string` | yes | {"format": "uri"} |

Sample parameters:

```json
{
  "browser": "kitesurf",
  "elements": [
    {
      "selector": "example selector"
    }
  ],
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "browser": {
    "description": "Browser that renders the page. Omit to use the default Chrome browser. Set to \"kitesurf\" to use the Kitesurf browser engine.",
    "enum": [
      "kitesurf"
    ],
    "type": "string"
  },
  "elements": {
    "description": "CSS selectors of the elements to scrape",
    "items": {
      "properties": {
        "selector": {
          "type": "string"
        }
      },
      "required": [
        "selector"
      ],
      "type": "object"
    },
    "minItems": 1,
    "type": "array"
  },
  "url": {
    "format": "uri",
    "type": "string"
  }
}
```

## `start_crawl`

Action slug: `start-crawl`

Price: `5` credits

Start an asynchronous crawl of a website. Returns a job_id — poll get_crawl_result to retrieve records.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `browser` | `string` | no | Browser that renders the crawled pages. Omit to use the default Chrome browser. Set to "kitesurf" to use the Kitesurf browser engine. Requires render to be true. |
| `depth` | `integer` | no | How many links deep to crawl |
| `limit` | `integer` | no | Maximum number of pages to crawl |
| `render` | `boolean` | no | Whether to render pages with a browser (vs. fetching raw HTML) |
| `url` | `string` | yes | {"format": "uri"} |

Sample parameters:

```json
{
  "browser": "kitesurf",
  "depth": 1,
  "limit": 1,
  "render": true,
  "url": "https://example.com"
}
```

Generated JSON parameter schema:

```json
{
  "browser": {
    "description": "Browser that renders the crawled pages. Omit to use the default Chrome browser. Set to \"kitesurf\" to use the Kitesurf browser engine. Requires render to be true.",
    "enum": [
      "kitesurf"
    ],
    "type": "string"
  },
  "depth": {
    "description": "How many links deep to crawl",
    "maximum": 9007199254740991,
    "minimum": 1,
    "type": "integer"
  },
  "limit": {
    "description": "Maximum number of pages to crawl",
    "maximum": 9007199254740991,
    "minimum": 1,
    "type": "integer"
  },
  "render": {
    "default": true,
    "description": "Whether to render pages with a browser (vs. fetching raw HTML)",
    "type": "boolean"
  },
  "url": {
    "format": "uri",
    "type": "string"
  }
}
```
