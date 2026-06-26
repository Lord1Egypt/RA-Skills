---
name: oo-dropbox
description: "Dropbox (dropbox.com). Use this skill for ANY Dropbox request — reading, creating, updating, and deleting data. Whenever a task involves Dropbox, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Dropbox"
  author: "OOMOL"
  version: "1.0.3"
  services: ["dropbox"]
  icon: "https://static.oomol.com/logo/third-party/Dropbox.svg"
---

# Dropbox

Operate **Dropbox** through your OOMOL-connected account. This skill calls the `dropbox` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Dropbox. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "dropbox" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "dropbox" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `copy` — Copy one file or folder to another Dropbox path. [write]
- `create_folder` — Create one folder in Dropbox. [write]
- `create_shared_link` — Create one Dropbox shared link with optional custom settings. [write]
- `delete` — Delete one file or folder from Dropbox. [destructive]
- `download_file` — Download one Dropbox file and upload it to transit storage.
- `get_current_account` — Get basic profile information for the current Dropbox account.
- `get_metadata` — Get Dropbox metadata for one file or folder.
- `get_shared_link_file` — Download a Dropbox shared-link file and upload it to transit storage.
- `get_shared_link_metadata` — Get metadata for a Dropbox shared link.
- `get_tags` — Get user-generated Dropbox tags for one or more files or folders.
- `get_temporary_link` — Create a temporary direct-download Dropbox link for one file.
- `list_folder` — List files and folders inside one Dropbox folder.
- `list_folder_continue` — Continue a previous Dropbox folder listing with a cursor.
- `list_revisions` — List revisions for one Dropbox file.
- `list_shared_links` — List Dropbox shared links for the current user or a specific path.
- `modify_shared_link` — Modify settings for an existing Dropbox shared link. [write]
- `move` — Move one file or folder to another Dropbox path. [write]
- `restore` — Restore one Dropbox file to a previous revision. [write]
- `revoke_shared_link` — Revoke an existing Dropbox shared link. [destructive]
- `save_url` — Ask Dropbox to save a public URL into a Dropbox file path. [write]
- `save_url_check_job_status` — Check the status of an asynchronous Dropbox save_url job. [write]
- `search_files` — Search Dropbox files and folders with the official search_v2 endpoint.
- `search_files_continue` — Continue a previous Dropbox file search with a cursor.
- `upload_file` — Upload one file to Dropbox from inline text or base64 content. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Dropbox state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Dropbox is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=dropbox
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Dropbox homepage: https://www.dropbox.com
