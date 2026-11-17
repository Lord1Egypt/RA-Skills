---
name: oo-granola
description: "Granola (granola.ai). Use this skill for ANY Granola request — searching and reading data. Whenever a task involves Granola, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Granola"
  author: "OOMOL"
  version: "1.0.4"
  services: ["granola"]
  icon: "https://static.oomol.com/logo/third-party/granola.svg"
---

# Granola

Operate **Granola** through your OOMOL-connected account. This skill calls the `granola` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Granola. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "granola" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "granola" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_meeting_transcript` — Read a Granola meeting transcript with OAuth or an API key. Requires an eligible paid Granola plan.
- `get_meetings` — Read Granola meeting details and summaries by ID with OAuth or an API key. Use IDs returned for the same connection. Free-plan OAuth access covers personal notes from the last 30 days.
- `get_note` — Get a Granola note and summary by ID with OAuth or an API key, optionally including the transcript on eligible paid plans. Use an ID returned for the same connection.
- `list_folders` — List accessible Granola folders with OAuth or an API key and cursor pagination. MCP folder access requires a paid plan and uses local pagination of the returned list.
- `list_meetings` — List recent Granola meetings with OAuth or an API key. OAuth uses MCP's last-30-days window; API keys list notes created in the last 30 days. Use get_meetings to read summaries.
- `list_notes` — List Granola notes with OAuth or an API key. MCP lists meetings from the last 30 days and supports folder filtering and local cursor pagination. Creation and update filters require an API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Granola state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Granola is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/connections/granola
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Granola homepage: https://www.granola.ai
- API documentation: https://docs.granola.ai/introduction
