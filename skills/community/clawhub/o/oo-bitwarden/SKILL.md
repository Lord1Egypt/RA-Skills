---
name: oo-bitwarden
description: "Bitwarden (bitwarden.com). Use this skill for ANY Bitwarden request — searching and reading data. Whenever a task involves Bitwarden, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Bitwarden"
  author: "OOMOL"
  version: "1.0.3"
  services: ["bitwarden"]
  icon: "https://static.oomol.com/logo/third-party/bitwarden.svg"
---

# Bitwarden

Operate **Bitwarden** through your OOMOL-connected account. This skill calls the `bitwarden` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Bitwarden. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "bitwarden" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "bitwarden" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_collection` — Get one Bitwarden organization collection.
- `get_group` — Get one Bitwarden organization group.
- `get_group_member_ids` — List the member IDs associated with one Bitwarden organization group.
- `get_member` — Get one Bitwarden organization member.
- `get_member_group_ids` — List the group IDs associated with one Bitwarden organization member.
- `get_policy` — Get one Bitwarden organization policy by its numeric policy type.
- `get_subscription` — Get the organization's Bitwarden subscription capacity details.
- `list_collections` — List collections in the Bitwarden organization.
- `list_events` — List Bitwarden organization audit events with optional filters and pagination.
- `list_groups` — List groups in the Bitwarden organization.
- `list_members` — List members in the Bitwarden organization.
- `list_policies` — List policies in the Bitwarden organization.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Bitwarden state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Bitwarden is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/bitwarden
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Bitwarden homepage: https://bitwarden.com/
- API documentation: https://bitwarden.com/help/bitwarden-apis/
