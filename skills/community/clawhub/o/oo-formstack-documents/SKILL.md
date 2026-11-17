---
name: oo-formstack-documents
description: "Formstack Documents (forms.formstack.com). Use this skill for ANY Formstack Documents request — reading, creating, updating, and deleting data. Whenever a task involves Formstack Documents, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Formstack Documents"
  author: "OOMOL"
  version: "1.0.4"
  services: ["formstack_documents"]
  icon: "https://static.oomol.com/logo/third-party/formstack_documents.svg"
---

# Formstack Documents

Operate **Formstack Documents** through your OOMOL-connected account. This skill calls the `formstack_documents` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Formstack Documents. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "formstack_documents" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "formstack_documents" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `copy_document` — Create a named copy of a Formstack Documents template. [write]
- `create_document` — Create a Formstack Documents template from HTML or a public file URL. [write]
- `delete_document` — Delete a Formstack Documents template by its document ID. [destructive]
- `get_document` — Get one Formstack Documents template by its document ID.
- `get_document_fields` — List merge fields detected in a Formstack Documents template.
- `list_documents` — List Formstack Documents templates, optionally filtered by search text or folder.
- `update_document` — Update mutable fields or source content for a Formstack Documents template. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Formstack Documents state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Formstack Documents is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/formstack_documents
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Formstack Documents homepage: https://forms.formstack.com/products/documents
- API documentation: https://www.webmerge.me/developers
