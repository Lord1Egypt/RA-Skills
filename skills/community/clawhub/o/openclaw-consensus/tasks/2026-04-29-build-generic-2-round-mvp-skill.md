# Task: Build Generic 2-Round MVP Skill

## Title
Build the first truthful MVP of `openclaw-consensus`

## Date
2026-04-29

## Owner
- Main orchestrator
- Delivery subagent

## Status
- completed

## Objective
Implement the smallest truthful OpenClaw-native MVP for 2-round cross-model deliberation with generic workflow only.

## Outcome
Delivered a real repo-local MVP with:
- `SKILL.md` at repo root
- `src/cli.mjs` runtime for fixed 2-round deliberation
- repo-local install/uninstall scripts
- artifact writing for brief, metadata, round 1, round 2, and final synthesis
- fallback rejection when OpenClaw runs a different model than requested
- captured validation evidence in `validation/2026-04-29/`

## What changed
### Runtime + packaging
- added `package.json`
- added `src/cli.mjs`
- added `SKILL.md`
- added `scripts/install-skill.sh`
- added `scripts/uninstall-skill.sh`
- added `LICENSE`

### Documentation alignment
- updated `README.md`
- updated `docs/COMMANDS.md`
- updated `docs/SKILL_LIFECYCLE.md`
- updated `docs/AI_BOOTSTRAP.md`
- updated `docs/RUNBOOK.md`

### Validation evidence
Added:
- `validation/README.md`
- `validation/2026-04-29/install.log`
- `validation/2026-04-29/uninstall.log`
- `validation/2026-04-29/reinstall-and-skill-info.log`
- `validation/2026-04-29/help-and-models.log`
- `validation/2026-04-29/happy-path-run/`
- `validation/2026-04-29/happy-path-run.log`
- `validation/2026-04-29/happy-path-readback.log`
- `validation/2026-04-29/failure-path-run/`
- `validation/2026-04-29/failure-path-run.log`
- `validation/2026-04-29/failure-path-readback.log`

## Key implementation decisions
- kept the workflow locked to exactly 2 rounds
- required explicit model selection in the CLI
- rejected `ollama/*` models in MVP to preserve the API-backed-only boundary
- used `openclaw config get agents` as the configured-pool source of truth
- treated OpenClaw fallback as a hard failure so the repo never pretends a requested model actually ran
- changed dev install from symlink to guarded copy after proving OpenClaw rejects workspace-skill symlink escapes

## Validation summary
### Install / uninstall / reinstall
- install works
- uninstall works
- reinstall works
- `openclaw skills info openclaw-consensus` shows the skill as ready

### Happy path
Successful run recorded in:
- `validation/2026-04-29/happy-path-run/`
- `validation/2026-04-29/happy-path-readback.log`

Models used:
- `openai-codex/gpt-5.4`
- `openai-codex/gpt-5.5`

### Failure path
Failure recorded in:
- `validation/2026-04-29/failure-path-run/`
- `validation/2026-04-29/failure-path-readback.log`

Failure proved:
- requested `anthropic/claude-sonnet-4-6`
- OpenClaw attempted fallback due provider billing issue
- runtime rejected the fallback and marked the run failed while preserving prior artifacts

## Notes
- Validation used two OpenAI Codex models because Anthropic was configured but not actually usable in this environment due billing fallback.
- The repo remains generic-only and intentionally narrow.
