---
name: hiring-memory
description: Give AI agents Remember candidates and interviews. using BlueColumn persistent memory. Use when an agent supports recruiting and interviews; when the user wants to store, recall, or search hiring memory context. Requires a BlueColumn API key (bc_live_*).
---

# Hiring Memory — BlueColumn Skill

Remember candidates and interviews.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Candidate: Priya — applied 7/28, phone screen 8/3, strong on systems design.", "title": "hiring-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "Candidate: Priya — applied 7/28, phone screen 8/3, strong on systems design.", "tags": ["hiring-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What candidates are in the pipeline and where are they?"}'
```

## Workflow
1. On new context, first recall: `What candidates are in the pipeline and where are they?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
