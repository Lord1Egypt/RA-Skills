# AI search (GEO): getting read and cited by AI answer engines

## Crawlers: search and user fetches vs. training

Each AI company runs separate crawlers. Blocking the *training* crawler doesn't remove a site from that company's *search* answers. Blocking the *search* crawler does.

| Company | Search / citations | Fetches when a user asks | Model training |
| --- | --- | --- | --- |
| OpenAI (ChatGPT) | OAI-SearchBot | ChatGPT-User | GPTBot |
| Anthropic (Claude) | Claude-SearchBot | Claude-User | ClaudeBot |
| Perplexity | PerplexityBot | Perplexity-User | – |
| Google | Googlebot (AI Overviews and AI Mode use normal Search) | – | Google-Extended (Gemini; no effect on Search) |
| Apple | Applebot | – | Applebot-Extended |

Default recommendation: allow everything. A founder usually wants the product known to every model. If the user wants to opt out of training only:

```txt
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: *
Allow: /

Sitemap: https://example.com/sitemap.xml
```

Also check for blocks outside robots.txt: Cloudflare's "Block AI bots" / AI Crawl Control, WAF rules and bot-fight modes. `audit_ai_search` notes when our crawler was refused but a browser got the page.

## Content must be in the HTML

Most AI crawlers fetch HTML and don't run JavaScript. If `audit_ai_search` or `audit_page` reports thin or missing main content on a page that looks fine in a browser, the page is client-rendered. Fix the rendering first (see frameworks.md).

## llms.txt

A markdown map of the site for language models, served as `text/plain` or `text/markdown` at `/llms.txt`:

```markdown
# Product Name

> One paragraph: what the product is, who it's for, and what makes it different. Plain facts, no hype.

Optional short paragraphs with key facts (pricing model, platforms, integrations).

## Product

- [Features](https://example.com/features): what it does, feature by feature
- [Pricing](https://example.com/pricing): plans and limits

## Docs

- [Getting started](https://example.com/docs/start): install and first run

## Optional

- [Blog](https://example.com/blog): guides and announcements
```

Rules the validator checks: one H1 first, a blockquote summary, H2 sections whose list items are `- [name](absolute-url): note`, and links that resolve. Generate it from the real sitemap and navigation, so it stays true. `/llms-full.txt` (the full text of key pages) is optional.

## Markdown twins

Serving a clean markdown version of content pages (`/docs/start.md`, or markdown when the request sends `Accept: text/markdown`) makes pages cheap for agents to read. Worth doing for docs and long-form content. Low priority for marketing pages.

## Pages that get cited

- **Answer first**: a question as the heading (`## How much does X cost?`), and the answer in the first sentence under it. Details follow.
- **Structure**: lists for steps and options, tables for comparisons and pricing. Models lift these cleanly.
- **Specifics**: numbers, dates, named integrations and limits. Vague marketing copy gives a model nothing to quote.
- **Comparison and alternatives pages** ("X vs Y", "X alternatives") match how people ask assistants, as long as they're honest.
- **Freshness**: a visible "Updated" date, plus `dateModified` in `Article` JSON-LD, changed only when the content really changes.

## Entity signals

- `Organization` JSON-LD on the home page: `name`, `url`, `logo`, `sameAs` (X/Twitter, LinkedIn, GitHub, Product Hunt, Crunchbase).
- For software, `SoftwareApplication` with `applicationCategory`, `operatingSystem` and `offers`. Add `aggregateRating` only if real reviews exist on the page.
- The same product name and one-line description everywhere: site, directories, social bios. Assistants learn a product from what third-party sites say about it, so directory listings and reviews help.

## Measuring

AI answers vary per run, so check a fixed set of real buyer questions over time rather than one prompt once. LaunchRanked's free AI visibility checker (https://launchranked.com/tools/ai-visibility-checker) runs a snapshot. Autopilot tracks 25 prompts across ChatGPT, Perplexity, Gemini and Claude over time.
