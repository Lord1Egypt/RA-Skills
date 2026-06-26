---
name: "News Corbett Report"
description: "The Corbett Report — official WordPress RSS at corbettreport.com/feed/. Fetch only; answer in English; items strictly from XML; dated header, numbered list, title as link, optional teaser from <description>."
tags: ["news", "corbett", "podcast", "feed", "rss"]
hint_allow_substrings: ["corbett", "corbett report", "james corbett"]
requires: []
source: "https://corbettreport.com/"
---

# The Corbett Report — RSS

Independent outlet (James Corbett). For current episodes and posts use **only** the official feed — do not invent third-party pages or items.

## Feed (prefer `fetch` tool)

```text
https://corbettreport.com/feed/
```

Optional check:

```bash
curl -sL "https://corbettreport.com/feed/"
```

## Format (RSS 2.0)

Typical fields:

- **Channel:** `<title>`, `<link>`, `<lastBuildDate>`
- **Each `<item>`:** `<title>`, `<link>` (canonical post URL), `<pubDate>`, `<description>` (teaser), optional `<category>` (may repeat), often `<enclosure>` (MP3). For the reply, the **post link** is always `<link>`, not the enclosure URL.

Render XML entities readably (e.g. `&#8211;` → en dash). Do **not** expand or rewrite feed text.

## Rules

- Only headlines, URLs, and teasers that appear **in the same `<item>`**. No extra episodes or URLs.
- Default: **newest first** (feed order), **3–5** items unless the user asks for a different count.
- **Language:** Write the **entire** answer in **English** — headings, labels, and quoted teaser text exactly as in the feed. **Do not** translate into German (or other languages) unless the user explicitly asks for a translation.

## Mandatory

Non-negotiable checklist (single-file skill — everything lives in this README):

1. **Source:** Use only items from `https://corbettreport.com/feed/` after a successful `fetch`. Do not invent titles or URLs.

2. **Per item:** Title, link, and teaser must come from the **same** `<item>`. The article URL is the item’s `<link>`, **not** the MP3 `enclosure` URL.

3. **Count:** Default **3–5** newest items unless the user specifies otherwise.

4. **Layout:** `##` title, optional `###` for the list; blank line after headings; numbered list; **`**[title](url)**`** with no separate link line.

5. **Language:** Reply **fully in English** (headings, labels, and feed text as-is). **No** German or other translation unless the user explicitly requests translation.

## Response layout

No emoji required. Blank line after `##` / `###`. Each item on its own line(s).

```markdown
## The Corbett Report

*As of feed `lastBuildDate`: …*

### Latest

1. **[Exact `<title>`](https://corbettreport.com/…/)** — *categories if useful*
   - *Teaser from `<description>` (trim if long, ~200 chars max)*

2. …
```

- Put the URL only inside the title link: `**[…](url)**`, not a separate `*Link:*` line.
- Categories: copy from `<category>` only; omit if empty or redundant.

## Errors

If the feed is empty or fetch fails, say so briefly — do not invent content.

## When to use

Questions about Corbett Report, James Corbett, latest episode or interview, Corbett podcast headlines, “what’s new on Corbett Report”.
