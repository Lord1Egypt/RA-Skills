---
name: markdown-publish
description: Publishes Markdown to a public URL and returns the link. Use when the user asks to share, publish, host, or get a link for a page — or when you have produced a long page that is better delivered as a link than pasted inline. No authentication required. Pages are public and cannot be edited after publishing, so do not publish secrets or private data.
compatibility: Requires curl and network access to https://markdown.page.
---

# Publish Markdown

Publish Markdown to a public URL. Browsers receive HTML; command-line tools and agents receive plain text. No account or API key required.

## Publication judgment

Pages are public and cannot be edited after publishing. Use your judgment about whether the user's request and content are appropriate to publish. To correct a page, publish a new one; removal can be requested through the page's report link.

## Workflow

1. Identify the Markdown file or compose the requested content in a `.md` file.
2. Check that the Markdown is no larger than 1 MB.
3. Publish it:

```bash
curl https://markdown.page/api/publish --data-binary @PATH_TO_FILE.md
```

4. On success, return the URL printed by the command. The raw Markdown is available by appending `.md` to that URL.

Do not claim success unless the command succeeds and returns a `https://markdown.page/...` URL. For HTTP 429, explain that the fair-use rate limit was reached, back off before at most one retry, and do not loop.

## Service details

- Authentication: none
- Maximum Markdown page: 1 MB (request envelope: 2 MB)
- Rendered page: `https://markdown.page/{slug}`
- Raw source: `https://markdown.page/{slug}.md`
- Read negotiation: browsers receive rendered HTML; `Accept: text/plain` receives plain text; `.md` always returns source Markdown
- Supported syntax: standard Markdown and GFM, including tables, task lists, fenced code, and HTTP(S) images
- Links may use `https://`, `http://`, or `mailto:`

Typical errors: `400` malformed or unsupported body; `413` page or request envelope exceeds its limit; `415` unsupported content type; `429` fair-use rate limit.

Official references: [agent guide](https://markdown.page/llms.txt), [API reference](https://markdown.page/api.md), and [FAQ](https://markdown.page/faq.md).
