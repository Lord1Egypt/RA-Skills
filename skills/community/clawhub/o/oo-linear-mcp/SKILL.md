---
name: oo-linear-mcp
description: "Linear MCP (linear.app). Use this skill for ANY Linear MCP request — reading, creating, and updating data. Whenever a task involves Linear MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Linear MCP"
  author: "OOMOL"
  version: "1.0.3"
  services: ["linear_mcp"]
  icon: "https://static.oomol.com/logo/third-party/linear_mcp.svg"
---

# Linear MCP

Operate **Linear MCP** through your OOMOL-connected account. This skill calls the `linear_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Linear MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "linear_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "linear_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_comment` — Comment on a Linear issue through Linear's MCP save_comment tool, optionally as a reply to another comment. Needs the write scope on the grant. [write]
- `create_issue` — Create a Linear issue through Linear's MCP save_issue tool. Needs the write scope on the grant; an id in the input is dropped so this never updates an existing issue. [write]
- `get_issue` — Get one Linear issue with its full description through Linear's MCP get_issue tool.
- `get_self` — Get the signed-in Linear user through Linear's MCP get_user tool.
- `list_comments` — List the comments on one Linear issue through Linear's MCP list_comments tool.
- `list_issue_labels` — List issue labels through Linear's MCP list_issue_labels tool, for the workspace or one team.
- `list_issue_statuses` — List one team's workflow states through Linear's MCP list_issue_statuses tool: the names the issue tools take as state.
- `list_issues` — List Linear issues through Linear's MCP list_issues tool with optional updated-since, ordering, limit, and cursor pagination. Descriptions may be clipped; call get_issue for the full text.
- `list_projects` — List Linear projects through Linear's MCP list_projects tool, optionally for one team, with cursor pagination.
- `list_teams` — List the teams of the connected Linear workspace through Linear's MCP list_teams tool: the keys and IDs the issue tools take as team.
- `update_issue` — Update a Linear issue through Linear's MCP save_issue tool with its id: the title, description, team, assignee, state, priority, labels, project, due date, parent or estimate. Needs the write scope on the grant. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Linear MCP state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Linear MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/linear_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Linear MCP homepage: https://linear.app/docs/mcp
- API documentation: https://linear.app/docs/mcp
