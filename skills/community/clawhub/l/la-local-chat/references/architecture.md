# Architecture

## Product
La Local is a chat-style system for searching, creating, and updating audiovisual locations.

## Current stack
### Frontend
- Repo: `GatoNegroIaLAB/lalocal-chat`
- Deploy: Vercel
- Role: UI + proxy/BFF

### Backend
- Repo: `GatoNegroIaLAB/lalocal-webhook`
- Runtime: EasyPanel / AWS
- Role: chat orchestration, uploads, create/update flows, Notion integration, Dropbox integration, history

## Architecture rules
- Preserve `thread_id` through proxied chat and upload flows.
- Treat Notion as the source of truth.
- Tie Dropbox folder creation to the Notion-generated ID.
- Keep create/update deterministic.
- Focus AI improvement effort primarily on search.
