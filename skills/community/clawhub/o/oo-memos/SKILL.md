---
name: oo-memos
description: "Memos (usememos.com). Use this skill for ANY Memos request — reading, creating, updating, and deleting data. Whenever a task involves Memos, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Memos"
  author: "OOMOL"
  version: "1.0.5"
  services: ["memos"]
  icon: "https://static.oomol.com/logo/third-party/memos.webp"
---

# Memos

Operate **Memos** through your OOMOL-connected account. This skill calls the `memos` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Memos. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "memos" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "memos" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_memo` — Create a Markdown memo on the connected Memos instance. [write]
- `delete_attachment` — Delete one attachment by resource name. [destructive]
- `delete_memo` — Delete one memo, optionally forcing deletion when associated data exists. [destructive]
- `get_attachment` — Retrieve one attachment's metadata by resource name.
- `get_current_user` — Retrieve the Memos user associated with the connected personal access token.
- `get_memo` — Retrieve one memo by its Memos resource name.
- `get_user` — Retrieve one Memos user by resource name.
- `list_attachments` — List attachment metadata with pagination, filtering, and ordering.
- `list_memo_attachments` — List attachments associated with one memo.
- `list_memos` — List memos with pagination, state selection, ordering, and CEL filtering.
- `list_users` — List users visible to the connected Memos account.
- `set_memo_attachments` — Replace the complete attachment set associated with one memo. [destructive]
- `update_memo` — Update selected content, visibility, pin, state, time, or location fields on a memo. [write]
- `upload_attachment` — Download a public file URL and upload its bytes to the connected Memos instance. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Memos state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Memos is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/memos
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Memos homepage: https://usememos.com
- API documentation: https://usememos.com/docs/api/latest
