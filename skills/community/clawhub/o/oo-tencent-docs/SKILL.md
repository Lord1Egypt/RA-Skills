---
name: oo-tencent-docs
description: "Tencent Docs (docs.qq.com). Use this skill for ANY Tencent Docs request — reading, creating, and updating data. Whenever a task involves Tencent Docs, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Tencent Docs"
  author: "OOMOL"
  version: "1.0.4"
  services: ["tencent_docs"]
  icon: "https://static.oomol.com/logo/third-party/tencent_docs.svg"
---

# Tencent Docs

Operate **Tencent Docs** through your OOMOL-connected account. This skill calls the `tencent_docs` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Tencent Docs. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "tencent_docs" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "tencent_docs" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `batch_update_doc` — Apply up to thirty Tencent Docs document V3 batch update operations. [write]
- `batch_update_sheet` — Apply up to five Tencent Docs spreadsheet V3 batch update operations. [write]
- `convert_file_id` — Convert between Tencent Docs fileID and encodedID values.
- `create_file` — Create a Tencent Docs online document, sheet, form, slide, or smart sheet. [write]
- `generate_form_result` — Generate the result spreadsheet for a Tencent Docs form. [write]
- `get_current_user` — Get the current Tencent Docs user profile for the OAuth access token.
- `get_doc_content` — Get the structured content and version of a Tencent Docs document.
- `get_export_progress` — Check a Tencent Docs asynchronous export operation and return the download URL when ready.
- `get_file_metadata` — Get Tencent Docs metadata for one file by file ID.
- `get_sheet_range` — Read cell values and metadata from a Tencent Docs spreadsheet range.
- `list_folder` — List files and folders in a Tencent Docs folder.
- `list_smartsheet_sheets` — List child sheets inside a Tencent Docs Smartsheet file.
- `rename_file` — Rename a Tencent Docs file by file ID. [write]
- `search_files` — Search Tencent Docs files by title keyword or owner nickname.
- `start_export` — Start an asynchronous Tencent Docs file export and return the operation ID. [write]
- `update_form_collection_deadline` — Publish, pause, or update the collection deadline for a Tencent Docs form. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Tencent Docs state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Tencent Docs is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/tencent_docs
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Tencent Docs homepage: https://docs.qq.com
- API documentation: https://docs.qq.com/open/document/
