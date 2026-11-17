---
name: oo-nusii-proposals
description: "Nusii Proposals (nusii.com). Use this skill for ANY Nusii Proposals request — reading, creating, updating, and deleting data. Whenever a task involves Nusii Proposals, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Nusii Proposals"
  author: "OOMOL"
  version: "1.0.5"
  services: ["nusii_proposals"]
  icon: "https://static.oomol.com/logo/third-party/nusii_proposals.svg"
---

# Nusii Proposals

Operate **Nusii Proposals** through your OOMOL-connected account. This skill calls the `nusii_proposals` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Nusii Proposals. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "nusii_proposals" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "nusii_proposals" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `archive_proposal` — Archive a Nusii proposal by ID. [destructive]
- `create_client` — Create a client in the connected Nusii account. [write]
- `create_proposal` — Create a Nusii proposal, optionally resolving a client and copying sections from a template. [write]
- `get_account` — Get the Nusii account associated with the connected API token.
- `get_client` — Get one Nusii client by ID.
- `get_proposal` — Get one Nusii proposal by ID, including any recipient resources Nusii returns.
- `get_template` — Get one Nusii proposal template by ID.
- `list_clients` — List clients in the connected Nusii account with optional pagination.
- `list_proposals` — List Nusii proposals with pagination and optional status, archive, or recipient filters.
- `list_templates` — List account or public Nusii templates with optional pagination.
- `list_themes` — List the proposal themes available in Nusii.
- `list_users` — List Nusii account users for prepared-by and sender selection.
- `send_proposal` — Send a Nusii proposal to one legacy email address or up to 10 structured recipients. [write]
- `update_proposal` — Update one or more documented fields on a Nusii proposal. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Nusii Proposals state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Nusii Proposals is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/nusii_proposals
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Nusii Proposals homepage: https://nusii.com/
- API documentation: https://developer.nusii.com/
