---
name: oo-eraser
description: "Eraser (eraser.io). Use this skill for ANY Eraser request — reading, creating, updating, and deleting data. Whenever a task involves Eraser, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Eraser"
  author: "OOMOL"
  version: "1.0.5"
  services: ["eraser"]
  icon: "https://static.oomol.com/logo/third-party/eraser.svg"
---

# Eraser

Operate **Eraser** through your OOMOL-connected account. This skill calls the `eraser` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Eraser. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "eraser" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "eraser" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `archive_file` — Archive an Eraser file. [destructive]
- `create_diagram` — Create a diagram from Eraser DSL inside an existing file. [write]
- `create_file` — Create an Eraser file with optional Markdown content. [write]
- `delete_diagram` — Delete a diagram from an Eraser file. [destructive]
- `generate_diagram_from_dsl` — Render Eraser DSL into a diagram image and optional editable Eraser file. [write]
- `generate_diagram_from_prompt` — Generate or revise an Eraser diagram from a natural-language prompt. [write]
- `get_diagram` — Get one diagram from an Eraser file.
- `get_file` — Get an Eraser file and its current content.
- `list_diagrams` — List diagrams contained in an Eraser file.
- `list_files` — List files available to the authenticated Eraser team.
- `update_diagram` — Replace the Eraser DSL source of a diagram in a file. [destructive]
- `update_file` — Replace selected metadata or Markdown content of an Eraser file. [destructive]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Eraser state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Eraser is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/eraser
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Eraser homepage: https://www.eraser.io
- API documentation: https://docs.eraser.io/reference/getting-started
