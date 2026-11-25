---
name: oo-metabase
description: "Metabase (metabase.com). Use this skill for ANY Metabase request — reading, creating, updating, and deleting data. Whenever a task involves Metabase, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Metabase"
  author: "OOMOL"
  version: "1.0.7"
  services: ["metabase"]
  icon: "https://static.oomol.com/logo/third-party/metabase.svg"
---

# Metabase

Operate **Metabase** through your OOMOL-connected account. This skill calls the `metabase` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Metabase. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "metabase" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "metabase" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_tool` — Call a native Metabase MCP tool with JSON arguments matching the inputSchema returned by list_tools with toolNames. Depending on the tool, this can run queries or create, update, or archive Metabase content as the API key's user; check the tool's annotations and confirm writes first. [destructive]
- `get_card` — Retrieve one Metabase card by ID.
- `get_collection` — Retrieve one Metabase collection by ID.
- `get_current_user` — Get the Metabase user associated with the API key.
- `get_dashboard` — Retrieve one Metabase dashboard by ID.
- `get_database` — Retrieve one Metabase database by ID.
- `list_cards` — List Metabase cards, also known as questions.
- `list_collections` — List Metabase collections visible to the API key.
- `list_dashboards` — List Metabase dashboards visible to the API key.
- `list_databases` — List Metabase databases visible to the API key.
- `list_mcp_resources` — Discover native MCP resources. Data resources can be read with read_mcp_resource; MCP Apps (ui://) resources are not supported.
- `list_tools` — Discover the tools exposed by this Metabase instance's native MCP server. Without toolNames, returns a compact index (name, one-line summary, annotations); pass toolNames to get the full descriptions and input schemas of those tools before calling them with call_tool. Tool names and schemas follow the instance's Metabase version.
- `read_mcp_resource` — Read a text resource listed by list_mcp_resources. MCP Apps (ui://) resources are not supported.
- `search` — Search Metabase content visible to the API key.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Metabase state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Metabase is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/metabase
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Metabase homepage: https://www.metabase.com
- API documentation: https://www.metabase.com/docs/latest/api
