---
name: oo-artificial-analysis
description: "Artificial Analysis (artificialanalysis.ai). Use this skill for ANY Artificial Analysis request — searching and reading data. Whenever a task involves Artificial Analysis, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Artificial Analysis"
  author: "OOMOL"
  version: "1.0.2"
  services: ["artificial_analysis"]
  icon: "https://static.oomol.com/logo/third-party/artificial_analysis.svg"
---

# Artificial Analysis

Operate **Artificial Analysis** through your OOMOL-connected account. This skill calls the `artificial_analysis` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Artificial Analysis. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "artificial_analysis" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "artificial_analysis" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_model` — Get one language model's evaluations, pricing and performance. Requires Pro or Commercial.
- `get_model_performance` — Get language model performance over time, grouped by API provider. Requires Commercial.
- `get_provider` — Get an API provider and its language model pricing and performance. Requires Commercial.
- `get_provider_measurements` — Get raw model measurements for an API provider. Requires Commercial and an explicit provider grant. Dates earlier than one month ago are clamped by the API.
- `get_provider_performance` — Get an API provider's performance over time, grouped by model. Requires Commercial.
- `list_free_models` — List public language model benchmarks, median performance and input/output prices. Available to every API tier; returns the Free field set even with a paid key.
- `list_models` — List language model evaluations, pricing and performance with the full paid field set. Requires Pro or Commercial; use list_free_models with a Free key.
- `list_providers` — List language model API providers. Requires Commercial.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Artificial Analysis state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Artificial Analysis is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/artificial_analysis
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Artificial Analysis homepage: https://artificialanalysis.ai
- API documentation: https://artificialanalysis.ai/data-api/docs
