---
name: podcast-manager
description: Find, subscribe to, track, and summarize podcast episodes using public RSS feeds and lightweight local tracking files. Use when a user asks to add/manage podcast subscriptions, list new episodes, mark episodes as listened, catch up on a show, or get quick episode summaries/action items.
---

# Podcast Manager

Manage podcast workflows with predictable steps and low token overhead.

## Working Files

Use these workspace files by default:

- `memory/podcasts/subscriptions.json` — list of subscribed shows
- `memory/podcasts/state.json` — per-show progress (last checked, listened episodes)
- `memory/podcasts/notes.md` — summaries and action notes

If files or parent directories do not exist, create them.

## Data Model

Keep `subscriptions.json` as:

```json
{
  "shows": [
    {
      "title": "Example Show",
      "feedUrl": "https://example.com/feed.xml",
      "homepage": "https://example.com",
      "tags": ["ai", "business"]
    }
  ]
}
```

Keep `state.json` as:

```json
{
  "shows": {
    "https://example.com/feed.xml": {
      "lastChecked": "2026-03-12T20:00:00Z",
      "listenedGuids": [],
      "bookmarkedGuids": []
    }
  }
}
```

## Core Workflow

1. Resolve the show and RSS feed URL.
2. Fetch and parse recent episodes from the feed.
3. Compare feed entries with local state.
4. Return a concise update (new/unheard episodes first).
5. Apply requested mutations (subscribe/unsubscribe/listened/bookmark/note).
6. Persist changes in the tracking files.

## Feed Discovery

When feed URL is not provided:

1. Use `web_search` with query format: `"<podcast name> official rss feed"`.
2. Open top candidates with `web_fetch`.
3. Prefer canonical feed URLs from official sites or known podcast hosts.
4. Confirm before subscribing if multiple plausible feeds remain.

## Episode Retrieval Rules

- Parse RSS/Atom entries by stable identifiers in this order: `guid`, `id`, `link`, then `title+pubDate` fallback.
- Normalize publication time to ISO-8601 when possible.
- Keep responses compact: newest 3–10 episodes unless user asks for more.
- When audio URL exists, include it only when requested.

## Commands to Support (Intent-Level)

Handle these intent families:

- Subscribe: add show/feed to `subscriptions.json`
- Unsubscribe: remove show/feed from `subscriptions.json`
- Check updates: list unheard episodes since last check
- Mark listened: add episode guid to `listenedGuids`
- Bookmark: add episode guid to `bookmarkedGuids`
- Catch up summary: summarize N latest unheard episodes
- Show notes/action items: append concise bullets to `memory/podcasts/notes.md`

## Summary Style

For episode summaries:

- Use 3–6 bullets: main topic, key claims, practical takeaways.
- Add a `Questions to revisit` bullet if uncertainty exists.
- Avoid fabricating details; say when metadata is incomplete.

## Error Handling

- If feed is unreachable, report status and keep existing state unchanged.
- If parsing fails, return a short diagnostic and propose one fallback source.
- On ambiguous show matches, ask one disambiguation question with 2–4 options.

## Safety and UX

- Do not auto-subscribe/unsubscribe without explicit user intent.
- Do not expose private local paths unless the user asks.
- Prefer deterministic updates to local files over ephemeral memory.
