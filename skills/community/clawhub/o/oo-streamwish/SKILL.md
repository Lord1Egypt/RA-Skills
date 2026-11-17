---
name: oo-streamwish
description: "StreamWish (streamwish.com). Use this skill for ANY StreamWish request — reading, creating, updating, and deleting data. Whenever a task involves StreamWish, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "StreamWish"
  author: "OOMOL"
  version: "1.0.2"
  services: ["streamwish"]
  icon: "https://static.oomol.com/logo/third-party/streamwish.svg"
---

# StreamWish

Operate **StreamWish** through your OOMOL-connected account. This skill calls the `streamwish` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected StreamWish. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "streamwish" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "streamwish" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `clone_file` — Clone a file into the account. [write]
- `create_folder` — Create a folder. [write]
- `delete_file` — Delete a file from the account. [destructive]
- `edit_file` — Update file metadata; omitted fields are not changed. [write]
- `edit_folder` — Update a folder; omitted fields are not changed. [write]
- `get_account` — Get account details and storage usage.
- `get_account_stats` — Get daily account statistics.
- `get_direct_link` — Get direct video URLs and optional HLS manifest URL.
- `get_file_info` — Get metadata for one or more files, including per-file status.
- `list_files` — List files with filters and page-based pagination.
- `list_folders` — List child folders and optionally their files.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change StreamWish state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — StreamWish is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/streamwish
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- StreamWish homepage: https://streamwish.com
- API documentation: https://streamwish.com/api.html
