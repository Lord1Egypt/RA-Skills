---
name: oo-sunsama-mcp
description: "Sunsama MCP (help.sunsama.com). Use this skill for ANY Sunsama MCP request — reading, creating, updating, and deleting data. Whenever a task involves Sunsama MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sunsama MCP"
  author: "OOMOL"
  version: "1.0.5"
  services: ["sunsama_mcp"]
  icon: "https://static.oomol.com/logo/third-party/sunsama_mcp.svg"
---

# Sunsama MCP

Operate **Sunsama MCP** through your OOMOL-connected account. This skill calls the `sunsama_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sunsama MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sunsama_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sunsama_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `accept_meeting_invite` — Confirms attendance to a meeting that the user is invited to. [write]
- `add_subtasks_to_task` — Adds multiple subtasks to an existing task. Do not use for merging existing tasks in as subtasks. [write]
- `add_task_to_channel` — Adds a task to a channel. [write]
- `align_task_with_objective` — Aligns a task with an objective. [write]
- `append_task_notes` — Appends Markdown content to the end of an existing task's notes. Existing notes are preserved; the new content is added below them with a horizontal rule separator. Use edit_task_notes to replace the notes body entirely. [write]
- `call_tool` — Call a Sunsama MCP tool with JSON arguments. [destructive]
- `change_backlog_folder` — Moves one or more tasks to a backlog folder. If folderId is null, removes tasks from their current folder. [write]
- `create_calendar_event` — Creates a new calendar event. [write]
- `create_channel` — Creates a new channel for the user. [write]
- `create_task` — Creates a single task with a title, optional notes (markdown), and estimated time. Scheduled to a day by default; pass `backlog` instead to stage it in the backlog. This is also the tool for a task that links to an item in another tool — pass `integrationUrl`, which works for a backlog task too. [write]
- `create_weekly_objective` — Creates a new weekly objective. [write]
- `decline_meeting_invite` — Decline attendance to a meeting that the user is invited to. [write]
- `delete_all_incomplete_recurring_task_instances` — PERMANENTLY deletes incomplete instances of a recurring task and TERMINATES the series, preventing any future instances from ever being created. This is irreversible. When afterDate is provided, only instances after that date are deleted and the series is terminated at that date. When omitted, all incomplete instances are deleted. WARNING: If the user wants to temporarily skip a period (e.g. vacation) and resume the series afterwards, do NOT use this tool — use edit_task_recurrence_rule with deleteOldInstancesAfter and firstOccurrenceOnOrAfter instead. [destructive]
- `delete_calendar_event` — Removes a calendar event and deletes all associated tasks. If the event is a meeting then any access role can remove the event. Otherwise only owners or writers can remove the event. Note: If the event is a meeting and the user is an owner or write this will remove the event for ALL attendees. [destructive]
- `delete_channel` — Deletes one of the user's channels. Takes a channel ID, not a channel name — use the search_channels tool to resolve a name the user mentions into an ID first. Tasks, objectives, and calendar events in the channel are not deleted, but they lose their channel assignment and cannot be reassigned by undoing this. Deleting a category also uncategorizes the channels inside it. This cannot be undone, so confirm with the user before calling it. [destructive]
- `delete_task` — Deletes an existing task. [destructive]
- `edit_subtask_title` — Updates the title of an existing subtask. [write]
- `edit_task_due_date` — Sets or clears the due date of a task. This is the hard deadline, not the day the task is planned/scheduled for (use move_task_to_day for that). [write]
- `edit_task_notes` — Replaces the notes body of an existing task with new Markdown content. The full notes field is overwritten — use append_task_notes to add to existing notes without replacing them. [write]
- `edit_task_recurrence_rule` — Updates the recurrence rule of an existing task. This is the preferred tool for temporarily pausing or skipping a recurring task for a specific period (e.g. vacation, leave). By combining deleteOldInstancesAfter (to clear instances during the skip period) and firstOccurrenceOnOrAfter (to restart the series afterwards), you can maintain the recurrence while accommodating temporary breaks — unlike delete_all_incomplete_recurring_task_instances which permanently terminates the series. When firstOccurrenceOnOrAfter is provided, this forks the recurring series: a new series begins from that date and the old series ends the day before. [write]
- `edit_task_time_estimate` — Updates the time estimate of an existing task. [write]
- `edit_task_title` — Updates the title of an existing task. [write]
- `get_archived_tasks` — Fetches the users archived tasks
- `get_backlog_tasks` — Fetches the users backlog tasks
- `get_daily_highlights` — Gets a list of daily highlights (end of day journal entries of your work day) for the user. Returns published daily wraps in Markdown format. If startDate and endDate are omitted, returns only the most recent one.
- `get_help_article` — Fetches the full text of a single Sunsama help center article. First call "list_help_articles" to find the relevant article, then pass its id here. Returns the article title, url, and plain-text body so you can answer the user's question from the docs.
- `get_task_by_id` — Fetches a single task by its Sunsama task ID. Returns full task details including integration information.
- `get_task_time_estimate` — Gets the time estimate for a task in minutes.
- `import_task_from_calendar_event` — Imports a calendar event as a task. [write]
- `list_help_articles` — Lists Sunsama's help center articles as a catalog: each entry has an id, title, description, category, and url. Use this whenever the user asks how a Sunsama feature works, what Sunsama can or cannot do, or whenever you are unsure about product behavior or a limitation. Pick the most relevant article from the list, then call "get_help_article" with its id to read it and answer from the docs instead of guessing. You can also share the article url with the user.
- `list_resources` — Lists all available resources and resource templates exposed by this MCP server. Use this tool to discover what data sources are available when the client doesn't support the MCP resources protocol natively. Returns an array of resources, where each resource has: - name: The resource identifier - uri: The static URI (for fixed resources) OR uri_template (for parameterized resources) - description: What the resource provides - mimeType: The content type returned
- `list_tools` — Discover the current Sunsama task and daily planning MCP tools with their live input schemas.
- `mark_subtask_as_completed` — Marks a subtask of an existing task as completed. [write]
- `mark_subtask_as_incomplete` — Marks a subtask of an existing task as incomplete. [write]
- `mark_task_as_completed` — Marks a task as completed. Can also be used to move a task to a previous day which auto-completes the task. [write]
- `mark_task_as_incomplete` — Marks a task as incomplete. [write]
- `move_calendar_event` — Updates a calendar event's date, time, and/or duration. [write]
- `move_task_from_backlog` — Moves a task out of the backlog and onto a specific date. [write]
- `move_task_to_backlog` — Moves a task to the backlog. IF THE USER ASKS YOU TO MOVE A TASK TO A SPECIFIC DAY THEN YOU SHOULD USE THE move_task_to_day TOOL NOT THIS ONE. [write]
- `move_task_to_day` — Moves or defers a task to a specific date. [write]
- `read_resource` — Reads a specific resource by URI. Use this tool to fetch data from resources when the client doesn't support the MCP resources protocol natively. For static resources, pass the exact URI from list_resources. For templated resources, fill in the placeholders with actual values. Example: If list_resources shows uri_template "sunsama://tasks/{calendarDay}", you would call this with uri "sunsama://tasks/2025-01-15" to get tasks for that day.
- `rename_channel` — Renames one of the user's channels. Takes a channel ID, not a channel name — use the search_channels tool to resolve a name the user mentions into an ID first. Renaming only changes the channel's label; the tasks, objectives, and calendar events assigned to it stay assigned. [write]
- `reorder_tasks` — Reorders tasks for the calendar day according to the provided order of taskIds. [write]
- `reposition_task_in_backlog` — Repositions a task within the backlog by moving it to a specific time bucket (horizon) and position (append/prepend). [write]
- `restore_task` — Changes a task from deleted to not deleted. [write]
- `search_channels` — Searches the user's channels by meaning, not just by exact name. Returns the closest matching channels ordered by relevance, so "client work" can match a channel named "Acme Corp". Use this to resolve a channel a user mentions into a channel ID before assigning tasks to it.
- `search_tasks` — Searches for tasks. Returns tasks that match the search term or are similar to the search term.
- `set_backlog_priority` — Sets the backlog priority of a task. Backlog priority persists and is used for tasks in the backlog. Valid values: "urgent", "high", "medium", "low", "none". Set to null to clear. [write]
- `set_calendar_event_allow_task_projections` — Sets whether tasks are allowed to be automatically projected (scheduled) at the same time as a calendar event. When set to true, tasks can be automatically projected during the event. When set to false, tasks cannot be automatically projected during the event. Note: This only affects automatic projections; users can still manually timebox tasks during this event. [write]
- `set_daily_priority` — Sets the daily priority of a task. Daily priority is tied to a specific day and decays after that day. Valid values: "urgent", "important", "normal", "low". Set to null to clear. The date is automatically determined from the task. [write]
- `set_shutdown_time` — Sets the shutdown time for a specific day. [write]
- `start_task_timer` — Starts the timer for a task or subtask. If a subtaskId is provided, starts the timer for that specific subtask. [write]
- `stop_task_timer` — Stops the timer for a task or subtask. If a subtaskId is provided, stops the timer for that specific subtask. [destructive]
- `timebox_a_task_to_calendar` — Timeboxes a task to the calendar. This will create a timebox event for the task. This may also be referred to as "scheduling" a task or "adding a task to the calendar". [write]
- `toggle_auto_import_events` — Enables or disables automatic importing of calendar events to the daily task list. [write]
- `unarchive_task` — Unarchives a task and moves it to a specific date or the backlog if no date is provided. [write]
- `update_all_incomplete_recurring_task_instances` — Updates all incomplete instances of a recurring task to match the current task. This is useful when you want to apply changes made to one instance of a recurring task to all future incomplete instances. [write]
- `update_calendar_preferences` — Updates preferences for a specific calendar including whether it is the default for tasks, default for events, and whether it is included in auto-importing of events. [write]
- `update_import_event_filters` — Updates the exclusion filters that determine which calendar events are excluded from automatic import. Events matching any of these filters will NOT be automatically imported. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sunsama MCP state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sunsama MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/connections/sunsama_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Sunsama MCP homepage: https://help.sunsama.com/docs/integrations/mcp/
- API documentation: https://help.sunsama.com/docs/integrations/mcp/
