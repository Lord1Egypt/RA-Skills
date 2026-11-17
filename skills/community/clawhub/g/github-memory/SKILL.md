---
name: github-memory
description: Give AI agents Remember GitHub issues and PRs. using BlueColumn persistent memory. Use when an agent tracks repos, issues, and pull requests; when the user wants to store, recall, or search github memory context. Requires a BlueColumn API key (bc_live_*).
---

# Github Memory — BlueColumn Skill

Remember github issues and prs.. Powered by BlueColumn (bluecolumn.ai) persistent vector memory.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Store
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "PR #88: adds recall streaming. Reviewers: Alex, Sam. Merged 7/29.", "title": "github-memory - note"}'
```

## Quick note
```bash
curl -X POST .../agent-note \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"text": "PR #88: adds recall streaming. Reviewers: Alex, Sam. Merged 7/29.", "tags": ["github-memory"]}'
```

## Recall
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"q": "What PRs are waiting on review?"}'
```

## Workflow
1. On new context, first recall: `What PRs are waiting on review?`
2. Use the answer to personalize the response
3. After the interaction, store the summary via `/agent-remember`

## Docs
Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
