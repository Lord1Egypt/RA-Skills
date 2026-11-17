---
name: oo-iyunbiao
description: "Yunbiao (iyunbiao.com). Use this skill for ANY Yunbiao request — reading, creating, updating, and deleting data. Whenever a task involves Yunbiao, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Yunbiao"
  author: "OOMOL"
  version: "1.0.3"
  services: ["iyunbiao"]
  icon: "https://static.oomol.com/logo/third-party/iyunbiao.jpg"
---

# Yunbiao

Operate **Yunbiao** through your OOMOL-connected account. This skill calls the `iyunbiao` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Yunbiao. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "iyunbiao" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "iyunbiao" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `batch_save_forms` — Create or update multiple Yunbiao forms. Inspect errorFormList for individual failures even when the request succeeds. [destructive]
- `download_attachment` — Download a Yunbiao attachment to a usable file transit URL. Use the attachment file ID from get_form.
- `download_cloud_file` — Download a Yunbiao enterprise cloud drive file to a usable file transit URL.
- `get_form` — Read a Yunbiao form with its current version, detail rows and attachment references.
- `get_role` — Read a complete Yunbiao role record.
- `get_template_structure` — Get Yunbiao template fields and detail table definitions. Requires server 3.3.45.43 or later.
- `get_user` — Read a complete Yunbiao user record, including roles and posts.
- `list_roles` — List Yunbiao roles, optionally with filtering, sorting and pagination.
- `list_templates` — List available Yunbiao templates. Requires Yunbiao server 3.3.45.43 or later.
- `list_users` — List Yunbiao users, optionally with filtering, sorting and pagination.
- `query_detail_rows` — Query rows in a Yunbiao detail table across forms. Requires server 3.3.45.43 or later.
- `query_forms` — Find Yunbiao forms with filters, sorting and pagination. Use get_form to retrieve full detail rows before editing.
- `query_global_interface` — Call a global Yunbiao data interface. Its configured business logic may modify data. [destructive]
- `query_template_interface` — Call a data interface configured on a Yunbiao template. Its configured business logic may modify data. [destructive]
- `save_form` — Create or update a Yunbiao form. Before updating, read the complete form and preserve its objectId and current objectVersion. [destructive]
- `save_role` — Create or update a Yunbiao role. Read get_role before updating and preserve its fields. [destructive]
- `save_user` — Create or update a Yunbiao user. Read get_user before updating and preserve its fields. Passwords in the user record must already be MD5-encoded. [destructive]
- `upload_attachment` — Upload a file from a URL to Yunbiao, returning an attachment entry to include in save_form. Upload alone does not attach it to a form. Connector upload limit: 64 MiB. [write]
- `upload_cloud_file` — Upload a file from a URL to the Yunbiao enterprise cloud drive. Upload alone does not associate it with a form. Connector upload limit: 64 MiB. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Yunbiao state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Yunbiao is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/iyunbiao
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Yunbiao homepage: https://www.iyunbiao.com
- API documentation: https://docs.iyunbiao.com/openAPI/1
