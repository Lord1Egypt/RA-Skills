# Marrow MCP quick reference

Use the existing `@getmarrow/mcp` tools directly.

## Core decision loop

- `marrow_orient` — run at session start to surface warnings, recent failure patterns, and `shouldPause`
- `marrow_think` — log intent before a complex action and get pattern intelligence plus loop detection
- `marrow_commit` — record the result of the action tied to a prior `decision_id`
- `marrow_run` — one-call orient + think + commit for a completed action
- `marrow_auto` — lightweight fire-and-forget logging, recommended default for most actions
- `marrow_ask` — query decision history in plain English before unfamiliar or risky work
- `marrow_status` — check Marrow platform health

## Memory tools

- `marrow_list_memories` — list memories with filters
- `marrow_get_memory` — fetch a single memory by id
- `marrow_update_memory` — edit memory text, tags, or metadata
- `marrow_delete_memory` — soft-delete a memory
- `marrow_mark_outdated` — mark a memory outdated
- `marrow_supersede_memory` — replace a memory with a new version
- `marrow_share_memory` — share a memory with selected agents
- `marrow_export_memories` — export memories as JSON or CSV
- `marrow_import_memories` — import memories with merge or replace mode
- `marrow_retrieve_memories` — full-text search memories with filters

## Workflow tools

- `marrow_workflow` — register, list, inspect, start, and advance multi-step workflows

## Practical defaults

- Start every session with `marrow_orient`
- Use `marrow_auto` before and after normal actions
- Use `marrow_think` and `marrow_commit` for multi-step work or when outcomes matter
- Use `marrow_ask` when you do not trust your first guess
