# Changelog

## 1.0.0-beta.6 - 2026-09-17

- Require JianDan CLI `1.0.0-beta.6`; pair with MCP `0.1.0-beta.4`.
- Coordinate shared local authorization across agents and concurrent CLI processes; avoid automatic logout/login repairs.
- Require system asset extraction and deep parsing for every script source; remove manual asset creation from agent workflows.
- Preserve edits and image regeneration for existing parsed assets.
- Clarify that older-client enforcement requires the matching backend deployment; client publication does not deploy the backend.

## 1.0.0-beta.5 - 2026-09-11

- Require JianDan CLI `1.0.0-beta.5` and document reauthorization for expanded brand/material scopes.
- Add script episode replacement, AI verification, version history, and restore workflows.
- Add material-library reads and writes, brand profile management, and manual role/scene creation.
- Document the uploaded-script two-stage asset extraction and parsing workflow.
- Add Seedance 2.5 storyboard generation settings and explicit video-model unlock guidance.
- Add local video attachment and WorkBuddy harness handoff instructions.

## 1.0.0-beta.3 - 2026-08-25

- Publish the first standalone JianDan Agent Skill repository.
- Use browser-based JianDan account authorization only.
- Default to the JianDan production API.
- Support Codex, OpenClaw, and TRAE skill installation paths.
- Add brand association during initial project creation.
- Add uploaded-script asset parsing, storyboard editing, video workflows, and task diagnostics.
- Keep all live writes behind `--confirm` after a matching `--dry-run` preview.
