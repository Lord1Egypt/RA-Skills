---
name: hn-news
description: Fetch and display Hacker News stories about AI, agents, and Claude. Default is past week. Use when the user asks for HN news, Hacker News AI stories, latest AI news or "what's AI trending on Hacker News".
---

# Hacker News — AI & Agent Stories

Fetch and present the latest Hacker News stories about AI, agents, and Claude.

## Source

- API: HN Algolia search (`https://hn.algolia.com/api/v1/search_by_date`)
- Keywords: `AI OR "agent" OR claude`
- Type: stories only

## Workflow

1. Run the script to fetch news:
   - **Default (past week):** `python skills/hn-news/hn.py week`
   - **Latest:** `python skills/hn-news/hn.py latest`
   - **Pagination:** add `--page N` (0-based)
2. Parse the output and reformat into a clean, readable digest

## Output Format

Present each story as:

```
### N. Title

👤 Author · ⭐ Points · 🕒 Time

🔗 [Link]
```

Separate stories with `---`.

Add a brief **header** with the total count and time range:

```
📰 Hacker News — AI & Agent Stories (Past Week)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Showing N stories from the past 7 days.
```

## Notes

- Default to `week` mode unless user asks for "latest"
- If there are many results (>20), show the top 20 and mention total count
- Translate the header to Chinese if the user writes in Chinese
- Keep titles and metadata in original English
