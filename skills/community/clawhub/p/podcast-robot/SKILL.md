---
name: "podcast-robot"
description: "Talk to the Podcast Robot MCP server (podcastindexrobot.com, a Podcast Index service) for podcast discovery, what's new, people, places, transcript search, shareable clips, live streams, Podping events and feed grading. Use when the user wants anything about podcasts; no API key needed."
---

# Podcast Robot

## Purpose
A zero-setup client for the Podcast Robot MCP server: search podcasts, check what's new in followed
shows, find who was on a show, shows near a place, search episode transcripts, make shareable clip
references, list live streams, read Podping events, grade a podcaster's feed. No API key, no account,
no OAuth. The server is public and stores nothing about the user. Full guide: https://podcastindexrobot.com/llms.txt

## Tooling
`bin/mcp_robot.py` is a minimal JSON-RPC client (Streamable HTTP via curl).

List available tools:
```
bin/mcp_robot.py tools
```

Call a tool (args as JSON):
```
bin/mcp_robot.py call <tool> '<json-args>'
```

Start here (a live menu plus an onboarding checklist):
```
bin/mcp_robot.py call start_here '{}'
```

Search for a show:
```
bin/mcp_robot.py call search_podcasts '{"query": "No Agenda", "mode": "title", "max_results": 3}'
```

Find a moment in a transcript (needs the episode id from get_episodes / whats_new), then clip it:
```
bin/mcp_robot.py call get_episodes '{"feed": "41504", "max_results": 1}'
bin/mcp_robot.py call transcript_search '{"episode": "61124290178", "query": "bitcoin", "max_hits": 2}'
bin/mcp_robot.py call make_clip '{"episode": "61124290178", "start": 4577, "duration": 45}'
```

## Preferences (the server is stateless)
Ask the user once for their podcast app, city, the shows they follow and topics they like; keep the
answers in your own memory and pass them as `prefs` on every call, e.g.
`{"prefs": {"app": "fountain", "city": "Austin", "follows": ["41504"], "language": "en"}}`.
With `prefs.app` set, every show and episode result carries `open.app`, a link that opens in the
user's app. Without it, use `open.universal`.

## Auth
None. The endpoint `https://podcastindexrobot.com/mcp` is open. Do not ask the user for credentials and do not invent any.

## Operating Rules
1. Be polite to a shared hosted endpoint: the limit is 60 calls per minute per IP. When keeping
   watch, pass the time of your last check as `since` (whats_new, podping_events, feed_activity) and
   check at most every 15 minutes.
2. `transcript_search` returns media-fragment play URLs (`#t=start,end`); use `make_clip` for a shareable clip reference.
3. `podping_events` with `resolve: true` adds feedId and title to each event; `contains` filters feed URLs.
4. Every result ends with `hints`: suggested next calls. Offer the user two or three of them.
5. Results with `"kind": "fault"` carry an `errorId`: tell the user it is logged and being fixed, quote the id, retry once.
   Results with `"kind": "input"` are not bugs: follow `whatToTry`, `closestMatches` or `howToAdd`.
6. Never present invented episode details; everything comes from tool output.
