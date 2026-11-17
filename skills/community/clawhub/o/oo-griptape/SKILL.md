---
name: oo-griptape
description: "Griptape (griptape.ai). Use this skill for ANY Griptape request — reading, creating, updating, and deleting data. Whenever a task involves Griptape, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Griptape"
  author: "OOMOL"
  version: "1.0.5"
  services: ["griptape"]
  icon: "https://static.oomol.com/logo/third-party/griptape.svg"
---

# Griptape

Operate **Griptape** through your OOMOL-connected account. This skill calls the `griptape` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Griptape. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "griptape" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "griptape" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `cancel_assistant_run` — Cancel a Griptape Cloud assistant run. [destructive]
- `create_assistant` — Create a Griptape Cloud assistant. [write]
- `create_assistant_run` — Create a run for a Griptape Cloud assistant. [write]
- `delete_assistant` — Delete a Griptape Cloud assistant. [destructive]
- `get_assistant` — Retrieve one Griptape Cloud assistant by ID.
- `get_assistant_run` — Retrieve one Griptape Cloud assistant run by ID.
- `get_organization` — Retrieve one Griptape Cloud organization by ID.
- `list_assistant_events` — List non-streaming events for a Griptape Cloud assistant run.
- `list_assistant_runs` — List runs for a Griptape Cloud assistant.
- `list_assistants` — List Griptape Cloud assistants with optional pagination.
- `list_organizations` — List Griptape Cloud organizations accessible to the API key.
- `update_assistant` — Update a Griptape Cloud assistant. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Griptape state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Griptape is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/griptape
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Griptape homepage: https://www.griptape.ai
- API documentation: https://docs.griptape.ai/stable/griptape-cloud/api/api-reference/
