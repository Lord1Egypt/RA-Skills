---
name: meeting-memory
description: Give AI agents Every meeting becomes searchable. using BlueColumn persistent memory. Use when an agent takes meeting notes and needs recall; when the user wants to store, recall, or search meeting memory context. Requires a BlueColumn API key (bc_live_*).
---

# Meeting Memory — BlueColumn Skill

Every meeting becomes searchable.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Meeting 7/30 standup: blockers — staging env down; owner: dev team.", "title": "meeting-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Meeting 7/30 standup: blockers — staging env down; owner: dev team.", "tags": ["meeting-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What action items came out of the last standup?"}'
```

## Workflow
1. On new context, first recall: `What action items came out of the last standup?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
