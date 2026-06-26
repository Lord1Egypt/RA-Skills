# Runbook

## Purpose

Operate the mesh plugin on a gateway through controlled actions.

## Step 1: Preflight

Run `preflight` action first and verify:

1. required binaries present
2. caller allowlist set correctly
3. global/per-action gates in expected state

## Step 2: Setup / Repair

Use `setup-ansible-plugin`:

1. install plugin (npm/github/path)
2. run `openclaw ansible setup`
3. verify `openclaw ansible status`

## High-Risk Gate Precedence

1. Global high-risk gate (`OPENCLAW_ALLOW_HIGH_RISK=1`) must be on.
2. Then action-specific gate must be on:
  - `OPENCLAW_ALLOW_RUN_CMD=1` for run-cmd
  - `OPENCLAW_ALLOW_DEPLOY_SKILL=1` for deploy-skill
3. Caller must match `OPENCLAW_ALLOWED_CALLERS`.

## Side Effects

1. No automatic capability registration in mesh state.
2. `deploy-skill` writes to `/opt/openclaw/skills` and requires operator privileges.
