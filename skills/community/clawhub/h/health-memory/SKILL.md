---
name: health-memory
description: Give AI agents Remember health and fitness goals. using BlueColumn persistent memory. Use when an agent tracks health habits and goals; when the user wants to store, recall, or search health memory context. Requires a BlueColumn API key (bc_live_*).
---

# Health Memory — BlueColumn Skill

Remember health and fitness goals.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Goal: 10k steps/day. 7/31: 9,200 steps, streak 6 days.", "title": "health-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Goal: 10k steps/day. 7/31: 9,200 steps, streak 6 days.", "tags": ["health-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "How am I tracking against my health goals?"}'
```

## Workflow
1. On new context, first recall: `How am I tracking against my health goals?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
