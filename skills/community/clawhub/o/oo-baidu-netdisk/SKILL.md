---
name: oo-baidu-netdisk
description: "Baidu Netdisk (pan.baidu.com). Use this skill for ANY Baidu Netdisk request — reading, creating, updating, and deleting data. Whenever a task involves Baidu Netdisk, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Baidu Netdisk"
  author: "OOMOL"
  version: "1.0.7"
  services: ["baidu_netdisk"]
  icon: "https://static.oomol.com/logo/third-party/baidu_netdisk.png"
---

# Baidu Netdisk

Operate **Baidu Netdisk** through your OOMOL-connected account. This skill calls the `baidu_netdisk` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Baidu Netdisk. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "baidu_netdisk" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "baidu_netdisk" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `copy` — Synchronously copy one Baidu Netdisk file or folder. [write]
- `create_folder` — Create one folder at an absolute path below the user's Baidu Netdisk root. [write]
- `create_share_link` — Create one Baidu Netdisk share link for one or more files or folders. [write]
- `create_text_file` — Create one UTF-8 text file through Baidu MCP. [write]
- `download_file` — Download one Baidu Netdisk file and upload it to connector transit storage.
- `get_current_account` — Get the current Baidu Netdisk account and membership summary.
- `get_quota` — Get total, used, remaining, free, and expiring Baidu Netdisk capacity.
- `list_files` — List all files and folders, or only documents, images, or videos, from the user's Baidu Netdisk root.
- `move` — Synchronously move one Baidu Netdisk file or folder. [destructive]
- `rename` — Synchronously rename one Baidu Netdisk file or folder. [write]
- `search_files` — Search files and folders below an absolute Baidu Netdisk directory.
- `semantic_search_files` — Search Baidu Netdisk using a natural-language description.
- `upload_file_from_url` — Ask Baidu Netdisk to fetch one public URL into an absolute destination path. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Baidu Netdisk state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Baidu Netdisk is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/baidu_netdisk
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Baidu Netdisk homepage: https://pan.baidu.com
- API documentation: https://pan.baidu.com/union/doc/
