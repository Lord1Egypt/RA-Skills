---
name: oo-clickup-mcp
description: "ClickUp MCP (developer.clickup.com). Use this skill for ANY ClickUp MCP request — reading, creating, and updating data. Whenever a task involves ClickUp MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ClickUp MCP"
  author: "OOMOL"
  version: "1.0.4"
  services: ["clickup_mcp"]
  icon: "https://static.oomol.com/logo/third-party/clickup_mcp.svg"
---

# ClickUp MCP

Operate **ClickUp MCP** through your OOMOL-connected account. This skill calls the `clickup_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ClickUp MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "clickup_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "clickup_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_task` — Create a task in a ClickUp List. [write]
- `create_task_comment` — Add a comment to a ClickUp task. [write]
- `get_task` — Get one ClickUp task, optionally including normally summarized sections.
- `get_workspace_hierarchy` — Get the authorized ClickUp Workspace hierarchy of Spaces, Folders, and Lists.
- `get_workspace_members` — List members and guests in an authorized ClickUp Workspace.
- `search_workspace` — Search tasks, Lists, Folders, and Docs across the authorized ClickUp Workspaces.
- `send_chat_message` — Send a message to a ClickUp Chat channel. [write]
- `update_task` — Update the properties of an existing ClickUp task. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ClickUp MCP state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ClickUp MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/clickup_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- ClickUp MCP homepage: https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server
- API documentation: https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server
