---
name: oo-asana
description: "Asana (asana.com). Use this skill for ANY Asana request — reading, creating, updating, and deleting data. Whenever a task involves Asana, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Asana"
  author: "OOMOL"
  version: "1.0.7"
  services: ["asana"]
  icon: "https://static.oomol.com/logo/third-party/Asana.svg"
---

# Asana

Operate **Asana** through your OOMOL-connected account. This skill calls the `asana` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Asana. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "asana" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "asana" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_project_custom_field` — Add a custom field setting to an Asana project. [write]
- `add_project_followers` — Add users as followers of an Asana project. [write]
- `add_project_members` — Add users as members of an Asana project. [write]
- `add_section_task` — Move a task into a section, optionally at a specific position. [write]
- `add_task_dependencies` — Add dependencies to an Asana task. [write]
- `add_task_dependents` — Add dependent tasks to an Asana task. [write]
- `add_task_followers` — Add followers to an Asana task. [write]
- `add_task_project` — Add an Asana task to a project with optional section placement. [write]
- `add_task_tag` — Add a tag to an Asana task. [write]
- `add_team_user` — Add an existing organization user to an Asana team. [write]
- `add_workspace_user` — Add or invite a user to an Asana workspace or organization. [write]
- `create_attachment` — Attach a downloaded public file or external resource URL to an Asana object. [write]
- `create_custom_field` — Create an Asana custom field in a workspace. [write]
- `create_custom_field_enum_option` — Create an option for an Asana enum or multi-enum custom field. [write]
- `create_project` — Create a project at exactly one workspace or team location. [write]
- `create_project_section` — Create a section in an Asana project, optionally at a specific position. [write]
- `create_subtask` — Create a direct subtask under an Asana task. [write]
- `create_tag` — Create a tag in an Asana workspace through the generic tag endpoint. [write]
- `create_task` — Create an Asana task in a project, workspace, or parent task. [write]
- `create_task_story` — Create a comment story on an Asana task. [write]
- `create_team` — Create an Asana team within an organization. [write]
- `create_team_project` — Create a project in an Asana team. [write]
- `create_workspace_project` — Create a project in an Asana workspace or organization. [write]
- `create_workspace_tag` — Create a tag in an Asana workspace or organization. [write]
- `delete_attachment` — Delete an Asana attachment. [destructive]
- `delete_custom_field` — Delete an Asana custom field. [destructive]
- `delete_project` — Delete an Asana project. [destructive]
- `delete_section` — Delete an empty Asana project section. [destructive]
- `delete_story` — Delete an Asana story or task comment created by the authenticated user. [destructive]
- `delete_tag` — Delete an Asana tag. [destructive]
- `delete_task` — Delete an Asana task. [destructive]
- `duplicate_project` — Start an asynchronous job to duplicate an Asana project. [write]
- `duplicate_task` — Duplicate an Asana task and selected associations. [write]
- `get_attachment` — Get an Asana attachment by gid.
- `get_custom_field` — Get an Asana custom field by gid.
- `get_project` — Get an Asana project by gid.
- `get_project_task_counts` — Get all documented task and milestone counts for an Asana project.
- `get_section` — Get an Asana project section by gid.
- `get_story` — Get an Asana story, including a task comment story, by gid.
- `get_tag` — Get an Asana tag by gid.
- `get_task` — Get a single Asana task by gid.
- `get_task_by_custom_id` — Get an Asana task by workspace and custom ID.
- `get_team` — Get an Asana team by gid.
- `get_user` — Get an Asana user by gid, email, or the special identifier "me".
- `get_workspace` — Get an Asana workspace or organization by gid.
- `get_workspace_events` — Read the Enterprise workspace event stream from an optional sync token and return Asana's next sync state.
- `get_workspace_user` — Get a user record in the context of an Asana workspace or organization.
- `insert_custom_field_enum_option` — Reorder an option in an Asana enum or multi-enum custom field. [write]
- `insert_project_section` — Move a section before or after another section in the same project. [write]
- `list_attachments` — List attachments on an Asana task, project, or project brief.
- `list_project_custom_field_settings` — List the custom field settings on an Asana project.
- `list_project_sections` — List sections in an Asana project.
- `list_project_tasks` — List tasks within an Asana project.
- `list_projects` — List projects filtered by exactly one workspace or team.
- `list_section_tasks` — List tasks in an Asana section.
- `list_subtasks` — List direct subtasks of an Asana task.
- `list_tag_tasks` — List tasks carrying an Asana tag.
- `list_tags` — List tags in an Asana workspace through the generic tag endpoint.
- `list_task_dependencies` — List tasks that an Asana task depends on.
- `list_task_dependents` — List tasks that depend on an Asana task.
- `list_task_projects` — List projects associated with a task.
- `list_task_stories` — List each story and comment recorded on an Asana task.
- `list_task_tags` — List the Asana tags attached to a task.
- `list_tasks` — List tasks matching Asana's general task filters.
- `list_team_custom_field_settings` — List the custom field settings on an Asana team. Asana returns this collection without pagination.
- `list_team_projects` — List projects shared with a team.
- `list_team_users` — List users who belong to an Asana team.
- `list_user_favorites` — List a user's favorite Asana resources within a workspace.
- `list_user_task_list_tasks` — List tasks in an Asana user task list.
- `list_user_teams` — List the teams to which an Asana user belongs in an organization.
- `list_users` — List users visible to the connected account, optionally filtered by workspace or team.
- `list_workspace_custom_fields` — List the custom fields in an Asana workspace.
- `list_workspace_projects` — List projects in an Asana workspace or organization.
- `list_workspace_tags` — List tags in an Asana workspace or organization.
- `list_workspace_teams` — List teams in an Asana organization workspace.
- `list_workspace_users` — List users in an Asana workspace or organization.
- `list_workspaces` — List the Asana workspaces and organizations visible to the connected account.
- `remove_project_custom_field` — Remove a custom field setting from an Asana project. [destructive]
- `remove_project_followers` — Remove users from an Asana project's followers. [destructive]
- `remove_project_members` — Remove users from an Asana project. [destructive]
- `remove_task_dependencies` — Remove dependencies from an Asana task. [destructive]
- `remove_task_dependents` — Remove dependent tasks from an Asana task. [destructive]
- `remove_task_followers` — Remove followers from an Asana task. [destructive]
- `remove_task_project` — Remove an Asana task from a project. [destructive]
- `remove_task_tag` — Remove a tag from an Asana task. [destructive]
- `remove_team_user` — Remove a user from an Asana team. [destructive]
- `remove_workspace_user` — Remove a user from an Asana workspace or organization. [destructive]
- `search_workspace_projects` — Search projects in a workspace using Asana's documented project filters. Asana does not paginate search results; use limit to cap the page size.
- `search_workspace_tasks` — Search tasks in an Asana workspace using advanced filters.
- `set_task_parent` — Set, change, or remove an Asana task's parent. [destructive]
- `update_custom_field` — Update an Asana custom field. [write]
- `update_custom_field_enum_option` — Update an Asana enum option. [write]
- `update_project` — Update one or more writable fields on an Asana project. [write]
- `update_section` — Rename an Asana project section. [write]
- `update_story` — Update the text, HTML, or pinned state of an Asana comment story. [write]
- `update_tag` — Update one or more mutable fields on an Asana tag. [write]
- `update_task` — Update an existing Asana task. [write]
- `update_team` — Update an existing Asana team. [write]
- `update_user` — Update an Asana user's display name or custom field values. [write]
- `update_workspace` — Rename an existing Asana workspace or organization. [write]
- `update_workspace_user` — Update an Asana user in the context of a workspace or organization. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Asana state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Asana is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/asana
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Asana homepage: https://asana.com
- API documentation: https://developers.asana.com/reference/rest-api-reference
