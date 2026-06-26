---
name: jina-reader
description: Fetch clean, AI-friendly Markdown content from any URL using Jina.ai Reader. Bypasses paywalls, handles Twitter/X posts, renders JavaScript-heavy pages, returns structured content with titles and metadata. Use this when you need to read or extract content from web pages after search, or when dealing with paywalled sites, Twitter/X, or SPA pages that need JS rendering.
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["node"]}}}
---

# Jina.ai Reader

Fetch clean, AI-friendly Markdown content from any URL. No API key required.

## Features

- ✅ Bypasses paywalls (tested with Every.to, Medium, etc.)
- ✅ Handles Twitter/X posts and threads
- ✅ Renders JavaScript-heavy pages (optional wait)
- ✅ Returns clean Markdown format
- ✅ **Free, no API key needed**

## Basic Usage

```bash
node {baseDir}/scripts/jina-reader.mjs "https://example.com/article"
```

## Options

| Option | Description |
|--------|-------------|
| `--wait-ms N` | Wait N milliseconds for JavaScript to render |
| `--with-images` | Include image captions in output |
| `--with-links` | Include all links in output |

## Examples

```bash
# Basic fetch
node {baseDir}/scripts/jina-reader.mjs "https://every.to/article"

# Twitter/X post
node {baseDir}/scripts/jina-reader.mjs "https://twitter.com/user/status/123456"

# Wait for JavaScript rendering
node {baseDir}/scripts/jina-reader.mjs "https://spa-site.com/page" --wait-ms 5000

# With images and links
node {baseDir}/scripts/jina-reader.mjs "https://blog.example.com/post" --with-images --with-links
```

## When to Use

- **Search + Read**: After Tavily/desearch finds URLs, use this to read the actual content
- **Twitter/X**: Most tools can't handle Twitter, this one can
- **Paywalled sites**: Works on many sites that require login
- **SPA/JS-heavy pages**: Use `--wait-ms` to let scripts run

## Notes

- No API key required
- Rate limits may apply for heavy usage
- For pagination, you may need to fetch multiple pages manually
