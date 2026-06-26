---
name: la-local-chat
description: Operate and improve the La Local location-management chat product. Use when reviewing or changing the frontend chat app, backend webhook, search behavior, media upload flow, Notion/Dropbox integration, deployment topology, or project-specific product logic for La Local.
---

# La Local Chat

Operate and improve the La Local chat product with one guiding rule:
- treat **search** as the main area for AI-assisted improvement
- keep **create/update** deterministic, explicit, and safe

## Core behavior

### Search
- Search by name, description, and relevant location context.
- Return up to 5 real matches.
- Never invent locations.
- Prefer structured retrieval and ranking over freeform generation.
- Improve relevance before adding sophistication.

### Create
- Ask for the location name first.
- Create the Notion record immediately.
- Use the Notion-generated ID as the Dropbox folder reference.
- Continue field gathering in a guided flow.

### Update
- Update by name or ID.
- Confirm the target record when ambiguity exists.
- Prefer deterministic field handling over freeform model behavior.

## Working rules
- Preserve `thread_id` in chat and upload flows.
- Treat Notion as the source of truth for the record.
- Keep Dropbox folder linkage tied to the Notion ID.
- Prefer incremental, testable changes over rewrites.
- Do not regress create/update flows while improving search.

## References
- Read `references/architecture.md` for the current system shape.
- Read `references/search-notes.md` when working on search quality or ranking behavior.
