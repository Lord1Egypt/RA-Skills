---
name: oo-hex
description: "Hex (hex.tech). Use this skill for ANY Hex request — reading, creating, and updating data. Whenever a task involves Hex, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Hex"
  author: "OOMOL"
  version: "1.0.0"
  services: ["hex"]
  icon: "https://static.oomol.com/logo/third-party/hex.svg"
---

# Hex

Operate **Hex** through your OOMOL-connected account. This skill calls the `hex` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Hex. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "hex" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "hex" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_run` — Cancel an in-progress Hex project run. [write]
- `get_project` — Get metadata for a single Hex project by project ID.
- `get_run_status` — Get the status and metadata for a specific Hex project run.
- `list_project_runs` — List API-triggered runs for a Hex project, optionally filtered by status.
- `list_projects` — List Hex projects visible to the connected token, with pagination and common project filters.
- `run_project` — Trigger a run of the latest published version of a Hex project.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Hex state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Hex is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=hex
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Hex homepage: https://hex.tech
