---
name: juya
description: Fetch Juya AI Daily (juya-ai-daily) newsletter content. Use when the user asks to view AI daily news, AI morning briefing, or Juya daily. Supports fetching a specific date, defaults to today.
---

# Juya AI Daily

RSS feed URL: `https://imjuya.github.io/juya-ai-daily/rss.xml`

## Usage

1. Fetch the RSS feed using `web_fetch`
2. Parse `<item>` list from the returned XML
3. Match the target entry by date (format `YYYY-MM-DD`), default to the latest
4. Extract HTML content from `<content:encoded>`, format as Markdown
5. For full content, visit the corresponding `<link>` for the detail page

## Date Matching

- Each item's `<title>` is in `YYYY-MM-DD` format
- Match by title when user specifies a date
- Default to the first (latest) item when no date is specified

## Output Format

Organize as a clean Markdown list, grouped by category (headlines, model releases, developer ecosystem, etc.), with titles and links.
