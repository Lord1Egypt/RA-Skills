---
name: oo-finchina
description: "FinChina (mcp.finchina.com). Use this skill for ANY FinChina request — searching and reading data. Whenever a task involves FinChina, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "FinChina"
  author: "OOMOL"
  version: "1.0.2"
  services: ["finchina"]
  icon: "https://static.oomol.com/logo/third-party/finchina.svg"
---

# FinChina

Operate **FinChina** through your OOMOL-connected account. This skill calls the `finchina` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected FinChina. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "finchina" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "finchina" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `discover_tools` — Call a FinChina query_* or screen_* navigation tool with no arguments to obtain subTools and their parameter schemas. This returns definitions, not business records. Use execute_tool to query a discovered subtool.
- `execute_tool` — Query a FinChina data subtool discovered with discover_tools. Pass its exact name and arguments. Queries consume account credits; this action executes one request without automatic pagination or business retries.
- `get_company_basic_info` — Query company basic information and selected indicators through FinChina, such as registered capital. Consumes account credits and executes one query. Discover query_enterprise_profile for the current additional parameters.
- `get_company_financial_metrics` — Query company financial indicators through FinChina, such as revenue over the last three years. Consumes account credits and executes one query. Discover query_enterprise_financial_data for the current additional parameters.
- `get_metadata` — Query FinChina indicator definitions, enumerations, or parameter metadata through caihui_mcp_metadata. Inspect its current schema using list_tools before supplying arguments.
- `list_tools` — Discover FinChina financial and enterprise-risk navigation tools, the execution entry point, and metadata tools with their current input schemas.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change FinChina state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — FinChina is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/finchina
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- FinChina homepage: https://mcp.finchina.com
- API documentation: https://mcp.finchina.com/guide/mcp/tools/api
