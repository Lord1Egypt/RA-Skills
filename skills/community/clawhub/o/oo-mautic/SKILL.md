---
name: oo-mautic
description: "Mautic (mautic.org). Use this skill for ANY Mautic request — reading, creating, updating, and deleting data. Whenever a task involves Mautic, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Mautic"
  author: "OOMOL"
  version: "1.0.4"
  services: ["mautic"]
  icon: "https://static.oomol.com/logo/third-party/mautic.svg"
---

# Mautic

Operate **Mautic** through your OOMOL-connected account. This skill calls the `mautic` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Mautic. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mautic" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mautic" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_contact_to_segment` — Manually add a Mautic contact to a segment. [write]
- `create_contact` — Create a Mautic contact using standard or instance-specific custom contact field aliases. [write]
- `delete_contact` — Delete a Mautic contact by numeric contact ID. [destructive]
- `get_contact` — Get a Mautic contact by numeric contact ID.
- `list_contacts` — List Mautic contacts with optional search, pagination, and ordering controls.
- `list_segments` — List Mautic segments with optional search, pagination, and ordering controls.
- `remove_contact_from_segment` — Manually remove a Mautic contact from a segment. [destructive]
- `update_contact` — Update selected fields on an existing Mautic contact without creating a missing contact. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Mautic state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Mautic is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/mautic
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Mautic homepage: https://mautic.org
- API documentation: https://devdocs.mautic.org/en/7.1/rest_api/authentication.html
