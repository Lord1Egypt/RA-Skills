---
name: oo-linear
description: "Linear (linear.app). Use this skill for ANY Linear request — reading, creating, updating, and deleting data. Whenever a task involves Linear, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Linear"
  author: "OOMOL"
  version: "1.0.1"
  services: ["linear"]
  icon: "https://static.oomol.com/logo/third-party/Linear.svg"
---

# Linear

Operate **Linear** through your OOMOL-connected account. This skill calls the `linear` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Linear. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "linear" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "linear" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_attachment` — Create or update an attachment for the specified Linear issue. [write]
- `create_comment_reaction` — Creates an emoji reaction for the specified Linear comment. [write]
- `create_linear_comment` — Creates a comment for the specified Linear issue. [write]
- `create_linear_issue` — Create a new Linear issue in the specified team and support fields such as project, person in charge, status, label, etc. [write]
- `create_linear_issue_relation` — Create a relationship between two Linear issues, such as blocks, related, or duplicate. [write]
- `create_linear_label` — Creates a new Linear issue label in the specified team. [write]
- `create_linear_project` — Create a new Linear project and associate one or more teams. [write]
- `create_project_milestone` — Creates a project milestone for the specified Linear project. [write]
- `create_project_update` — Creates a project progress update for the specified Linear project. [write]
- `delete_linear_issue` — Delete the specified Linear issue. [destructive]
- `get_all_linear_teams` — Lists all Linear team basic information accessible with the current credentials.
- `get_attachment` — Retrieve a Linear attachment based on the issue and attachment ID or file name.
- `get_current_user` — Get the currently authenticated Linear user profile.
- `get_cycles_by_team_id` — Get all cycle information under the specified team.
- `get_issue_defaults` — Gets the default status and default estimate used when the specified team creates an issue.
- `get_linear_issue` — Get details of a Linear issue, including comments, attachments, subscribers, and underlying relationship fields.
- `get_linear_project` — Get the details of a Linear project, complete with team, members, and initiatives on demand.
- `list_issue_drafts` — Lists issue drafts visible to the current user in Linear.
- `list_issues_by_team_id` — List Linear issues by team, and support cursor paging and whether to include archived issues.
- `list_linear_cycles` — Lists the Linear periods accessible by the current credential.
- `list_linear_issues` — Lists Linear issues accessible with current credentials, and supports filtering by project and person in charge.
- `list_linear_labels` — Lists Linear labels for a specified team or entire workspace.
- `list_linear_projects` — Lists Linear projects accessible with the current credentials.
- `list_linear_states` — Lists all workflow statuses for the specified team.
- `list_linear_teams` — Lists Linear teams accessible with current credentials, along with a list of members and projects.
- `list_linear_users` — List Linear users in the current workspace and support cursor paging.
- `remove_issue_label` — Removes a label from the specified Linear issue. [destructive]
- `remove_reaction` — Delete an existing Linear reaction. [destructive]
- `run_mutation` — Perform a mutation directly on the Linear GraphQL API. [write]
- `run_query` — Execute a read-only query directly against the Linear GraphQL API.
- `search_issues` — Retrieve issues through Linear's full-text search capabilities.
- `update_issue` — Update an existing Linear issue and support fields such as title, description, status, project, label, etc. [write]
- `update_linear_comment` — Update the text of an existing Linear comment. [write]
- `update_linear_project` — Update an existing Linear project. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Linear state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Linear is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=linear
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Linear homepage: https://linear.app
