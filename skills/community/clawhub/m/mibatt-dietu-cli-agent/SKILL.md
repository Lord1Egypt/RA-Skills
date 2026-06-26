---
name: mibatt-dietu-cli-agent
description: Use this skill when you need to operate Dietu through its official CLI for A-share market queries, strategy screening, decision workflows, or agent automation. Covers GitHub device flow login, PAT usage, output formats, and stable command recipes.
metadata:
  short-description: Operate Dietu CLI for A-share workflows
---

# Dietu CLI Agent

Use this skill when the task should be completed through the official `dietu` CLI instead of web UI clicks or backend-only scripts.

Typical fit:

- Query A-share market overviews, stock snapshots, indices, or search results
- Run strategy lists and screening commands
- Pull decision, trading, and review data from Dietu
- Set up CLI authentication for human users or automation
- Produce machine-readable CLI output for another agent or script

## Base URL

Default API endpoint: `https://dietu-api.mibatt.com`

Override via `--base-url`, `DIETU_BASE_URL`, or profile config.

## Quick rules

- Prefer the public CLI package: `npm i -g @mibatt/dietu@latest`
- For human login, use `dietu auth login`
- For automation, prefer a PAT in `DIETU_ACCESS_TOKEN`
- For agent consumption, prefer `--format json`
- For user-facing pasted output, prefer `--format markdown`
- For quick terminal inspection, prefer `--format table`
- Use real `ts_code` symbols such as `600519.SH` or `000001.SZ`
- If you do not know the command surface, run `dietu schema`
- If connectivity or auth looks suspicious, run `dietu doctor`

## Authentication

Read [references/auth.md](references/auth.md) when the task involves login, token sourcing, base URL switching, or PAT usage.

Important:

- The primary interactive path is GitHub device flow
- The recommended automation path is PAT from `Settings / Access Tokens`
- Do not invent outdated commands such as `dietu ping` or `dietu mcp start`

## Command recipes

Read [references/commands.md](references/commands.md) when you need concrete command sequences for:

- market
- research
- decision
- trading
- review
- schema and doctor

## Working style

- Start with the smallest command that can answer the task
- Add `--format json` before doing downstream parsing or summarization
- Preserve the user's chosen `--base-url`, `--profile`, or token source
- For commands that require an account, explicitly provide `--account <id>`
- If the task spans multiple CLI calls, keep outputs structured and consistent

## Non-goals

- Do not call internal Python scripts as the primary interface when the CLI already exposes the capability
- Do not assume browser-only login or password login is the preferred path
- Do not treat short-lived JWT copied from local profile as the recommended long-term automation credential
