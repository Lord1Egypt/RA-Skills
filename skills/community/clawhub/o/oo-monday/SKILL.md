---
name: oo-monday
description: "Monday (monday.com). Use this skill for ANY Monday request — reading, creating, updating, and deleting data. Whenever a task involves Monday, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Monday"
  author: "OOMOL"
  version: "1.0.1"
  services: ["monday"]
  icon: "https://static.oomol.com/logo/third-party/Monday.svg"
---

# Monday

Operate **Monday** through your OOMOL-connected account. This skill calls the `monday` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Monday. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "monday" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "monday" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `activate_form` — Activate a Monday Workform so it starts accepting submissions. [write]
- `add_teams_to_board` — Add Monday teams to a board as subscribers or owners. [write]
- `add_users_to_board` — Add Monday users to a board as subscribers or owners. [write]
- `archive_board` — Archive a Monday board. [write]
- `archive_item` — Archive a Monday item. [write]
- `assign_department_members` — Assign users to a Monday department on an enterprise account. [write]
- `change_item_position` — Change a Monday item's position on the same board. [write]
- `change_multiple_column_values` — Change multiple Monday column values in one mutation using the official JSON payload shape. [write]
- `change_simple_column_value` — Change a Monday column value using the official simple string mutation. [write]
- `clear_users_department` — Clear department assignments from Monday users on an enterprise account. [destructive]
- `create_board` — Create a Monday board with the official create_board mutation. [write]
- `create_column` — Create a Monday column on an existing board. [write]
- `create_dashboard` — Create a Monday dashboard with the official dashboard mutation. [write]
- `create_department` — Create a Monday department on an enterprise account. [write]
- `create_doc` — Create a Monday doc in a workspace or document column location. [write]
- `create_form` — Create a Monday Workform and its destination responses board. [write]
- `create_group` — Create a Monday group on an existing board. [write]
- `create_item` — Create a Monday item on a board, optionally setting column values and position. [write]
- `create_subitem` — Create a Monday subitem under an existing parent item. [write]
- `create_update` — Create a Monday update on an item or as a reply to an existing update. [write]
- `deactivate_form` — Deactivate a Monday Workform so it stops accepting submissions. [destructive]
- `delete_board` — Delete a Monday board. [destructive]
- `delete_column` — Delete a Monday column from an existing board. [destructive]
- `delete_dashboard` — Delete a Monday dashboard. [destructive]
- `delete_department` — Delete a Monday department on an enterprise account. [destructive]
- `delete_doc` — Delete an existing Monday doc. [destructive]
- `delete_group` — Delete a Monday group from an existing board. [destructive]
- `delete_item` — Delete a Monday item. [destructive]
- `delete_subscribers_from_board` — Remove Monday user subscribers from a board. [destructive]
- `delete_teams_from_board` — Remove Monday team subscribers from a board. [destructive]
- `delete_update` — Delete an existing Monday update. [destructive]
- `duplicate_item` — Duplicate a Monday item. [write]
- `edit_update` — Edit an existing Monday update. [write]
- `find_items_by_column_values` — Find Monday items on a board by matching explicit column values.
- `get_board_memberships` — Retrieve the user and team memberships configured on a Monday board.
- `get_current_user` — Retrieve the Monday user associated with the current personal API token.
- `get_form` — Retrieve a Monday Workform by its unique form token.
- `get_items` — Retrieve specific Monday items by ID.
- `get_items_page` — Retrieve a filtered page of Monday board items using the official items_page query.
- `get_next_items_page` — Retrieve the next page of Monday items from an items_page cursor.
- `list_activity_logs` — List board-scoped Monday activity logs.
- `list_assets` — Retrieve one or more Monday assets by asset ID.
- `list_audit_logs` — List account-level Monday audit logs on enterprise accounts.
- `list_board_columns` — List the columns for a specific Monday board.
- `list_boards` — List Monday boards with official pagination and board-level filters.
- `list_departments` — List Monday departments on enterprise accounts.
- `list_docs` — List Monday docs by document, object, or workspace identifiers.
- `list_groups` — List the groups for a specific Monday board.
- `list_subitems_by_parent` — List Monday subitems for one or more parent items.
- `list_team_members` — List the members of a specific Monday team.
- `list_teams` — List Monday teams with official filters and pagination.
- `list_update_replies` — List Monday replies for updates on one or more boards. [write]
- `list_updates` — List Monday updates with optional date filtering.
- `list_users` — List Monday users with official root-level filters and pagination.
- `list_workspaces` — List Monday workspaces with official filters and pagination.
- `move_item_to_board` — Move a Monday item to another board and target group. [write]
- `move_item_to_group` — Move a Monday item to another group on the same board. [write]
- `set_item_description_content` — Replace a Monday item description using markdown content. [write]
- `update_board` — Update a Monday board attribute with the official update_board mutation. [write]
- `update_column` — Update a Monday column with the official update_column mutation. [write]
- `update_dashboard` — Update a Monday dashboard with the official dashboard mutation. [write]
- `update_department` — Update a Monday department on an enterprise account. [write]
- `update_doc_name` — Update the name of an existing Monday doc. [write]
- `update_group` — Update an existing Monday group attribute. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Monday state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Monday is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=monday
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Monday homepage: https://monday.com
