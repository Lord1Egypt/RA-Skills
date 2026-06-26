---
name: motion-planning
description: Manage projects, tasks, schedules, custom fields, and team collaboration in Motion. Create projects, manage recurring tasks, configure workspaces, track statuses, and handle team scheduling with timezone-aware work hours.
---

# Motion

![Motion](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/motion.webp)

Manage projects, tasks, schedules, custom fields, and team collaboration in Motion at scale. Create and manage projects, handle task workflows, configure workspaces, track statuses, and manage team scheduling with timezone-aware work hours.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=motion-planning) for hosted connection flows and credentials so you do not need to configure Motion API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Motion |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│   Motion API     │
│   (User Chat)   │     │   (REST)     │     │   (v1)          │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin  │                       │
         │  2. Pair Device     │                       │
         │  3. Connect Motion   │                       │
         │                   │  4. Secure Token        │
         │                   │  5. Proxy Requests      │
         │                   │                         │
         ▼                   ▼                         ▼
   ┌──────────┐      ┌──────────┐           ┌──────────┐
   │  SKILL   │      │ Dashboard│           │  Motion  │
   │  File    │      │ Auth      │           │ Workspace│
   └──────────┘      └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Motion again."

## Quick Start

```bash
# List workspaces
clawlink_call_tool --tool "motion_list_workspaces" --params '{}'

# List projects
clawlink_call_tool --tool "motion_list_projects" --params '{}'

# List tasks
clawlink_call_tool --tool "motion_list_tasks" --params '{}'

# Get current user
clawlink_call_tool --tool "motion_get_my_user" --params '{}'
```

## Authentication

All Motion tool calls are authenticated automatically by ClawLink using the user's connected Motion account.

**No API key is required in chat.** ClawLink stores the API key securely and injects it into every Motion API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=motion and connect Motion (requires an active Motion account).
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `motion` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration motion
```

**Response:** Returns the live tool catalog for Motion.

### Reconnect

If Motion tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=motion
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration motion`

## Security & Permissions

- Access is scoped to the connected Motion workspace(s) only.
- **All write operations require explicit user confirmation.** Before executing any project, task, or workspace action, confirm the target resource and intended effect with the user.
- Destructive actions (delete task, delete custom field, unassign task) are marked as high-impact and must be confirmed.
- Custom field deletion permanently removes the field from the workspace — this is irreversible.
- Task deletion permanently removes the task from Motion — this is irreversible.
- Unassigning a task removes the current assignee, leaving the task unassigned.

## Tool Reference

### User & Identity

| Tool | Description | Mode |
|------|-------------|------|
| `motion_get_my_user` | Get the current user (owner of the API key) — returns ID, name, and email | Read |

### Workspaces

| Tool | Description | Mode |
|------|-------------|------|
| `motion_list_workspaces` | Get all workspaces accessible to the user, with optional workspace ID filtering | Read |

### Projects

| Tool | Description | Mode |
|------|-------------|------|
| `motion_list_projects` | Get all projects for a workspace, optionally filtered by workspace | Read |
| `motion_get_project` | Get a single project by ID — returns name, description, status, and custom field values | Read |
| `motion_create_project` | Create a new project in a workspace with optional due date, description (HTML), labels, and priority | Write |
| `motion_add_custom_field_to_project` | Add or update a custom field value on a project | Write |

### Tasks

| Tool | Description | Mode |
|------|-------------|------|
| `motion_list_tasks` | Get all tasks with optional filtering by assignee, project, workspace, status, label, or name | Read |
| `motion_get_task` | Get a task by ID — returns title, description, due date, priority, assignees, scheduling info, and custom fields | Read |
| `motion_create_task` | Create a new task in a workspace with name, priority, due date, and assignee | Write |
| `motion_update_task` | Update an existing task — modify name, priority, due date, status, or assignee (partial update) | Write |
| `motion_delete_task` | Permanently delete a task from Motion | Write |
| `motion_move_task` | Move a task to a different workspace | Write |
| `motion_unassign_task` | Remove the current assignee from a task, leaving it unassigned | Write |
| `motion_create_recurring_task` | Create a recurring task with a schedule pattern (daily, weekly, monthly, etc.) | Write |
| `motion_list_recurring_tasks` | Get all recurring tasks for a workspace | Read |

