---
name: oo-clickup
description: "ClickUp (clickup.com). Use this skill for ANY ClickUp request — reading, creating, updating, and deleting data. Whenever a task involves ClickUp, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "ClickUp"
  author: "OOMOL"
  version: "1.0.1"
  services: ["clickup"]
  icon: "https://static.oomol.com/logo/third-party/ClickUp.svg"
---

# ClickUp

Operate **ClickUp** through your OOMOL-connected account. This skill calls the `clickup` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected ClickUp. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "clickup" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "clickup" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_dependency` — Add a ClickUp dependency relationship to a task. [write]
- `add_tag_to_task` — Add a ClickUp tag to a task. [write]
- `add_task_link` — Add a ClickUp task link to a task. [write]
- `add_task_to_list` — Add a ClickUp task to an additional list. [write]
- `create_checklist` — Create a checklist on a ClickUp task. [write]
- `create_checklist_item` — Create a checklist item on a ClickUp checklist. [write]
- `create_folder` — Create a ClickUp folder in a space. [write]
- `create_folderless_list` — Create a ClickUp folderless list in a space. [write]
- `create_list` — Create a ClickUp list in a folder. [write]
- `create_list_from_template` — Create a ClickUp list from a folder list template. [write]
- `create_space` — Create a ClickUp space in a workspace. [write]
- `create_task` — Create a ClickUp task in a list with optional scheduling and assignee fields. [write]
- `create_task_attachment` — Upload an attachment file to a ClickUp task. [write]
- `create_task_comment` — Create a comment on a ClickUp task. [write]
- `create_task_from_template` — Create a ClickUp task from a task template. [write]
- `create_threaded_comment` — Create a threaded reply on a ClickUp comment. [write]
- `delete_checklist` — Delete a ClickUp checklist by checklist ID. [destructive]
- `delete_checklist_item` — Delete a ClickUp checklist item by checklist item ID. [destructive]
- `delete_comment` — Delete a ClickUp comment by comment ID. [destructive]
- `delete_dependency` — Delete a ClickUp dependency relationship from a task. [destructive]
- `delete_folder` — Delete a ClickUp folder by folder ID. [destructive]
- `delete_list` — Delete a ClickUp list by list ID. [destructive]
- `delete_space` — Delete a ClickUp space by space ID. [destructive]
- `delete_task` — Delete a ClickUp task by task ID. [destructive]
- `delete_task_link` — Delete a ClickUp task link from a task. [destructive]
- `get_current_user` — Get the authenticated ClickUp user profile.
- `get_custom_task_types` — Get the ClickUp custom task types available on a workspace.
- `get_folder` — Get a ClickUp folder by folder ID.
- `get_folder_custom_fields` — Get the ClickUp custom fields available on a folder.
- `get_folder_views` — Get the ClickUp views available on a folder.
- `get_list` — Get a ClickUp list by list ID.
- `get_list_custom_fields` — Get the ClickUp custom fields available on a list.
- `get_list_members` — Get the ClickUp members with explicit access to a list.
- `get_list_views` — Get the ClickUp views available on a list.
- `get_space` — Get a ClickUp space by space ID.
- `get_space_custom_fields` — Get the ClickUp custom fields available on a space.
- `get_space_tags` — Get the ClickUp tags available on a space.
- `get_space_views` — Get the ClickUp views available on a space.
- `get_task` — Get a ClickUp task by task ID.
- `get_task_comments` — Get the comments on a ClickUp task.
- `get_task_members` — Get the ClickUp members with explicit access to a task.
- `get_task_templates` — Get the ClickUp task templates available in a workspace.
- `get_threaded_comments` — Get the threaded replies on a ClickUp comment.
- `get_user` — Get a ClickUp workspace user by user ID.
- `get_view` — Get a ClickUp view by view ID.
- `get_view_tasks` — Get the visible ClickUp tasks in a view.
- `get_workspace_custom_fields` — Get the ClickUp custom fields available on a workspace.
- `get_workspace_everything_level_views` — Get the ClickUp everything-level views available on a workspace.
- `list_folderless_lists` — List the ClickUp folderless lists available in a space.
- `list_folders` — List the ClickUp folders available in a space.
- `list_list_tasks` — List the ClickUp tasks in a list with optional filters.
- `list_lists` — List the ClickUp lists available in a folder.
- `list_spaces` — List the ClickUp spaces available in a workspace.
- `list_workspace_tasks` — List the ClickUp tasks in a workspace with official filter parameters.
- `list_workspace_users` — List the members visible on a ClickUp workspace.
- `list_workspaces` — List the ClickUp workspaces available to the authenticated user.
- `move_task_to_home_list` — Move a ClickUp task to a new home list. [write]
- `remove_custom_field_value` — Remove a ClickUp custom field value from a task. [destructive]
- `remove_tag_from_task` — Remove a ClickUp tag from a task. [destructive]
- `remove_task_from_list` — Remove a ClickUp task from an additional list. [destructive]
- `set_custom_field_value` — Set a ClickUp custom field value on a task. [write]
- `update_checklist` — Update a ClickUp checklist by checklist ID. [write]
- `update_checklist_item` — Update a ClickUp checklist item by checklist item ID. [write]
- `update_comment` — Update a ClickUp comment by comment ID. [write]
- `update_folder` — Update a ClickUp folder by folder ID. [write]
- `update_list` — Update a ClickUp list by list ID. [write]
- `update_space` — Update a ClickUp space by space ID. [write]
- `update_task` — Update a ClickUp task by task ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change ClickUp state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — ClickUp is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2, API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=clickup
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- ClickUp homepage: https://clickup.com
