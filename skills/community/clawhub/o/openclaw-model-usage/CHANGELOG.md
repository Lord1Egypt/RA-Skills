# Changelog

All notable changes to `openclaw-model-usage` will be documented in this file.

## 1.2.1

- clarify README and skill guidance so real dashboards use `~/.openclaw/agents` by default
- explicitly mark `tests/fixtures_root` as development-only to avoid sending sample dashboards by mistake
- align installed skill guidance with the shipped summary + dashboard workflow

## 1.2.0

- add human-friendly `overview`, `top-agents`, and `top-sessions` commands on top of the session-aware backend
- make the default non-JSON output compact and ranked for operator/chat use while preserving JSON output for scripting
- expand smoke coverage for the new summary UX and aliases
- refresh README examples toward the new default workflow
- add a local-first `dashboard` command that writes a responsive self-contained HTML usage report
- improve dashboard presentation with friendlier session names and a cleaner mobile-friendly daily cost trend section
- support the intended flow of short summary first, HTML dashboard second

## 1.1.0

- add Phase 1 session-aware attribution by joining usage rows with OpenClaw session metadata
- add `sessions`, `subagents`, and `session-tree` views
- enrich row output with session/subagent metadata such as session key, label, parent linkage, channel, and spawn depth
- improve fallback attribution from session-log subagent context when index metadata is incomplete
- update docs and smoke coverage for session/subagent analysis

