---
name: oo-treg
description: "Treg (treg.to). Use this skill for ANY Treg request — reading, creating, updating, and deleting data. Whenever a task involves Treg, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Treg"
  author: "OOMOL"
  version: "1.0.0"
  services: ["treg"]
  icon: "https://static.oomol.com/logo/third-party/treg.svg"
---

# Treg

Operate **Treg** through your OOMOL-connected account. This skill calls the `treg` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Treg. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "treg" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "treg" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_tool` — Call a Treg catalog endpoint or registered team tool with JSON parameters. Read catalog_get first and use its method, inputs and price. Calls can modify or delete upstream resources and spend team credits. Only synchronous JSON responses are supported; use URL inputs for remote files where the tool supports them. After a timeout, verify the outcome before retrying. [destructive]
- `catalog_get` — Read a Treg catalog tool's parameters, method, price and examples before calling it.
- `catalog_search` — Search Treg's catalog by task and compare available tools and prices before calling one.
- `get_balance` — Read the connected team's current prepaid Treg balance in integer micro-USD.
- `list_tools` — List the connected team's registered tools that this token is allowed to use.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Treg state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Treg is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/treg
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Treg homepage: https://treg.to
- API documentation: https://github.com/superdesigndev/treg#part-1--using-the-registry
