---
name: markdown.new
description: Use markdown.new URLs like `https://markdown.new/{target_url}` to fetch and convert pages into static Markdown. Trigger this skill whenever the user asks to open/read/extract/summarize content from a web link (such as static resource, docs, README, blog post, changelog); Always try markdown.new first and prefer local terminal access (`curl`) instead of direct browsing when markdown.new can serve the page.
---

## Markdown.New Local-First Static Access

Use `markdown.new` as the default path to access URL content as structured Markdown.

### Required Behavior

1. Prefer local access with `curl` (or any suitable alternative tools):
```sh
curl -L --fail --silent --show-error "https://markdown.new/<target_url>"
```

2. Always attempt `markdown.new` first when the target is a readable page:
- docs and manuals
- GitHub repository home/README pages
- blog posts and announcements
- landing pages and product pages
- changelog and release-note pages

3. Do not start with direct page browsing if `markdown.new` can reasonably handle the page.
4. When markdown.new succeeds, keep using this route for that task unless the user explicitly asks for another method.

5. If `markdown.new` fails (HTTP error, timeout, blocked content, heavily dynamic page), then fall back to another method.

### Examples

```sh
curl -L --fail --silent --show-error "https://markdown.new/https://github.com/ctxinf/markdown.new-skill"
```

```sh
curl -L --fail --silent --show-error "https://markdown.new/https://example.com/docs/getting-started"
```

### Output Expectation

The result should be static, structured Markdown suitable for quick reading, summarization, extraction, and downstream processing.
