---
name: monday-workflows
description: Manage Monday.com workspaces, boards, items, teams, and documents. Create projects, manage tasks and columns, handle team permissions, automate workflows with webhooks, and track portfolio-level analytics.
---

# Monday

![Monday](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/monday.svg)

Manage Monday.com workspaces, boards, items, teams, and documents at scale. Create and manage projects, handle task workflows, configure automations, manage team permissions, and track portfolio analytics.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=monday-workflows) for hosted connection flows and credentials so you do not need to configure Monday.com API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect Monday |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│ Monday.com API   │
│   (User Chat)   │     │   (GraphQL)  │     │   (v2)          │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin  │                       │
         │  2. Pair Device   │                       │
         │  3. Connect Monday │                      │
         │                   │  4. Secure Token      │
         │                   │  5. Proxy Requests    │
         │                   │                       │
         ▼                   ▼                       ▼
   ┌──────────┐      ┌──────────┐           ┌──────────┐
   │  SKILL   │      │ Dashboard│           │ Monday   │
   │  File    │      │ Auth     │           │ Workspace│
   └──────────┘      └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for Monday again."

## Quick Start

```bash
# List boards
clawlink_call_tool --tool "monday_boards" --params '{}'

# Get items
clawlink_call_tool --tool "monday_items" --params '{"board_id": "BOARD_ID"}'

# Get team info
clawlink_call_tool --tool "monday_get_team" --params '{"team_id": "TEAM_ID"}'
```

## Authentication

All Monday.com tool calls are authenticated automatically by ClawLink using the user's connected Monday.com workspace.

**No API key is required in chat.** ClawLink stores the OAuth token securely and injects it into every Monday.com GraphQL API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=monday and connect Monday.com (requires an active Monday.com account).
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `monday` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration monday
```

**Response:** Returns the live tool catalog for Monday.

### Reconnect

If Monday tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=monday
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration monday`

## Security & Permissions

- Access is scoped to the connected Monday.com workspace only.
- **All write operations require explicit user confirmation.** Before executing any board, item, or workspace action, confirm the target resource and intended effect with the user.
- Destructive actions (delete board, delete item, delete workspace) are marked as high-impact and must be confirmed.
- Enterprise features (audit logs, portfolios) require Enterprise plan.
- Board deletion moves to archive — permanent deletion requires separate confirmation.
- User deactivation also deactivates their integrations and automations.

## Tool Reference

### Workspaces

| Tool | Description | Mode |
|------|-------------|------|
| `monday_list_workspaces` | List all workspaces in the account | Read |
| `monday_get_workspace` | Get workspace details by ID | Read |
| `monday_create_workspace` | Create a new workspace | Write |
| `monday_update_workspace` | Update workspace name or description | Write |
| `monday_archive_workspace` | Archive (soft-remove) a workspace | Write |
| `monday_delete_workspace` | Permanently delete a workspace | Write |

### Folders

| Tool | Description | Mode |
|------|-------------|------|
| `monday_list_folders` | List all folders in a workspace | Read |
| `monday_get_folder` | Get folder details by ID | Read |
| `monday_create_folder` | Create a new folder in a workspace | Write |
| `monday_update_folder` | Update folder name | Write |
| `monday_delete_folder` | Permanently delete a folder and all nested subfolders and boards | Write |

### Boards

| Tool | Description | Mode |
|------|-------------|------|
| `monday_boards` | Get board metadata (id, name, state, kind, workspace) with filtering | Read |
| `monday_get_board` | Get full board details including structure and ownership | Read |
| `monday_create_board` | Create a new board with optional template and folder | Write |
| `monday_update_board` | Update board name, description, or owner | Write |
| `monday_archive_board` | Archive a board (can be restored) | Write |
| `monday_delete_board` | Permanently delete a board | Write |
| `monday_duplicate_board` | Duplicate a board with structure and optionally items and updates | Write |
| `monday_convert_board_to_project` | Convert board to project board with advanced project features | Write |

### Columns

| Tool | Description | Mode |
|------|-------------|------|
| `monday_columns` | Get column metadata from boards (type, title, settings, capabilities) | Read |
| `monday_create_column` | Create a new column with specified type and title | Write |
| `monday_update_column` | Update column name, description, or settings | Write |
| `monday_delete_column` | Permanently delete a column from a board | Write |

### Items

| Tool | Description | Mode |
|------|-------------|------|
| `monday_items` | Get items from a board with optional group and pagination filters | Read |
| `monday_get_item` | Get item details by ID including column values | Read |
| `monday_create_item` | Create a new item on a board with optional group and column values | Write |
| `monday_create_item_from_nl` | Create item from natural language description using LLM | Write |
| `monday_update_item` | Update item column values or name | Write |
| `monday_archive_item` | Archive an item (can be restored) | Write |
| `monday_delete_item` | Permanently delete an item | Write |
| `monday_duplicate_item` | Duplicate an item with optional updates included | Write |
| `monday_move_item` | Move item to a different group on the same board | Write |

