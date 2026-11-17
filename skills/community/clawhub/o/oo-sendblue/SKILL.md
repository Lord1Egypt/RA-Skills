---
name: oo-sendblue
description: "Sendblue (sendblue.com). Use this skill for ANY Sendblue request — reading, creating, updating, and deleting data. Whenever a task involves Sendblue, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sendblue"
  author: "OOMOL"
  version: "1.0.2"
  services: ["sendblue"]
  icon: "https://static.oomol.com/logo/third-party/sendblue.svg"
---

# Sendblue

Operate **Sendblue** through your OOMOL-connected account. This skill calls the `sendblue` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sendblue. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sendblue" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sendblue" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `bulk_create_contacts` — Create multiple Sendblue contacts and return successful contacts and any per-contact failures. [write]
- `bulk_delete_contacts` — Delete multiple Sendblue contacts by phone number and return deletion counts. [destructive]
- `count_contacts` — Count Sendblue contacts, optionally filtered by phone number.
- `create_contact` — Create a Sendblue contact, optionally updating an existing contact with the same number. [write]
- `delete_contact` — Delete a Sendblue contact by phone number. [destructive]
- `get_contact` — Retrieve a Sendblue contact by phone number.
- `list_contacts` — List Sendblue contacts with offset pagination, phone or identity filters, and sorting.
- `set_contact_opt_out` — Set a Sendblue contact's messaging opt-out preference, or opt the contact back in. [write]
- `update_contact` — Update a Sendblue contact. Tags replace the full set; custom variables merge with existing values. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sendblue state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sendblue is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/sendblue
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Sendblue homepage: https://www.sendblue.com/
- API documentation: https://docs.sendblue.com/
