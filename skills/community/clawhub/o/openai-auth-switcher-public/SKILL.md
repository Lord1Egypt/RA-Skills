---
name: openai-auth-switcher-public
description: Web-first, publishable OpenClaw skill for OpenAI OAuth account switching. Use when you need a reusable public-track workflow for first-run takeover, environment discovery, doctor checks, runtime inspection, slot management, dry-run validation, controlled switch experiments, rollback planning, and release-safe packaging without bundling live auth snapshots, logs, callbacks, or other machine-specific runtime data.
---

# OpenAI Auth Switcher Public

Use this skill as the **publishable public-track release** of the OpenAI auth switcher workflow.

It is designed for OpenClaw administrators who want a **web-first, first-run-friendly, release-safe** workflow for OpenAI OAuth account takeover, inspection, dry-run validation, controlled switching, and public distribution.

## Purpose

Keep the live/internal operator skill and the public distributable skill separated.

This public track must:

- avoid bundling live runtime state
- avoid bundling auth snapshots, callbacks, backups, or token ledgers from a real machine
- avoid machine-specific hard-coded paths where possible
- document compatibility boundaries explicitly
- provide a release-safe packaging workflow
- keep temporary runtime files inside the skill runtime area, while encouraging important persistent state to live in an external state base via `OPENAI_AUTH_SWITCHER_PUBLIC_STATE_DIR`

## Core operating model

Treat OpenClaw OpenAI OAuth switching as a high-sensitivity maintenance workflow.

Always do work in this order:

1. Use `install.sh` as the default user-facing bootstrap entrypoint.
2. Run `doctor.py` when installation or environment checks fail.
3. Confirm runtime discovery with `env_detect.py`.
4. Inspect the current runtime before any switch logic.
5. Dry-run any target before proposing a write.
6. Keep rollback and backup behavior explicit.
7. Package only from this public skill directory or from a sanitized staging copy.

## Included scripts

Primary public-release scripts:

- `install.sh` — recommended user entrypoint; wraps the web bootstrap into a single shell command
- `uninstall.sh` — recommended cleanup entrypoint before `clawhub uninstall`
- `scripts/install_web_app.py` — one-shot web bootstrap for first-run access
- `scripts/pick_port.py` — port selection helper (`9527` → `12138` → fallback)
- `scripts/generate_web_credentials.py` — default admin credential generator
- `scripts/doctor.py` — compatibility and environment checks
- `scripts/env_detect.py` — OpenClaw path and runtime discovery
- `scripts/paths.py` — centralized path resolution helpers
- `scripts/inspect_runtime.py` — portable runtime inspection
- `scripts/profile_slot.py` — public-safe slot metadata and local slot files
- `scripts/rollback_experiment.py` — rollback helper using explicit backup sources
- `scripts/switch_experiment.py` — controlled switch experiment with backup and rollback
- `scripts/token_ledger.py` — local token attribution ledger rebuild
- `scripts/hourly_usage.py` — hourly/daily rollup payload for local analytics
- `scripts/package_public_skill.py` — release-safe packager wrapper

Helper modules:

- `scripts/auth_file_lib.py`
- `scripts/probe_lib.py`
- `scripts/lock_lib.py`
- `scripts/state_lib.py`

## Compatibility and safety references

Read only as needed:

- `references/compatibility.md` — Python / Node / OpenClaw / OS expectations
- `references/runtime-discovery.md` — path detection and override model
- `references/install-and-runbook.md` — operator flow and first-run checks
- `references/security-model.md` — sensitivity, boundaries, and redaction rules
- `references/packaging-policy.md` — publish checklist and forbidden contents
- `references/migration-notes.md` — relation to the internal/live skill

## Release rule

Do not publish `skills/openai-auth-switcher` directly.

Use the public skill directory for ClawHub publication and use a packaging wrapper that rejects runtime data, backups, session callbacks, and credential-bearing files.

Recommended first release positioning:

- version: `0.1.0`
- tested on OpenClaw `2026.3.11`
- tested on Python `3.11`
- tested on Node.js `22.x`
- Linux-first release
