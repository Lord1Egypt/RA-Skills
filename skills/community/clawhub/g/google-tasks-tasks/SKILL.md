---
name: google-tasks-tasks
description: Google Tasks API integration with managed OAuth. Manage task lists, tasks, due dates, notes, and completion state in Google Tasks. Use this skill when users want to create, update, or manage tasks and to-do items in Google Tasks.
---

# Google Tasks

![Google Tasks](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/google-tasks.svg?v=2)

Access Google Tasks via the Tasks API with managed OAuth authentication. Manage task lists, tasks, due dates, notes, and completion state.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-tasks-tasks) for hosted connection flows and credentials so you do not need to configure Google Tasks API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Google Tasks |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect Google Tasks |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Google Tasks   │
│   (User Chat)   │     │   (OAuth)    │     │   (Tasks API)    │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect Tasks     │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │  Google  │
   │  File    │           │ Auth     │           │  Tasks   │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Google Tasks again."

## Quick Start

```bash
# List task lists
clawlink_call_tool --tool "googletasks_list_tasklists" --params '{}'

# List tasks in a task list
clawlink_call_tool --tool "googletasks_list_tasks" --params '{"tasklist_id": "@default"}'

# Get a task
clawlink_call_tool --tool "googletasks_get_task" --params '{"tasklist_id": "@default", "task_id": "YOUR_TASK_ID"}'
```

## Authentication

All Google Tasks tool calls are authenticated automatically by ClawLink using the user's connected Google account.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Google Tasks API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=google-tasks and connect Google Tasks.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `google-tasks` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration google-tasks
```

**Response:** Returns the live tool catalog for Google Tasks.

### Reconnect

If Google Tasks tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=google-tasks
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration google-tasks`

## Security & Permissions

- Access is scoped to task lists and tasks within the connected Google account.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete task, clear completed tasks) are marked as high-impact and must be confirmed.

## Tool Reference

### Task List Management

| Tool | Description | Mode |
|------|-------------|------|
| `googletasks_list_tasklists` | List all task lists for the authenticated user | Read |
| `googletasks_get_tasklist` | Get a specific task list by ID | Read |
| `googletasks_insert_tasklist` | Create a new task list | Write |
| `googletasks_update_tasklist` | Update a task list's title | Write |
| `googletasks_delete_tasklist` | Delete a task list and all its tasks | Write |
| `googletasks_clear_completed_tasks` | Clear all completed tasks from a task list | Write |

### Task Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googletasks_list_tasks` | List all tasks in a task list | Read |
| `googletasks_get_task` | Get a specific task by ID | Read |
| `googletasks_insert_task` | Create a new task in a task list | Write |
| `googletasks_update_task` | Update a task's title, notes, due date, or status | Write |
| `googletasks_delete_task` | Delete a task | Write |
| `googletasks_move_task` | Move a task within a task list (change position or list) | Write |
| `googletasks_patch_task` | Patch a task's individual fields | Write |

### Completion Operations

| Tool | Description | Mode |
|------|-------------|------|
| `googletasks_complete_task` | Mark a task as completed | Write |
| `googletasks_uncomplete_task` | Mark a task as not completed | Write |

## Code Examples

### List all task lists

```bash
clawlink_call_tool --tool "googletasks_list_tasklists" \
  --params '{}'
```

### List tasks in the default task list

```bash
clawlink_call_tool --tool "googletasks_list_tasks" \
  --params '{
    "tasklist_id": "@default"
  }'
```

### Create a new task

```bash
clawlink_call_tool --tool "googletasks_insert_task" \
  --params '{
    "tasklist_id": "@default",
    "title": "Review quarterly report",
    "notes": "Check all numbers before submitting",
    "due": "2024-03-15T17:00:00Z"
  }'
```

### Mark a task as completed

```bash
clawlink_call_tool --tool "googletasks_complete_task" \
  --params '{
    "tasklist_id": "@default",
    "task_id": "YOUR_TASK_ID"
  }'
```

### Create a new task list

```bash
clawlink_call_tool --tool "googletasks_insert_tasklist" \
  --params '{
    "title": "Work Projects"
  }'
```

### Update a task

```bash
clawlink_call_tool --tool "googletasks_update_task" \
  --params '{
    "tasklist_id": "@default",
    "task_id": "YOUR_TASK_ID",
    "title": "Updated task title",
    "notes": "Added more notes here."
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Google Tasks is connected.
2. Call `clawlink_list_tools --integration google-tasks` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `google-tasks`.
5. If no Google Tasks tools appear, direct the user to https://claw-link.dev/dashboard?add=google-tasks.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → call                                         │
│                                                             │
│  Example: List task lists → List tasks → Show results      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview → User approves            │
│           → Execute update                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, and get operations before writes.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Use `@default` as the tasklist_id to refer to the user's default task list.
- Task IDs are stable within a task list but not across lists.
- Tasks can have subtasks (nested tasks) — the `parent` field defines the hierarchy.
- Completed tasks are moved to the "completed" section and hidden by default.
- Due dates use RFC 3339 timestamp format.
- `clear_completed_tasks` permanently removes all completed tasks from a task list.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration google-tasks`. |
| Missing connection | Google Tasks is not connected. Direct the user to https://claw-link.dev/dashboard?add=google-tasks. |
| `RESOURCE_NOT_FOUND` | Task or task list does not exist. Check the ID. |
| `INVALID_ARGUMENT` | Invalid parameter or missing required field. Review the tool schema with `clawlink_describe_tool`. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `google-tasks`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [Google Tasks API Overview](https://developers.google.com/tasks/reference/rest)
- [Tasklists Reference](https://developers.google.com/tasks/reference/rest/v1/tasklists)
- [Tasks Reference](https://developers.google.com/tasks/reference/rest/v1/tasks)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-tasks-tasks
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=google-tasks-tasks)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)