### Column Values

| Tool | Description | Mode |
|------|-------------|------|
| `monday_change_simple_column_value` | Set column value using simple string (Text, Status, Dropdown) | Write |
| `monday_change_column_value` | Change column value with full JSON value support | Write |
| `monday_clear_column_value` | Clear/reset a column value | Write |

### Groups

| Tool | Description | Mode |
|------|-------------|------|
| `monday_groups` | Get groups from a board | Read |
| `monday_create_group` | Create a new group on a board | Write |
| `monday_update_group` | Update group name | Write |
| `monday_delete_group` | Permanently delete a group and its items | Write |
| `monday_duplicate_group` | Duplicate a group with items | Write |

### Tags

| Tool | Description | Mode |
|------|-------------|------|
| `monday_list_tags` | List all tags in the account | Read |
| `monday_get_tag` | Get tag details by ID | Read |
| `monday_create_tag` | Create a new tag or return existing tag | Write |
| `monday_delete_tag` | Remove a tag from a specific item (not account-level delete) | Write |

### Subscribers & Notifications

| Tool | Description | Mode |
|------|-------------|------|
| `monday_add_subscribers_to_object` | Add subscribers/owners to a board or item | Write |
| `monday_delete_subscribers_from_board` | Remove subscribers from a board | Write |
| `monday_create_notification` | Send a notification to a user | Write |

### Teams

| Tool | Description | Mode |
|------|-------------|------|
| `monday_list_teams` | List all teams in the account | Read |
| `monday_get_team` | Get team details by ID | Read |
| `monday_create_team` | Create a new team | Write |
| `monday_update_team` | Update team name or description | Write |
| `monday_delete_team` | Permanently delete a team | Write |
| `monday_add_users_to_team` | Add users to a team | Write |
| `monday_remove_users_from_team` | Remove users from a team | Write |
| `monday_add_teams_to_board` | Add teams to a board with permission levels | Write |
| `monday_delete_teams_from_board` | Remove teams from a board | Write |
| `monday_add_teams_to_workspace` | Add teams to a workspace | Write |
| `monday_delete_teams_from_workspace` | Remove teams from a workspace | Write |

### Users

| Tool | Description | Mode |
|------|-------------|------|
| `monday_list_users` | List all users in the account | Read |
| `monday_get_user` | Get user details by ID | Read |
| `monday_create_user` | Invite and create a new user | Write |
| `monday_update_user` | Update user name or email | Write |
| `monday_activate_users` | Activate or reactivate users | Write |
| `monday_deactivate_users` | Deactivate users (also deactivates their integrations and automations) | Write |
| `monday_add_users_to_board` | Add users to a board with specified role | Write |
| `monday_remove_users_from_board` | Remove users from a board | Write |
| `monday_add_users_to_workspace` | Add users to a workspace | Write |
| `monday_remove_users_from_workspace` | Remove users from a workspace | Write |

### Updates & Activity

| Tool | Description | Mode |
|------|-------------|------|
| `monday_get_updates` | Get updates from an item | Read |
| `monday_create_update` | Create a new update or reply to an existing update | Write |
| `monday_update_update` | Update update text | Write |
| `monday_delete_update` | Delete an update by ID | Write |

### Documents

| Tool | Description | Mode |
|------|-------------|------|
| `monday_docs` | Get document data with filtering | Read |
| `monday_get_doc` | Get document details by ID | Read |
| `monday_create_doc` | Create a new doc in a workspace or doc column | Write |
| `monday_update_doc` | Update doc content | Write |
| `monday_delete_doc` | Delete a doc by ID | Write |
| `monday_blocks` | Get document block data from workdocs | Read |

### Timeline & Sprints

| Tool | Description | Mode |
|------|-------------|------|
| `monday_get_timeline_widget` | Get timeline widget data for a board | Read |
| `monday_create_timeline_item` | Create timeline item in Emails & Activities app | Write |
| `monday_update_timeline_item` | Update timeline item details | Write |
| `monday_delete_timeline_item` | Delete timeline item | Write |

### Custom Activities

| Tool | Description | Mode |
|------|-------------|------|
| `monday_custom_activity` | List custom activities from Emails & Activities app | Read |
| `monday_create_custom_activity` | Create a custom activity type with color and icon | Write |
| `monday_update_custom_activity` | Update custom activity details | Write |
| `monday_delete_custom_activity` | Delete a custom activity | Write |

### Dashboards

| Tool | Description | Mode |
|------|-------------|------|
| `monday_get_dashboard` | Get dashboard details by ID | Read |
| `monday_create_dashboard` | Create a new dashboard with associated boards | Write |
| `monday_update_dashboard` | Update dashboard settings | Write |
| `monday_delete_dashboard` | Delete a dashboard | Write |

### Portfolio

