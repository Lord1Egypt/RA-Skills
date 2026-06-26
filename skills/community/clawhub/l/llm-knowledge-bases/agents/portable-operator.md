# Portable Operator Instructions

Use these instructions for any MCP-capable agent that should operate an `LLM Knowledge Bases` vault.

Core model:

- the runtime owns Vault I/O, IDs, paths, validation, state, and generated navigation
- the agent owns understanding, synthesis, Q&A, and deciding which wiki pages should exist
- every meaningful interaction should improve the wiki, not only produce a chat answer

Preferred actions:

- `ingest-source`
- `ask-and-file`
- `maintain-wiki`
- `map-gaps`

Non-negotiable boundaries:

- never modify files under `raw/`
- never write directly into `wiki/` with generic file tools
- never fabricate note ids, hashes, or `source_refs`
- never claim a write succeeded unless the MCP tool confirmed it

Preferred tool order:

- ingest (text/data): `kb_status` -> `kb_list_raw` -> `kb_prepare_source` -> `kb_read_raw` -> `kb_upsert_source_note` -> `kb_rebuild_indexes`
- ingest (pdf/image): `kb_status` -> `kb_list_raw` -> `kb_prepare_source_bundle` -> `kb_get_raw_asset` -> `kb_prepare_representation` -> `kb_upsert_representation` -> `kb_read_representations` -> `kb_upsert_source_note` -> `kb_rebuild_indexes`
- answer: `kb_search` -> `kb_read_notes` -> answer -> `kb_upsert_output` or `kb_upsert_derived_note`
- maintain: `kb_lint` -> `kb_read_notes` -> optional `kb_repair_source_ids` when source ids or manifest/source-note metadata drifted -> targeted fixes -> `kb_rebuild_indexes`
- gap mapping: `kb_search` -> `kb_read_notes` -> `kb_map_gaps` -> optional `kb_promote_gap`
