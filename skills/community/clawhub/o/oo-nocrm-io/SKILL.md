---
name: oo-nocrm-io
description: "noCRM.io (nocrm.io). Use this skill for ANY noCRM.io request — reading, creating, updating, and deleting data. Whenever a task involves noCRM.io, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "noCRM.io"
  author: "OOMOL"
  version: "1.0.1"
  services: ["nocrm_io"]
  icon: "https://static.oomol.com/logo/third-party/NoCRM.io.svg"
---

# noCRM.io

Operate **noCRM.io** through your OOMOL-connected account. This skill calls the `nocrm_io` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected noCRM.io. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "nocrm_io" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "nocrm_io" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_tag_to_lead` — Add one or more tags to a noCRM.io lead. [write]
- `append_to_lead_description` — Append text to the description of a noCRM.io lead.
- `assign_lead_to_user` — Assign a noCRM.io lead to a specific user. [write]
- `change_lead_status_to_cancelled` — Change a noCRM.io lead status to cancelled.
- `change_lead_status_to_standby` — Change a noCRM.io lead to standby and schedule its next reminder.
- `create_lead` — Create a lead in noCRM.io with the provided title and description. [write]
- `delete_lead` — Delete a noCRM.io lead. [destructive]
- `duplicate_lead` — Duplicate an existing noCRM.io lead into another step. [write]
- `list_teams` — List the teams available in the connected noCRM.io account.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change noCRM.io state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — noCRM.io is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=nocrm_io
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- noCRM.io homepage: https://www.nocrm.io
