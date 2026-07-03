# HTML standards for Medium's URL importer

Medium's URL importer converts only a constrained subset of HTML into blocks
cleanly. Anything outside this subset is stripped, mangled, or rejected.
**Load this file before writing a post.** `assets/post-template.html` is a
ready-to-fill reference implementation of every rule below.

## Document structure

- Exactly **one `<h1>`**, at the very top, identical to `<title>`.
- Body: an opening hook `<p>`, then 3–6 `<h2>` sections (optionally with
  `<h3>` subsections), at least one image, a `<blockquote>` pull-quote, and a
  closing `<p>` with a summary or call to action.

## Allowed tags

| Tag | Notes |
|-----|-------|
| `<h1>` | Exactly one per post, identical to `<title>` |
| `<h2>` | Section headings (use liberally) |
| `<h3>` | Subsections |
| `<p>` | Body paragraphs (keep them short — Medium breaks long ones visually) |
| `<strong>` | Bold |
| `<em>` | Italic |
| `<a href="...">` | Links |
| `<img src="..." alt="...">` | Absolute HTTPS URLs only |
| `<blockquote>` | Pull-quotes |
| `<pre><code>` | Code blocks |
| `<ul>` / `<ol>` / `<li>` | Lists |
| `<hr>` | Section dividers — **max 2 per post** |

## Banned tags and patterns

| Banned | Why |
|--------|-----|
| `<script>` | Stripped; never executes in Medium |
| `<style>` | Stripped |
| `<iframe>` | Rejected |
| `<table>` | Medium's importer doesn't render tables cleanly |
| `<div>`, `<span>` | Stripped |
| Inline `style="..."` | Stripped |
| `<h4>`, `<h5>`, `<h6>` | Use `<h3>` and bold text instead |

## Images

- **Absolute HTTPS only.** No relative paths.
- Recommended source: `https://images.unsplash.com/photo-{ID}?w=1200&q=80`.
  (Hotlinking the Unsplash CDN is fine for personal posts; for higher-volume
  use, follow Unsplash's API and attribution guidelines.)
- Always provide `alt` text.

## Code blocks

- Inside `<pre><code>`, use HTML entities `&lt;` and `&gt;` for `<` and `>`.
- The importer does not highlight syntax; rely on monospace formatting.

## YouTube embeds

Paste the bare URL in its own `<p>` — Medium's importer converts it into an
embed block:

```html
<p>https://www.youtube.com/watch?v=VIDEO_ID</p>
```

## Cover image and published date (`<head>` metadata)

For posts to import with the correct cover image and date, include:

```html
<meta property="og:image" content="COVER_IMAGE_URL">
<meta property="article:published_time" content="YYYY-MM-DDTHH:MM:SSZ">
```

`og:image` requires an absolute HTTPS URL; `article:published_time` requires
ISO-8601 (`YYYY-MM-DDTHH:MM:SSZ`).

## Content quality

No hallucinated facts. No filler. No LLM-tells like "in conclusion" or
"as we have seen".
