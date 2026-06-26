---
name: oo-docsumo
description: "Docsumo (docsumo.com). Use this skill for ANY Docsumo request — reading, creating, and updating data. Whenever a task involves Docsumo, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Docsumo"
  author: "OOMOL"
  version: "1.0.1"
  services: ["docsumo"]
  icon: "https://static.oomol.com/logo/third-party/docsumo.svg"
---

# Docsumo

Operate **Docsumo** through your OOMOL-connected account. This skill calls the `docsumo` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Docsumo. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "docsumo" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "docsumo" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_account_info` — Get Docsumo account details, monthly document quota usage, and the currently enabled document types.
- `get_document_detail` — Get Docsumo document detail metadata for one document, including page information and preview assets.
- `get_documents_summary` — Get the Docsumo documents summary grouped by document type, including disabled types and status counts.
- `get_extracted_data` — Get the simplified extracted Docsumo data for one document and preserve the dynamic section and field structure.
- `list_documents` — List Docsumo documents with optional folder, type, status, search, sorting, and created-date filters.
- `upload_document_from_url` — Upload one public file URL to Docsumo for a chosen document type and return the queued document metadata. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Docsumo state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Docsumo is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=docsumo
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Docsumo homepage: https://www.docsumo.com
