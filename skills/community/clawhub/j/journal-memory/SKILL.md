---
name: journal-memory
description: Give AI agents Store every thought as searchable memory. using BlueColumn persistent memory. Use when an agent keeps a journal and needs to revisit entries; when the user wants to store, recall, or search journal memory context. Requires a BlueColumn API key (bc_live_*).
---

# Journal Memory — BlueColumn Skill

Store every thought as searchable memory.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Journal 7/31: launched the memory company strategy, feeling good about ClawHub push.", "title": "journal-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Journal 7/31: launched the memory company strategy, feeling good about ClawHub push.", "tags": ["journal-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What did I journal about last week?"}'
```

## Workflow
1. On new context, first recall: `What did I journal about last week?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
