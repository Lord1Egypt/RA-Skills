---
name: oo-callingly
description: "Callingly (callingly.com). Use this skill for ANY Callingly request — reading, creating, updating, and deleting data. Whenever a task involves Callingly, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Callingly"
  author: "OOMOL"
  version: "1.0.0"
  services: ["callingly"]
  icon: "https://static.oomol.com/logo/third-party/callingly.svg"
---

# Callingly

Operate **Callingly** through your OOMOL-connected account. This skill calls the `callingly` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Callingly. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "callingly" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "callingly" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_call` — Create a Callingly call from lead details and routing information. [write]
- `delete_lead` — Delete a Callingly lead by ID. [destructive]
- `get_agent_schedule` — Retrieve the weekly schedule for one Callingly agent. [write]
- `get_call` — Retrieve one Callingly call by ID.
- `get_lead` — Retrieve one Callingly lead by ID.
- `get_team` — Retrieve one Callingly team by ID.
- `list_agents` — List Callingly agents for the current account or a specified client account.
- `list_calls` — List Callingly calls with optional date, team, and pagination filters.
- `list_leads` — List Callingly leads with optional date or phone number filters.
- `list_team_agents` — List agents assigned to one Callingly team.
- `list_teams` — List Callingly teams for the current account or a specified client account.
- `update_lead` — Update a Callingly lead by ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Callingly state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Callingly is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=callingly
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Callingly homepage: https://callingly.com
