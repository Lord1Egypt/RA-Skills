---
name: home-memory
description: Give AI agents Remember household context. using BlueColumn persistent memory. Use when an agent manages home tasks and maintenance; when the user wants to store, recall, or search home memory context. Requires a BlueColumn API key (bc_live_*).
---

# Home Memory — BlueColumn Skill

Remember household context.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "HVAC filter due Aug 15. Landlord email on file.", "title": "home-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "HVAC filter due Aug 15. Landlord email on file.", "tags": ["home-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What home maintenance is coming due?"}'
```

## Workflow
1. On new context, first recall: `What home maintenance is coming due?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
