---
name: oo-magileads
description: "Magileads (magileads.com). Use this skill for ANY Magileads request — reading, creating, updating, and deleting data. Whenever a task involves Magileads, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Magileads"
  author: "OOMOL"
  version: "1.0.4"
  services: ["magileads"]
  icon: "https://static.oomol.com/logo/third-party/magileads.svg"
---

# Magileads

Operate **Magileads** through your OOMOL-connected account. This skill calls the `magileads` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Magileads. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "magileads" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "magileads" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_contact_list` — Create a Magileads contact list with optional tags, folder, language, and country metadata. [write]
- `delete_contact_list` — Delete one Magileads contact list by identifier. [destructive]
- `get_contact_list` — Get the profile and metadata of one Magileads contact list by identifier.
- `list_contact_lists` — List all Magileads contact lists available to the authenticated account, including shared lists.
- `update_contact_list` — Update the metadata of one Magileads contact list by identifier. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Magileads state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Magileads is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/magileads
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Magileads homepage: https://www.magileads.com/
- API documentation: https://api.magileads.net/
