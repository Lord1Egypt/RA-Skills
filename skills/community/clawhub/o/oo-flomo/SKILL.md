---
name: oo-flomo
description: "flomo (flomoapp.com). Use this skill for ANY flomo request — reading, creating, and updating data. Whenever a task involves flomo, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "flomo"
  author: "OOMOL"
  version: "1.0.2"
  services: ["flomo"]
  icon: "https://static.oomol.com/logo/third-party/flomo.png"
---

# flomo

Operate **flomo** through your OOMOL-connected account. This skill calls the `flomo` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected flomo. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "flomo" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "flomo" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_memo` — Create a flomo memo by sending markdown or plain text to the incoming webhook. [write]
- `get_daily_review` — Fetch flomo daily review content through the flomo Max MCP server.
- `get_format_guide` — Fetch flomo memo formatting guidance through the flomo Max MCP server.
- `get_tag_guide` — Fetch flomo tag usage guidance through the flomo Max MCP server.
- `memo_batch_get` — Fetch multiple flomo memos through the flomo Max MCP server in a single tool call.
- `memo_recommended` — Find flomo memos related to a target memo through the flomo Max MCP server.
- `memo_search` — Search flomo memos through the flomo Max MCP server by keywords, tags, time range, or semantic search options.
- `memo_update` — Update an existing flomo memo through the flomo Max MCP server. The exact arguments are validated by flomo MCP. [write]
- `memory_context` — Read the generated flomo memory context through the flomo Max MCP server.
- `memory_user` — Read the generated flomo memory user profile through the flomo Max MCP server.
- `tag_rename` — Rename flomo tags through the flomo Max MCP server and update associated memos. [write]
- `tag_search` — Search flomo tags through the flomo Max MCP server.
- `tag_tree` — Fetch the flomo tag tree through the flomo Max MCP server.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change flomo state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — flomo is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key, custom credential) at:

  ```text
  https://console.oomol.com/app-connections?provider=flomo
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- flomo homepage: https://flomoapp.com
