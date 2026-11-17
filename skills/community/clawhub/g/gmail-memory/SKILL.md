---
name: gmail-memory
description: Give AI agents Remember Gmail threads. using BlueColumn persistent memory. Use when an agent manages email and needs thread history; when the user wants to store, recall, or search gmail memory context. Requires a BlueColumn API key (bc_live_*).
---

# Gmail Memory — BlueColumn Skill

Remember gmail threads.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Thread w/ vendor: quote sent 7/28, awaiting PO.", "title": "gmail-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Thread w/ vendor: quote sent 7/28, awaiting PO.", "tags": ["gmail-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What's the latest in my thread with the vendor?"}'
```

## Workflow
1. On new context, first recall: `What's the latest in my thread with the vendor?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
