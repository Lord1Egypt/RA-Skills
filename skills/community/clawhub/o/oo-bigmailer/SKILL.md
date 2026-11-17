---
name: oo-bigmailer
description: "BigMailer (bigmailer.io). Use this skill for ANY BigMailer request — reading, creating, updating, and deleting data. Whenever a task involves BigMailer, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "BigMailer"
  author: "OOMOL"
  version: "1.0.5"
  services: ["bigmailer"]
  icon: "https://static.oomol.com/logo/third-party/bigmailer.svg"
---

# BigMailer

Operate **BigMailer** through your OOMOL-connected account. This skill calls the `bigmailer` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected BigMailer. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "bigmailer" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "bigmailer" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_contact` — Create a contact in a BigMailer brand. [write]
- `create_list` — Create a contact list in a BigMailer brand. [write]
- `delete_contact` — Delete a BigMailer contact by ID or email address. [destructive]
- `delete_list` — Delete a BigMailer contact list without deleting its contacts. [destructive]
- `get_brand` — Get one BigMailer brand by ID.
- `get_contact` — Get one BigMailer contact by ID or email address.
- `get_list` — Get one BigMailer contact list by ID.
- `list_brands` — List brands in the BigMailer account.
- `list_contacts` — List contacts in a BigMailer brand, optionally filtered by list.
- `list_lists` — List contact lists in a BigMailer brand.
- `update_contact` — Update a BigMailer contact by ID or email address. [write]
- `update_list` — Update a BigMailer contact list name. [write]
- `upsert_contact` — Create or update a BigMailer contact by email address. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change BigMailer state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — BigMailer is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/bigmailer
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- BigMailer homepage: https://www.bigmailer.io/
- API documentation: https://docs.bigmailer.io/
