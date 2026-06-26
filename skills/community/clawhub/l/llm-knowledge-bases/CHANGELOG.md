# Changelog

## 1.2.2 - 2026-04-06

- Add stronger natural-language routing and compact Chinese one-line prompts for common wiki workflows.

## 1.2.1 - 2026-04-05

- Document and ship deterministic repair for legacy src-untitled source ids.

## 1.2.0 - 2026-04-05

- Updated the skill docs for runtime `0.4.0` and its representation-first multimodal ingest model
- Added `kb_get_raw_asset`, `kb_prepare_source_bundle`, `kb_prepare_representation`, `kb_upsert_representation`, and `kb_read_representations` to the documented tool surface
- Added `kb_repair_source_ids` to the documented runtime and maintenance surface so source-id drift can be repaired deterministically
- Clarified the split between direct text/data ingest and PDF/image ingest that must go through stored representations first
- Documented multimodal grounding expectations around `raw_kind`, `mime_type`, `asset_paths`, visible review notes, and the new lint warnings for missing or stale representation trails

## 1.1.4 - 2026-04-05

- Added `kb_promote_gap` so a current gap candidate can be promoted straight into a real derived note
- Refactored the docs so map-gaps can either return refined drafts or land the best current candidate immediately

## 1.1.3 - 2026-04-05

- Upgraded `kb_map_gaps` again so each candidate now includes a suggested opening and evidence summary inside the draft payload
- Clarified in the docs that map-gaps outputs are meant to be refined into near-ready derived notes

## 1.1.2 - 2026-04-05

- Upgraded `kb_map_gaps` from a plain candidate report into a curation assistant with priorities and ready-to-fill Markdown drafts
- Clarified in the skill docs that map-gaps should feed directly into `kb_upsert_derived_note`

## 1.1.1 - 2026-04-05

- Added `kb_map_gaps` to the documented runtime surface
- Updated the skill and agent prompts to treat gap mapping as a first-class workflow
- Clarified how the wiki should identify the next missing concept, entity, and synthesis pages

## 1.1.0 - 2026-04-05

- Repositioned the skill around a wiki-first operating model instead of a runtime-first three-action story
- Added first-class support in the docs and agent prompts for `concept`, `entity`, and `synthesis` pages
- Expanded the recommended vault layout to include `wiki/concepts/`, `wiki/entities/`, `wiki/syntheses/`, `wiki/index.md`, and `wiki/log.md`
- Reframed the canonical workflows as `ingest-source`, `ask-and-file`, `maintain-wiki`, and `map-gaps`
- Updated the scaffold script to create the new wiki directories and generated navigation placeholders

## 1.0.9 - 2026-04-05

- Repositioned the skill around the standalone CLI/MCP runtime instead of describing the product as OpenClaw-first
- Updated README, release notes, and operator prompts to treat OpenClaw as one compatible host alongside Claude Code, Codex, Cursor, and Gemini CLI
- Bumped ClawHub publish metadata to match the new standalone runtime story

## 1.0.8 - 2026-04-04

- Added a Claude Code MCP install path so the same `kb_*` contract can be used outside the OpenClaw host
- Added a reusable Claude Code subagent prompt that carries over the skill's compile, ask, and lint workflow rules
- Added a Codex `AGENTS.md` template plus a portable operator guide for other MCP-capable agents
- Added a multi-agent config helper path for Codex, Cursor, and Gemini CLI
- Updated the README and package metadata to document the cross-agent installation path
