---
name: oo-deepgram
description: "Deepgram (deepgram.com). Use this skill for ANY Deepgram request — searching and reading data. Whenever a task involves Deepgram, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Deepgram"
  author: "OOMOL"
  version: "1.0.1"
  services: ["deepgram"]
  icon: "https://static.oomol.com/logo/third-party/deepgram.svg"
---

# Deepgram

Operate **Deepgram** through your OOMOL-connected account. This skill calls the `deepgram` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Deepgram. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "deepgram" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "deepgram" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_model` — Get metadata for one public Deepgram model.
- `get_project` — Get details for one Deepgram project.
- `get_project_model` — Get metadata for one model available to a Deepgram project.
- `list_models` — List the latest public Deepgram models.
- `list_project_balances` — List the outstanding balances for a Deepgram project.
- `list_project_keys` — List the API keys associated with a Deepgram project.
- `list_project_models` — List the models available to a specific Deepgram project.
- `list_projects` — List the Deepgram projects available to the current API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Deepgram state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Deepgram is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=deepgram
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Deepgram homepage: https://deepgram.com/
