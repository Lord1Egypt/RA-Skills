---
name: ansible-skills-admin
description: "Manage ansible skill lifecycle across gateways: source-of-truth edits, mirror sync, deployment verification, and drift cleanup."
---

# Ansible Skills Admin

Use this skill when the user asks to create, update, deploy, or reconcile ansible skill content across canonical and runtime locations.

## Source-of-Truth Policy

- Canonical repo in `~/code` is the golden source.
- Runtime mirrors in `~/.openclaw/workspace/skills/*` are deploy targets.
- Never leave runtime-only edits unpromoted unless explicitly requested.

## Standard Workflow

1. Edit canonical skill repo first.
2. Commit and push canonical changes.
3. Pull to runtime mirrors (local and VPS).
4. Verify mirror parity.
5. Restart gateway only if runtime requires reload.

## Required Checks

- Canonical clean state:
  - `git -C ~/code/openclaw-skill-ansible status -b --short`
- Runtime mirror parity:
  - `git -C ~/.openclaw/workspace/skills/ansible rev-parse --short HEAD`
- VPS mirror parity:
  - `ssh jane-vps "docker exec jane-gateway sh -lc 'git -C /home/node/.openclaw/workspace/skills/ansible rev-parse --short HEAD'"`

## Drift Triage

If runtime mirror differs from canonical:

- If change is intentional and useful, port to canonical repo and commit.
- If change is accidental, reset runtime mirror to canonical HEAD.
- Re-verify local and VPS mirrors after remediation.

## Human Visibility Requirement

When deploying skill changes, send lifecycle updates:

- `ACK` when rollout starts
- `IN_PROGRESS` at each gateway update
- `DONE` or `BLOCKED` with verification evidence

Use `conversation_id` for all related updates.
