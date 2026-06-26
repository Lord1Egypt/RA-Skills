---
name: oo-pandadoc
description: "PandaDoc (pandadoc.com). Use this skill for ANY PandaDoc request — reading, creating, updating, and deleting data. Whenever a task involves PandaDoc, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "PandaDoc"
  author: "OOMOL"
  version: "1.0.1"
  services: ["pandadoc"]
  icon: "https://static.oomol.com/logo/third-party/PandaDoc.svg"
---

# PandaDoc

Operate **PandaDoc** through your OOMOL-connected account. This skill calls the `pandadoc` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected PandaDoc. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pandadoc" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pandadoc" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_document_attachment` — Upload an attachment file to a draft PandaDoc document. [write]
- `create_document_from_file` — Create a PandaDoc document from a public file URL, a transit file reference, or a local file upload. [write]
- `create_folder` — Create a new document folder in PandaDoc. [write]
- `create_or_update_contact` — Create a PandaDoc contact, or update the existing contact that matches the provided email address. [write]
- `create_template` — Create a PandaDoc template from structured content or from a local PDF upload. [write]
- `create_webhook` — Create a PandaDoc webhook subscription for document lifecycle events. [write]
- `delete_contact` — Delete a contact from the connected PandaDoc workspace. [destructive]
- `delete_template` — Delete a template from the connected PandaDoc workspace. [destructive]
- `get_document_details` — Retrieve detailed metadata for a specific PandaDoc document.
- `get_template_details` — Retrieve detailed metadata for a specific PandaDoc template.
- `list_contacts` — List contacts in the connected PandaDoc workspace, with optional exact email filtering.
- `list_document_folders` — List document folders in the connected PandaDoc workspace.
- `list_templates` — List templates available in the connected PandaDoc workspace.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change PandaDoc state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — PandaDoc is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=pandadoc
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- PandaDoc homepage: https://www.pandadoc.com
