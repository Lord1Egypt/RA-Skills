---
name: oo-appgrowing-mcp
description: "AppGrowing Global MCP (appgrowing.net). Use this skill for ANY AppGrowing Global MCP request — reading, creating, updating, and deleting data. Whenever a task involves AppGrowing Global MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "AppGrowing Global MCP"
  author: "OOMOL"
  version: "1.0.2"
  services: ["appgrowing_mcp"]
  icon: "https://static.oomol.com/logo/third-party/appgrowing_mcp.svg"
---

# AppGrowing Global MCP

Operate **AppGrowing Global MCP** through your OOMOL-connected account. This skill calls the `appgrowing_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected AppGrowing Global MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "appgrowing_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "appgrowing_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_tool` — Call any current AppGrowing Global MCP tool after inspecting list_tools. Arguments must match the live schema. Calls may consume AppGrowing credits; inspect behavior annotations before invoking newly added tools. [destructive]
- `creativeAIAnalysisData` — Read narration, selling points and AI analysis for up to 100 creative resources. Pair each resource ID with one of its ad format IDs.
- `creativeResourceUrl` — Refresh expired creative download links using the resource filenames, including their extensions.
- `creativeSellingPointTrends` — Compare selling-point trends for games and apps by category, style and country.
- `filterOptions` — List the advertising filters available to your AppGrowing account. Business queries consume account credits.
- `list_tools` — Discover current AppGrowing Global MCP tools, live argument schemas and behavior annotations for advertising creative, app, publisher and developer research.
- `searchAdCreatives` — Find global advertising creatives by product, audience and campaign filters. Use filterOptions for valid IDs and page to continue through results.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change AppGrowing Global MCP state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — AppGrowing Global MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/appgrowing_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- AppGrowing Global MCP homepage: https://appgrowing.net/
- API documentation: https://docs.appgrowing.net/mcp/installation/
