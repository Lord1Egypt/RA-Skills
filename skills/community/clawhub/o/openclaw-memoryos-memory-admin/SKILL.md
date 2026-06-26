---
name: openclaw-memoryos-memory-admin
description: Inspect, back up, search, export, and update OpenClaw long-term memory stored with MemoryOS. Use when Codex needs to manage MemoryOS memory files for an OpenClaw-style agent, including locating the data directory, reading user profiles, reviewing user or assistant knowledge, appending curated memories, replacing profiles, exporting summaries, or preparing MemoryOS-based long-term memory operations for another agent project.
---

# OpenClaw MemoryOS Memory Admin

Manage OpenClaw long-term memory by operating directly on MemoryOS storage files and by following the MemoryOS data model used in `long_term_user.json` and `long_term_assistant.json`.

Use the bundled script for deterministic operations. Read the reference file only when you need to confirm the on-disk layout or explain how MemoryOS maps user profile, user knowledge, and assistant knowledge.

## Quick Start

Prefer `scripts/memoryos_admin.py` over ad hoc edits.

Common commands:

```powershell
python scripts/memoryos_admin.py summary --data-root "D:\path\to\memoryos_data" --user-id alice --assistant-id openclaw
python scripts/memoryos_admin.py search-user --data-root "D:\path\to\memoryos_data" --user-id alice --query "project preference"
python scripts/memoryos_admin.py add-user-knowledge --data-root "D:\path\to\memoryos_data" --user-id alice --text "User prefers concise technical answers."
python scripts/memoryos_admin.py set-profile --data-root "D:\path\to\memoryos_data" --user-id alice --profile-file ".\profile.txt"
python scripts/memoryos_admin.py backup --data-root "D:\path\to\memoryos_data" --user-id alice --assistant-id openclaw
```

## Workflow

Follow this order unless the user asks for a narrower task:

1. Locate the MemoryOS data root used by the OpenClaw integration.
2. Run `summary` to inspect current profile and knowledge counts.
3. Run `backup` before any mutating action.
4. Use `search-user` or `search-assistant` to verify whether the target memory already exists.
5. Use `add-user-knowledge`, `add-assistant-knowledge`, or `set-profile` for intentional updates.
6. Use `export-markdown` when the user wants a readable audit or handoff artifact.

## Data Rules

Treat these files as the authoritative long-term memory state:

- `users/<user_id>/long_term_user.json`
- `assistants/<assistant_id>/long_term_assistant.json`

Interpret them this way:

- `user_profiles.<user_id>.data`: current synthesized user profile
- `knowledge_base[]`: user-specific long-term knowledge entries
- `assistant_knowledge[]`: assistant-side reusable knowledge entries

Preserve existing timestamps unless you are explicitly adding or replacing content.

Do not hand-edit embeddings. The bundled admin script stores and updates records without embeddings on purpose, because this skill is for memory administration, curation, backup, and inspection. Semantic retrieval inside live MemoryOS runtime can rebuild or add embeddings through normal MemoryOS flows when needed.

## Mutation Guidance

Use `set-profile` only when the user wants to replace the synthesized profile with a curated version.

Use `add-user-knowledge` for durable facts about the user, preferences, identity, recurring tasks, or persistent context that OpenClaw should remember.

Use `add-assistant-knowledge` for workflow instructions, project background, house rules, or reusable operational knowledge that belongs to the assistant rather than the user.

Before appending a near-duplicate memory, search first and ask whether the old entry should be kept, replaced manually, or left unchanged if the instruction is ambiguous.

## OpenClaw Integration Notes

If OpenClaw is not present in the workspace, treat OpenClaw as the consuming agent and MemoryOS as the storage backend. The critical integration contract is the MemoryOS `data_storage_path` and the chosen `user_id` plus `assistant_id`.

When wiring another agent project to MemoryOS:

- keep a stable `user_id` per person
- keep a stable `assistant_id` per OpenClaw persona or deployment
- point the agent to the same `data_storage_path`
- back up memory files before schema or workflow changes

## References

Read `references/memoryos-layout.md` when you need exact file layout and field names.
