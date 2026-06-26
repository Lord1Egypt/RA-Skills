---
name: oo-vectorshift
description: "VectorShift (vectorshift.ai). Use this skill for ANY VectorShift request — searching and reading data. Whenever a task involves VectorShift, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "VectorShift"
  author: "OOMOL"
  version: "1.0.1"
  services: ["vectorshift"]
  icon: "https://static.oomol.com/logo/third-party/vectorshift.png"
---

# VectorShift

Operate **VectorShift** through your OOMOL-connected account. This skill calls the `vectorshift` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected VectorShift. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "vectorshift" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "vectorshift" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `bulk_run_pipeline` — Run multiple instances of the same VectorShift pipeline with JSON-safe inputs in one request.
- `get_pipeline` — Fetch one VectorShift pipeline by pipeline ID or by pipeline name.
- `list_pipelines` — List VectorShift pipelines that are accessible to the connected API key.
- `run_pipeline` — Run one VectorShift pipeline with JSON-safe inputs and return the resulting outputs.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change VectorShift state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — VectorShift is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=vectorshift
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- VectorShift homepage: https://vectorshift.ai
