---
name: oo-nyne-ai
description: "Nyne.ai (nyne.ai). Use this skill for ANY Nyne.ai request — reading, creating, and updating data. Whenever a task involves Nyne.ai, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Nyne.ai"
  author: "OOMOL"
  version: "1.0.5"
  services: ["nyne_ai"]
  icon: "https://static.oomol.com/logo/third-party/nyne_ai.png"
---

# Nyne.ai

Operate **Nyne.ai** through your OOMOL-connected account. This skill calls the `nyne_ai` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Nyne.ai. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "nyne_ai" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "nyne_ai" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_company_enrichment` — Poll a Nyne.ai company enrichment request and return its status plus completed company result.
- `get_company_search` — Poll a Nyne.ai company search request and return its status plus completed result page.
- `get_person_enrichment` — Poll a Nyne.ai person enrichment request and return its status plus completed profile result.
- `get_person_search` — Poll a Nyne.ai person search request and return its status plus completed result page.
- `get_usage` — Get Nyne.ai credit usage, monthly allocation, remaining balance, and per-API breakdown.
- `submit_company_enrichment` — Submit an asynchronous Nyne.ai company enrichment request from domain, email, phone, or social URL. [write]
- `submit_company_search` — Submit an asynchronous Nyne.ai company search using a natural-language query. [write]
- `submit_person_enrichment` — Submit an asynchronous Nyne.ai person enrichment request from email, phone, social URL, or name. [write]
- `submit_person_search` — Submit an asynchronous Nyne.ai people search using a natural-language query or structured filters. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Nyne.ai state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Nyne.ai is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/nyne_ai
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Nyne.ai homepage: https://nyne.ai
- API documentation: https://api.nyne.ai/documentation/authentication
