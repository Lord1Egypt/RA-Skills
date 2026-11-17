---
name: oo-monday
description: "monday (monday.com). Use this skill for ANY monday request — reading, creating, updating, and deleting data. Whenever a task involves monday, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "monday"
  author: "OOMOL"
  version: "1.0.9"
  services: ["monday"]
  icon: "https://static.oomol.com/logo/third-party/Monday.svg"
---

# monday

Operate **monday** through your OOMOL-connected account. This skill calls the `monday` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected monday. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

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

- `activate_form` — Activate a monday Workform so it starts accepting submissions. [write]
- `add_teams_to_board` — Add monday teams to a board as subscribers or owners. [write]
- `add_users_to_board` — Add monday users to a board as subscribers or owners. [write]
- `archive_board` — Archive a monday board. [destructive]
- `archive_item` — Archive a monday item. [destructive]
- `assign_department_members` — Assign users to a monday department on an enterprise account. [write]
- `change_item_position` — Change a monday item's position on the same board. [write]
- `change_multiple_column_values` — Change multiple monday column values in one mutation using the official JSON payload shape. [write]
- `change_simple_column_value` — Change a monday column value using the official simple string mutation. [write]
- `clear_users_department` — Clear department assignments from monday users on an enterprise account. [destructive]
- `create_board` — Create a monday board with the official create_board mutation. [write]
- `create_column` — Create a monday column on an existing board. [write]
- `create_dashboard` — Create a monday dashboard with the official dashboard mutation. [write]
- `create_department` — Create a monday department on an enterprise account. [write]
- `create_doc` — Create a monday doc in a workspace or document column location. [write]
- `create_form` — Create a monday Workform and its destination responses board. [write]
- `create_group` — Create a monday group on an existing board. [write]
- `create_item` — Create a monday item on a board, optionally setting column values and position. [write]
- `create_subitem` — Create a monday subitem under an existing parent item. [write]
- `create_update` — Create a monday update on an item or as a reply to an existing update. [write]
- `create_workspace` — Create a monday workspace with the official create_workspace mutation. [write]
- `deactivate_form` — Deactivate a monday Workform so it stops accepting submissions. [destructive]
- `delete_board` — Delete a monday board. [destructive]
- `delete_column` — Delete a monday column from an existing board. [destructive]
- `delete_dashboard` — Delete a monday dashboard. [destructive]
- `delete_department` — Delete a monday department on an enterprise account. [destructive]
- `delete_doc` — Delete an existing monday doc. [destructive]
- `delete_group` — Delete a monday group from an existing board. [destructive]
- `delete_item` — Delete a monday item. [destructive]
- `delete_subscribers_from_board` — Remove monday user subscribers from a board. [destructive]
- `delete_teams_from_board` — Remove monday team subscribers from a board. [destructive]
- `delete_update` — Delete an existing monday update. [destructive]
- `delete_workspace` — Delete a monday workspace with the official delete_workspace mutation. [destructive]
- `duplicate_item` — Duplicate a monday item. [write]
- `edit_update` — Edit an existing monday update. [write]
- `find_items_by_column_values` — Find monday items on a board by matching explicit column values.
- `get_board_memberships` — Retrieve the user and team memberships configured on a monday board.
- `get_current_user` — Retrieve the monday user associated with the current personal API token.
- `get_form` — Retrieve a monday Workform by its unique form token.
- `get_items` — Retrieve specific monday items by ID.
- `get_items_page` — Retrieve a filtered page of monday board items using the official items_page query.
- `get_next_items_page` — Retrieve the next page of monday items from an items_page cursor.
- `list_activity_logs` — List board-scoped monday activity logs.
- `list_assets` — Retrieve one or more monday assets by asset ID.
- `list_audit_logs` — List account-level monday audit logs on enterprise accounts.
- `list_board_columns` — List the columns for a specific monday board.
- `list_boards` — List monday boards with official pagination and board-level filters.
- `list_departments` — List monday departments on enterprise accounts.
- `list_docs` — List monday docs by document, object, or workspace identifiers.
- `list_groups` — List the groups for a specific monday board.
- `list_subitems_by_parent` — List monday subitems for one or more parent items.
- `list_team_members` — List the members of a specific monday team.
- `list_teams` — List monday teams, optionally filtering by team IDs.
- `list_update_replies` — List monday replies for updates on one or more boards.
- `list_updates` — List monday updates with optional date filtering.
- `list_users` — List monday users with official root-level filters and pagination.
- `list_workspaces` — List monday workspaces with official filters and pagination.
- `move_item_to_board` — Move a monday item to another board and target group. [destructive]
- `move_item_to_group` — Move a monday item to another group on the same board. [write]
- `set_item_description_content` — Replace a monday item description using markdown content. [destructive]
- `update_board` — Update a monday board attribute with the official update_board mutation. [destructive]
- `update_column` — Update a monday column with the official update_column mutation. [write]
- `update_dashboard` — Update a monday dashboard with the official dashboard mutation. [write]
- `update_department` — Update a monday department on an enterprise account. [write]
- `update_doc_name` — Update the name of an existing monday doc. [write]
- `update_group` — Update an existing monday group attribute. [write]
- `update_workspace` — Update a monday workspace with the official update_workspace mutation. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change monday state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — monday is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/monday
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- monday homepage: https://monday.com
- API documentation: https://developer.monday.com/api-reference/docs
