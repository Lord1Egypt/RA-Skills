---
name: oo-one-drive
description: "OneDrive (microsoft.com). Use this skill for ANY OneDrive request — reading, creating, updating, and deleting data. Whenever a task involves OneDrive, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "OneDrive"
  author: "OOMOL"
  version: "1.0.1"
  services: ["one_drive"]
  icon: "https://static.oomol.com/logo/third-party/OneDrive.svg"
---

# OneDrive

Operate **OneDrive** through your OOMOL-connected account. This skill calls the `one_drive` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected OneDrive. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "one_drive" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "one_drive" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_folder` — Create a folder in OneDrive. [write]
- `delete_item` — Delete a drive item from OneDrive and move it to the recycle bin. [destructive]
- `download_file` — Download one file from OneDrive by item ID and upload it to transit storage.
- `download_file_by_path` — Download one file from OneDrive by path and upload it to transit storage.
- `download_item_as_format` — Download one drive item after converting it to a supported Microsoft Graph format.
- `get_drive` — Get metadata for the current drive or a specific drive.
- `get_item` — Get metadata for a drive item by item ID or path.
- `get_root` — Get metadata for the root folder of the current drive or a specific drive.
- `list_folder_children` — List the direct children of a folder in OneDrive.
- `search_items` — Search OneDrive for files and folders by keyword.
- `update_file_content` — Replace the content of one existing OneDrive file. [write]
- `update_item_metadata` — Rename, move, or update metadata for a drive item. [write]
- `upload_file` — Upload one file to OneDrive, optionally creating destination folders on the way. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change OneDrive state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — OneDrive is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=one_drive
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- OneDrive homepage: https://www.microsoft.com/microsoft-365/onedrive/online-cloud-storage
