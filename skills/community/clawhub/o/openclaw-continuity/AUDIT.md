# Audit Guide

This repository is the public V2 package for `personal-hooks`, an OpenClaw
skill for structured continuity, tracking, and follow-up.

It is:

- an OpenClaw skill package
- a state-backed continuity and follow-up layer
- host-neutral at the core package boundary

It is not:

- a one-click full host distribution
- a generic transport or polling package
- an always-on idle/social nudging package by default

## One-line status

Public package identity is V2. Publication should be judged against
`docs/release-acceptance.md` and the current V2 validation set.

For current release state, read:

- `docs/v2-status.md`
- `docs/v2-validation-summary.md`
- `docs/v2-known-limits.md`
- `docs/release-acceptance.md`

## What the public V2 package covers

- routing between `casual_chat`, `staged_memory`, and `tracked_followup`
- four tracked event types:
  - `parked_topic`
  - `watchful_state`
  - `delegated_task`
  - `sensitive_event`
- incremental `event_chain` updates
- structured `causal_memory`
- `candidate -> incident -> hook` promotion
- `/new` carryover and continuity reattach
- active hook / closure lifecycle
- sleep/rest suppress
- dedupe / cooldown / dispatch cap
- frontstage guard and outbound stopgap integration points
- regression harness and live QA guidance

## What the public V2 package does not claim

- default idle/social rhythm nudging
- channel/network delivery reliability
- host-specific transport glue
- persona ownership

## Experimental or opt-in areas

- `experimental.rhythm_nudge.*`
- design-only notes under `docs/v2-blueprint.md`

## Recommended review order

1. `README.md`
2. `SKILL.md`
3. `config.schema.json`
4. `docs/call-flow.md`
5. `docs/harness.md`
6. `docs/release-acceptance.md`
7. `scripts/personal_hooks.py`

## Important file map

Core package files:

- `README.md`
- `SKILL.md`
- `config.schema.json`
- `scripts/personal_hooks.py`
- `scripts/followup_skill_harness.py`
- `scripts/web_live_runner.mjs`

Supporting documentation:

- `docs/call-flow.md`
- `docs/harness.md`
- `docs/live-qa-runbook.md`
- `docs/release-acceptance.md`
- `docs/v2-blueprint.md`

Reference material:

- `references/modules.md`
- `references/templates.md`

Examples:

- `examples/settings.sample.json`
- `examples/harness-report.sample.json`

## Minimal verification

```bash
python3 scripts/personal_hooks.py init
python3 scripts/personal_hooks.py capability-state-show
python3 scripts/followup_skill_harness.py --absence-minutes 3
```

For sandbox isolation, see `docs/harness.md`.

## Current package-level limits

- frontstage warmth and personality still depend on the host agent/model
- carryover remains intentionally short and structured, not full transcript replay
- host glue for live heartbeat / outbound interception remains opt-in
