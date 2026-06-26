---
name: hn-morning-brief
metadata: {"openclaw":{"emoji":"📰","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}
description: >
  Use this skill when the user explicitly mentions Hacker News or HN — e.g. "what's
  on HN", "show me Hacker News", "top HN stories", "anything good on HN today", or
  "dive deeper into this HN story". Do not activate for general tech news requests
  that don't mention HN or Hacker News.
---

## Morning Briefing

### Step 1 — Pull user interests from memory

```
memory_search("interests topics preferences technology news")
```

Do this first, before fetching stories — the results determine how stories are ranked. Extract any topics, technologies, or themes found. If nothing relevant comes back, fall back to HN ranking order.

### Step 2 — Fetch top HN stories

```bash
python3 skills/hn-morning-brief/scripts/fetch_hn.py --limit 20
```

(Path is relative to the project root — openclaw installs this skill at `skills/hn-morning-brief/`.)

Returns JSON with: `title`, `article_url`, `hn_url`, `domain`, `author`, `points`, `num_comments`.

### Step 3 — Rank and filter

Score each story by combining two signals:
- **Relevance to user interests** (from memory) — a story the user cares about is worth more regardless of score
- **HN points** — use as a tiebreaker and quality signal when interests are unclear

Surface the 8–12 highest-scoring stories. If memory search returned no clear interests, rank by `points` only.

### Step 4 — Present briefing

```
## HN Morning Brief — {today's date}

{N} stories picked for you

1. **{Title}** `{domain}` · ⬆ {points} · 💬 {num_comments}
   {one-line context or why this is interesting}
   → [Article]({article_url}) · [HN Discussion]({hn_url})

2. ...

---
Say "dive deeper into #N" or "tell me more about [title]" to get a full summary.
```

---

## Diving Deeper

When the user picks a story:

1. **Fetch and summarize the article** — read the article URL and write a 3–5 sentence summary of the key points. Do this even if the user just says "more on #3" — they want the content, not just the link.
2. **Show both links:**
   - Article: `{article_url}`
   - HN Discussion: `{hn_url}` (often where the most interesting debate happens)
3. **Offer to go further:** "Want me to search for more context on this?"

## Gotchas

- `article_url` is the **original article**. `hn_url` is the HN discussion thread. Never swap them — linking to the HN page when the user wants the article is a bad experience.
- If the article is a PDF or appears paywalled, say so and summarize from the title, domain, and any available description instead of silently failing.
- If `memory_search` returns no clear interests, rank by `points` and don't guess — invented interests will surface irrelevant stories.