### Comments

| Tool | Description | Mode |
|------|-------------|------|
| `motion_list_comments` | Get all comments on a specific task with cursor-based pagination | Read |
| `motion_create_comment` | Create a new comment on a task | Write |

### Custom Fields

| Tool | Description | Mode |
|------|-------------|------|
| `motion_list_custom_fields` | Get all custom fields for a workspace | Read |
| `motion_create_custom_field` | Create a new custom field in a workspace (supports text, select, multiSelect, date types; provide options in metadata for select types) | Write |
| `motion_add_custom_field_to_task` | Add or update a custom field value on a task | Write |
| `motion_add_custom_field_to_project` | Add or update a custom field value on a project | Write |
| `motion_delete_custom_field` | Permanently delete a custom field from the workspace | Write |
| `motion_delete_custom_field_from_task` | Remove a custom field value from a task (provide task ID and custom field value ID) | Write |
| `motion_delete_custom_field_from_project` | Remove a custom field value from a project | Write |

### Schedules & Statuses

| Tool | Description | Mode |
|------|-------------|------|
| `motion_list_schedules` | Get the user's scheduling configuration including work hours and timezone settings | Read |
| `motion_list_statuses` | Get available task statuses for a workspace | Read |

### Users

| Tool | Description | Mode |
|------|-------------|------|
| `motion_list_users` | Get users for a workspace or team with cursor-based pagination and workspace/team filtering | Read |

## Code Examples

### List workspaces

```bash
clawlink_call_tool --tool "motion_list_workspaces" \
  --params '{}'
```

### List projects

```bash
clawlink_call_tool --tool "motion_list_projects" \
  --params '{"workspaceId": "WORKSPACE_ID"}'
```

### Get a task

```bash
clawlink_call_tool --tool "motion_get_task" \
  --params '{"taskId": "TASK_ID"}'
```

### Create a task

```bash
clawlink_call_tool --tool "motion_create_task" \
  --params '{"name": "New Task", "priority": "high", "dueDate": "2025-06-15"}'
```

### Update a task

```bash
clawlink_call_tool --tool "motion_update_task" \
  --params '{"taskId": "TASK_ID", "name": "Updated Task Name", "priority": "medium"}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Motion is connected.
2. Call `clawlink_list_tools --integration motion` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `motion`.
5. If no Motion tools appear, direct the user to https://claw-link.dev/dashboard?add=motion.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List workspaces → List projects → Show results     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call          │
│                                                             │
│  Example: Preview task create → User approves → Execute     │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Custom fields must be created in a workspace before they can be added to tasks or projects.
- Custom field deletion permanently removes the field and all its values across the workspace — this is irreversible.
- Recurring tasks automatically generate task instances based on the specified frequency pattern.
- Cursor-based pagination is supported on list endpoints for tasks, comments, and users.
- Task update supports partial updates — only provide the fields you want to change.
- Moving a task to a different workspace changes its parent workspace.
- Unassigning a task removes the current assignee but does not delete the task.
- Schedules include work hours and timezone configuration for the user.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration motion`. |
| Missing connection | Motion is not connected. Direct the user to https://claw-link.dev/dashboard?add=motion. |
| Permission error | The authenticated user lacks permission for this operation. |
| Workspace not found | The workspace ID does not exist. Verify with `motion_list_workspaces`. |
| Task not found | The task ID does not exist. Verify with `motion_list_tasks`. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |
| High-impact action | Destructive action requires explicit user confirmation before execution. |

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

## Resources

- [Motion API Documentation](https://motion.app/developers)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=motion-planning
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Monday Workflows](https://clawhub.ai/hith3sh/monday-workflows) — For Monday.com board and project management
- [Make Automation](https://clawhub.ai/hith3sh/make-automation) — For Make.com scenario management

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=motion-planning)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)