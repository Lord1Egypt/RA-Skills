---
name: oo-eversign
description: "Xodo Sign (eversign.com). Use this skill for ANY Xodo Sign request — reading, creating, updating, and deleting data. Whenever a task involves Xodo Sign, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Xodo Sign"
  author: "OOMOL"
  version: "1.0.5"
  services: ["eversign"]
  icon: "https://static.oomol.com/logo/third-party/eversign.svg"
---

# Xodo Sign

Operate **Xodo Sign** through your OOMOL-connected account. This skill calls the `eversign` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Xodo Sign. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "eversign" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "eversign" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_document` — Create a Xodo Sign document from public file URLs or existing Xodo Sign file IDs. [write]
- `create_document_from_template` — Create a Xodo Sign document from an existing template, role assignments, and merge fields. [write]
- `get_audit_log` — Retrieve the complete audit event history for a Xodo Sign document.
- `get_document` — Retrieve a Xodo Sign document or template by its document hash.
- `list_businesses` — List businesses available to the connected Xodo Sign API key.
- `list_documents` — List Xodo Sign documents for a business, optionally filtering by documented status.
- `list_templates` — List active, archived, or draft Xodo Sign templates for a business.
- `reassign_signer` — Replace a signer on a Xodo Sign document and notify the affected participants. [destructive]
- `send_reminder` — Send a reminder to one signer of a Xodo Sign document. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Xodo Sign state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Xodo Sign is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/eversign
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Xodo Sign homepage: https://eversign.com/
- API documentation: https://eversign.com/api/documentation/methods
