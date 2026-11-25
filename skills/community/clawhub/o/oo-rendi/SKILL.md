---
name: oo-rendi
description: "Rendi (rendi.dev). Use this skill for ANY Rendi request — reading, creating, updating, and deleting data. Whenever a task involves Rendi, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Rendi"
  author: "OOMOL"
  version: "1.0.0"
  services: ["rendi"]
  icon: "https://static.oomol.com/logo/third-party/rendi.svg"
---

# Rendi

Operate **Rendi** through your OOMOL-connected account. This skill calls the `rendi` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Rendi. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "rendi" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "rendi" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_command_files` — Delete all stored output files belonging to one command. [destructive]
- `delete_file` — Delete one stored file from Rendi storage. [destructive]
- `delete_files` — Delete up to 1000 stored files. Output manifest files cannot be deleted with this endpoint; use delete_command_files for those outputs. [destructive]
- `get_command` — Get a regular or chained FFmpeg command status and output files, optionally with signed private download URLs.
- `get_file` — Get a stored file or command output with FFprobe metadata. Deleted files retain metadata with a null storage_url; private files can return signed download URLs.
- `list_commands` — List FFmpeg commands newest first, with status and processing metrics. Use get_command for output files.
- `list_files` — List stored and command output files newest first, excluding deleted and input files.
- `run_chained_ffmpeg_commands` — Submit up to 10 sequential FFmpeg commands sharing files. A later command can read an earlier output with -i {{out_alias}}. Retrieve outputs with get_command. [write]
- `run_ffmpeg_command` — Submit an FFmpeg command with media URLs or a ZIP URL. Use {{in_alias}} and {{out_alias}} placeholders; omit the ffmpeg executable. Retrieve outputs with get_command. [write]
- `store_file` — Ask Rendi to download a media URL, analyze it with FFprobe and store it. Retrieve its metadata and download URL with get_file. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Rendi state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Rendi is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/rendi
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Rendi homepage: https://www.rendi.dev/
- API documentation: https://www.rendi.dev/docs/api-reference/introduction