| Tool | Description | Mode |
|------|-------------|------|
| `monday_list_portfolios` | List all portfolios | Read |
| `monday_get_portfolio` | Get portfolio details by ID | Read |
| `monday_connect_project_to_portfolio` | Link a project board to a portfolio (Enterprise only) | Write |

### Object Lifecycle

| Tool | Description | Mode |
|------|-------------|------|
| `monday_create_object` | Create any Monday.com object via GraphQL mutation | Write |
| `monday_update_object` | Update any Monday.com object via GraphQL mutation | Write |
| `monday_delete_object` | Permanently delete an object with 30-day recovery grace period | Write |
| `monday_archive_object` | Archive an object (can be restored) | Write |

### Data Aggregation

| Tool | Description | Mode |
|------|-------------|------|
| `monday_aggregate_data` | Aggregate data across boards using grouping and functions (COUNT, SUM, MEAN, MIN, MAX) | Read |

### Automations & Integrations

| Tool | Description | Mode |
|------|-------------|------|
| `monday_list_automations` | List automations on a board | Read |
| `monday_get_automation` | Get automation details | Read |
| `monday_connections` | Get connection data for integrations (Gmail, Slack, etc.) | Read |
| `monday_connection_board_ids` | Get board IDs associated with connection columns | Read |
| `monday_get_account_trigger_statistics` | Get account-level trigger and automation statistics | Read |

### Webhooks

| Tool | Description | Mode |
|------|-------------|------|
| `monday_create_webhook` | Create a webhook for board or item events | Write |
| `monday_update_webhook` | Update webhook configuration | Write |
| `monday_delete_webhook` | Delete a webhook | Write |

### Admin & Governance

| Tool | Description | Mode |
|------|-------------|------|
| `monday_audit_logs` | Get security-related activity records (Enterprise + admin permissions) | Read |
| `monday_app_subscription` | Get app subscription data (status, billing, trial, pricing) | Read |

### Asset Management

| Tool | Description | Mode |
|------|-------------|------|
| `monday_list_assets` | List assets uploaded to a board | Read |
| `monday_get_asset_url` | Get temporary URL for an asset | Read |
| `monday_delete_asset` | Delete an asset (removes enclosing update or clears File column) | Write |

## Code Examples

### List boards

```bash
clawlink_call_tool --tool "monday_boards" \
  --params '{"workspace_ids": ["WORKSPACE_ID"]}'
```

### Create an item

```bash
clawlink_call_tool --tool "monday_create_item" \
  --params '{"board_id": "BOARD_ID", "group_id": "GROUP_ID", "item_name": "New Task"}'
```

### Update column value

```bash
clawlink_call_tool --tool "monday_change_column_value" \
  --params '{"board_id": "BOARD_ID", "item_id": "ITEM_ID", "column_id": "COLUMN_ID", "value": "{\"text\": \"New Status\"}"}'
```

### Create a board

```bash
clawlink_call_tool --tool "monday_create_board" \
  --params '{"workspace_id": "WORKSPACE_ID", "name": "New Project Board"}'
```

### Get item details

```bash
clawlink_call_tool --tool "monday_get_item" \
  --params '{"item_id": "ITEM_ID"}'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm Monday is connected.
2. Call `clawlink_list_tools --integration monday` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `monday`.
5. If no Monday tools appear, direct the user to https://claw-link.dev/dashboard?add=monday.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe → call                      │
│                                                             │
│  Example: List boards → Get items → Show results             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                     │
│  list → get → describe → preview → confirm → call          │
│                                                             │
│  Example: Preview item create → User approves → Execute     │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, search, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Board creation requires `workspace_id` if `folder_id` is provided and both must match.
- Item creation supports optional column values in the request.
- Natural language item creation fetches board column schema at runtime and uses LLM to generate values.
- Account trigger statistics require admin permissions.
- Audit logs require Enterprise plan and admin permissions with manage_account_security scope.
- Portfolio linking requires Enterprise plan and boards:write scope.
- Deactivating a user also deactivates their integrations and automations.
- Users cannot deactivate themselves.
- Deleting a folder permanently removes all nested subfolders and boards — this is irreversible.
- Object deletion includes a 30-day recovery grace period before permanent removal.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration monday`. |
| Missing connection | Monday is not connected. Direct the user to https://claw-link.dev/dashboard?add=monday. |
| Permission error | The authenticated user lacks permission for this operation. |
| Board not found | The board ID does not exist. Verify with `monday_boards`. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |
| Enterprise required | Feature requires Monday.com Enterprise plan. |

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

- [Monday.com API Documentation](https://developer.monday.com/api-reference/)
- [Monday.com GraphQL API](https://api.monday.com/v2)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=monday-workflows
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Motion Planning](https://clawhub.ai/hith3sh/motion-planning) — For Motion task and project planning
- [Make Automation](https://clawhub.ai/hith3sh/make-automation) — For Make.com scenario management

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=monday-workflows)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)