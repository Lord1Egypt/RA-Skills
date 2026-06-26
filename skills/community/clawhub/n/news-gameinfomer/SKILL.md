---
name: "Gameinformer News"
description: "Game Informer — section RSS (news/reviews/previews/features). Fetch per section; English reply; only ### headings for sections with at least one item from that feed; no empty placeholders; title as markdown link."
tags: ["news", "games", "game-informer", "rss"]
hint_allow_substrings: ["gameinformer", "game informer", "game news", "gaming news"]
requires: []
source: "https://www.gameinformer.com/"
---

# Game Informer — news by section

Official **per-section** RSS feeds (RSS 2.0). Each section has its **own** URL — do **not** guess categories from the all-in-one feed when the user wants the usual overview.

## Feed URLs (use `fetch`)

Use `https://www.gameinformer.com/…` (or `https://gameinformer.com/…` — both work).

| Section | URL |
|---------|-----|
| **News** | `https://www.gameinformer.com/news.xml` |
| **Reviews** | `https://www.gameinformer.com/reviews.xml` |
| **Previews** | `https://www.gameinformer.com/previews.xml` |
| **Features** | `https://www.gameinformer.com/features.xml` |

**All recent content (no section split):** `https://www.gameinformer.com/rss.xml` — use only when the user explicitly wants one combined feed, not the four blocks below.

## XML (per item)

Typical fields: `<title>`, `<link>` (canonical article URL), `<pubDate>`, `<description>` (often long HTML), optional `<dc:creator>`.

- Use **exact** `<title>` and `<link>` from the **same** `<item>`.
- **Do not** paste raw HTML from `<description>`; at most a **very short** plain-text teaser if you strip tags safely — otherwise **title + link only**.

## Which feeds to load

| User intent | Fetches |
|-------------|---------|
| Generic: Game Informer / GI / “what’s new” / headlines overview | **All four** section feeds (`news`, `reviews`, `previews`, `features`) — **four** separate `fetch` calls |
| Only news / reviews / previews / features | Only the matching `.xml` URL(s) |
| Explicitly “everything in one list” / main RSS only | `rss.xml` only (single section in the reply is OK) |

## Response — section layout (only non-empty feeds)

Language: **English** for headings and any prose.

Include a `###` section **only** when that feed was **loaded successfully** and you are listing **at least one** `<item>` from it.

**Do not** output a section that has no items — no headings like `### Reviews` with “No reviews available”, “Nothing in the feed”, or *(Feed unavailable.)*. If you did not fetch that URL or the XML has no items, **omit** that section entirely.

If several section feeds have items, use headings in this **order** (skip any that you omit): **News → Reviews → Previews → Features**.

Example when only **News** has data (e.g. only `news.xml` was fetched):

```markdown
## Game Informer

### News

1. **[Title from news.xml](exact-link-from-item)**
2. …
```

Example when **News** and **Reviews** both have data:

```markdown
## Game Informer

### News

1. **[Title](url)**

### Reviews

1. **[Title](url)**
```

Rules:

- **Blank line** after each `##` / `###`.
- **Numbered lists** under each included section; default **3–5** items per section unless the user asks otherwise.
- Put the URL **only** in the title: `**[Title](url)**` — no separate `Link:` line.
- A story from `news.xml` appears **only** under **News**; same for reviews/previews/features. **Never** list a reviews feed item under News.

## Mandatory

Non-negotiable checklist (single-file skill — everything lives in this README):

1. **Sections map to feeds:** **News** = `news.xml`, **Reviews** = `reviews.xml`, **Previews** = `previews.xml`, **Features** = `features.xml`. Items may appear **only** under the section whose feed they came from.

2. **Overview questions:** If the user does not restrict to one topic, **fetch all four** URLs (four separate `fetch` calls) before answering — when the runtime allows multiple fetches.

3. **Reply shape — omit empty:** Output `### News` / `### Reviews` / `### Previews` / `### Features` **only** for feeds you actually loaded **and** that contain **at least one** item you list. **Forbidden:** empty sections, “No reviews available”, “Nothing in the current feed”, or similar placeholders for a feed you did not populate from XML.

4. **Order:** Among sections you **do** include, use this order: News, then Reviews, then Previews, then Features.

5. **Items:** Title and URL must be from the **same** `<item>`. Use **`**[title](url)**`**. No invented stories. Default **3–5** items per **included** section unless the user specifies another count.

6. **Language:** Reply in **English**.

7. **Descriptions:** Do not dump HTML from `<description>`; title + link is enough unless a short plain teaser is clearly safe.

## Errors

If all fetches fail, say so — do not invent headlines.

## When to use

Game Informer, GI, gaming news from Game Informer, reviews/previews/features from the site, “latest Game Informer stories”.
