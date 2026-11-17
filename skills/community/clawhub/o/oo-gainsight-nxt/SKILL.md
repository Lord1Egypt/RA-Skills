---
name: oo-gainsight-nxt
description: "Gainsight NXT (gainsight.com). Use this skill for ANY Gainsight NXT request — reading, creating, updating, and deleting data. Whenever a task involves Gainsight NXT, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Gainsight NXT"
  author: "OOMOL"
  version: "1.0.5"
  services: ["gainsight_nxt"]
  icon: "https://static.oomol.com/logo/third-party/gainsight_nxt.svg"
---

# Gainsight NXT

Operate **Gainsight NXT** through your OOMOL-connected account. This skill calls the `gainsight_nxt` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Gainsight NXT. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "gainsight_nxt" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "gainsight_nxt" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_company` — Delete one Gainsight NXT Company record by its GSID. [destructive]
- `insert_companies` — Insert up to 50 records into the Gainsight NXT Company object using field names from your tenant's Data Management schema. [write]
- `query_companies` — Query Gainsight NXT Company records with selected fields, optional where conditions, sorting, limit, and offset.
- `update_companies` — Update up to 50 Gainsight NXT Company records identified by one to three Company key fields. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Gainsight NXT state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Gainsight NXT is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/gainsight_nxt
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Gainsight NXT homepage: https://www.gainsight.com
- API documentation: https://support.gainsight.com/gainsight_nxt/API_and_Developer_Docs/About/API_Documentation_Overview
