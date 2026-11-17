---
name: marketing-memory
description: Give AI agents Remember campaigns and results. using BlueColumn persistent memory. Use when an agent runs marketing and needs campaign history; when the user wants to store, recall, or search marketing memory context. Requires a BlueColumn API key (bc_live_*).
---

# Marketing Memory — BlueColumn Skill

Remember campaigns and results.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Campaign: ClawHub skills launch. Goal: 100 installs. Metrics 7/31: 12 installs, 4 bookmarks.", "title": "marketing-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Campaign: ClawHub skills launch. Goal: 100 installs. Metrics 7/31: 12 installs, 4 bookmarks.", "tags": ["marketing-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "How are our marketing campaigns performing?"}'
```

## Workflow
1. On new context, first recall: `How are our marketing campaigns performing?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
