---
name: cli
description: >
  Use this skill whenever the user wants to work with the Nudgen CLI from the
  terminal. This includes browser-based login, identity checks, team context
  management, brand config commands, contacts, campaigns, stats, referral
  analytics, and JSON output automation. Trigger on phrases like "nudgen CLI",
  "nudgen login", "nudgen teams switch", "nudgen contacts list", "nudgen
  campaigns", "nudgen stats", "nudgen referral", or any request to operate
  Nudgen from shell commands.
metadata:
  version: 1.0.0
---

# Nudgen CLI Skill

Use this skill for terminal-first Nudgen workflows. It is focused on operating the existing `nudgen` CLI, not app-level API integration design.

## When To Use

Use this skill when the user needs to:

- authenticate to `nudgen` from terminal
- manage active team context
- run contacts, campaigns, stats, brand, and referral commands
- inspect output in text or `--json`
- troubleshoot CLI auth/config behavior

If the user is writing backend integration code or needs exact HTTP payload design, use the separate `api` skill.

## When Not To Use

Do not use this skill when the task is:

- implementing Nudgen API calls in application/backend code
- designing email strategy or deliverability policy
- requesting product behavior that is not available via current CLI commands

## Working Style

When this skill is active:

1. Prefer `nudgen --help` and command-specific help for exact flags and latest shape.
2. Use browser callback login flow for auth: `nudgen login`.
3. Prefer `--json` when output feeds scripts or other agents.
4. Confirm active team context before team-scoped operations.
5. Avoid printing secrets. PAT storage is keychain-backed.
6. Be explicit when a command exists but is still placeholder behavior.
7. Prefer non-interactive commands (`--json`) when output is consumed by scripts/agents.

## Current Command Surface

- Top-level:
  - `nudgen login`
  - `nudgen logout`
  - `nudgen whoami`
  - `nudgen teams ...`
  - `nudgen brand ...`
  - `nudgen contacts ...`
  - `nudgen campaigns ...`
  - `nudgen stats`
  - `nudgen referral ...`
  - `nudgen version`

- Implemented as placeholders (not complete behavior):
  - `nudgen campaigns create`
  - `nudgen campaigns update <campaign-id>`
  - `nudgen contacts import`
  - `nudgen teams update <team-id>`

## Category Routing

- Auth flow, command groups, team context, JSON mode, and placeholder command caveats:
  Read `references/cli.md`

## Output Checklist

Aim to leave the user with:

- the exact `nudgen` command(s) to run
- active-team caveats when relevant
- safe credential handling reminders
- a concrete validation step (for example `nudgen whoami` or a list command with `--json`)
