---
name: monday-ops
description: >
  Agentic framework for operating monday.com workspaces via the Monday MCP connector.
  Use this skill whenever the user wants to interact with monday.com — creating boards,
  managing items/tasks, updating statuses, querying board data, building automations,
  generating sprint reports, triaging work, or performing any project management operation
  on monday.com. Trigger on phrases like "monday board", "create a task", "update status",
  "sprint summary", "move item", "board schema", "column values", "monday.com", "project
  board", "work tracker", "create a group", or any reference to managing work items,
  boards, columns, or workflows in monday.com. Also trigger when the user references
  a board ID, asks about task progress, or wants to automate monday.com workflows.
version: 0.1.1
metadata:
  openclaw:
    emoji: "📋"
    requires:
      env: []
      bins: []
    homepage: https://mcp.monday.com/mcp
---

# Monday.com Agentic Operations Skill

This skill enables Claude to operate monday.com workspaces as a project management agent. It covers discovering workspace structure, creating and modifying boards and items, managing columns and groups, posting updates, moving items through stages, and orchestrating multi-step workflows.

## Prerequisites

The user must have the **monday.com MCP connector** enabled in their Claude session. The hosted MCP endpoint is `https://mcp.monday.com/mcp`. If the connector is not connected, suggest the user enable it via the connectors menu.

## Available MCP Tools

The Monday MCP provides these tool categories. Before calling any tool, use `tool_search` with a relevant query (e.g., "monday create item") to load the exact parameter schema — never guess parameter names.

### Item Operations
| Tool | Purpose |
|------|---------|
| `create_item` | Create a new item on a board with column values |
| `delete_item` | Permanently delete an item |
| `get_board_items_by_name` | Search items by board ID and search term |
| `create_update` | Post a comment/update on an item |
| `change_item_column_values` | Modify column values of an existing item |
| `move_item_to_group` | Move an item to a different group |

### Board Operations
| Tool | Purpose |
|------|---------|
| `create_board` | Create a new board with columns |
| `get_board_schema` | Retrieve column and group structure |
| `create_group` | Add a new group to a board |
| `create_column` | Add a column to a board |
| `delete_column` | Remove a column from a board |

### Account Operations
| Tool | Purpose |
|------|---------|
| `list_users_and_teams` | Look up users or teams by name/ID |

### WorkForms Operations
| Tool | Purpose |
|------|---------|
| `create_form` | Create a new monday.com form |
| `get_form` | Retrieve a form by token |

### Dynamic API Tools (if enabled)
| Tool | Purpose |
|------|---------|
| `all_monday_api` | Run a specific monday.com GraphQL query or mutation approved by the user |
| `get_graphql_schema` | Fetch the monday.com GraphQL schema for a given type |
| `get_type_details` | Get detailed info about a GraphQL type |

> **Note:** Dynamic API tools should only be used for operations not covered by the standard tools above. Always confirm the intended query with the user before executing. Do not use these tools to access data outside the user's own workspace.

## Core Workflow: The Discover → Plan → Execute Pattern

Every monday.com task follows this three-phase pattern. Skipping discovery is the #1 cause of failed operations.

### Phase 1: Discover

Before creating or modifying anything, understand the workspace structure.

**For existing boards:**
1. Call `get_board_schema` with the board ID to learn column IDs, column types, and group IDs.
2. Column IDs are internal identifiers (e.g., `status`, `date4`, `text0`) — they are NOT the same as display names.
3. Group IDs (e.g., `new_group`, `topics`) are required for creating items in specific groups.

**For user lookups:**
1. Call `list_users_and_teams` to find user IDs before assigning items to people.

**Why this matters:** monday.com's API uses internal IDs everywhere. The column your user calls "Priority" might have the ID `status_1` or `color`. Trying to set a column by display name will fail silently or error. Always discover first.

### Phase 2: Plan

After discovery, map the user's intent to specific API calls:

- Translate user-facing names ("Status", "Due Date") to the internal column IDs from the schema.
- Determine the correct column value format for each column type (see the Column Value Formats reference).
- Identify the target group ID if the user specifies where to place an item.
- If multiple operations are needed (e.g., "create 5 tasks"), plan the sequence.

### Phase 3: Execute

Call the MCP tools in the planned order. After each call:

- Confirm success to the user with the item name, ID, and board link.
- If an operation fails, read the error message carefully — the most common issues are wrong column IDs, malformed column values, or permission errors.
- For batch operations, execute sequentially and report progress.

## Column Value Formats

Column values must be passed as JSON strings matching monday.com's expected format. Read `references/column-formats.md` for the full reference before setting column values.

**Critical rules:**
- Status columns use `label` (the display text) — e.g., `{"label": "Done"}`
- Date columns use ISO format — e.g., `{"date": "2026-05-15"}`
- People columns use user IDs — e.g., `{"personsAndTeams": [{"id": 12345, "kind": "person"}]}`
- Number columns use a plain number — e.g., `{"number": 42}`
- Text columns use plain text — e.g., `{"text": "Hello world"}`
- Dropdown columns use label IDs — e.g., `{"ids": [1, 3]}`

When in doubt, call `get_board_schema` and examine the column's `settings_str` to understand its allowed values.

## Common Agentic Workflows

### Create a Project Board from Scratch

```
1. create_board → get the new board_id
2. create_group (repeat for each stage: "To Do", "In Progress", "Done")
3. create_column (repeat for: status, date, people, priority, etc.)
4. create_item (repeat for each initial task)
```

### Sprint Summary / Status Report

```
1. get_board_schema → learn column IDs
2. get_board_items_by_name (with empty or broad search) → get all items
3. Aggregate by group and status column
4. Present a summary table with counts per status per group
```

### Triage Incoming Work

```
1. get_board_items_by_name → find items in the intake group
2. For each item, analyze the title/description
3. change_item_column_values → set priority, assignee, due date
4. move_item_to_group → route to the appropriate team group
5. create_update → post a triage note on each item
```

### Bulk Status Update

```
1. get_board_schema → learn the status column ID
2. get_board_items_by_name → find matching items
3. For each item: change_item_column_values → update status
4. Summarize what was changed
```

## Error Handling

**"Column not found"** — You used a display name instead of the internal column ID. Re-run `get_board_schema` and use the `id` field.

**"Invalid column value"** — The JSON format for the column value is wrong. Check the column type and refer to the Column Value Formats reference.

**"Item not found"** — The item ID doesn't exist or the user doesn't have access. Verify the ID and permissions.

**"Unauthorized"** — The MCP token doesn't have permission for this operation. The user may need to re-authenticate or check their monday.com permissions.

**Rate limiting** — If you get rate limit errors, add a brief pause between calls. monday.com's API has per-minute limits.

## Best Practices

1. **Always discover before mutating.** Never assume column IDs or group IDs.
2. **Confirm destructive operations.** Before deleting items, columns, or boards, show the user what will be deleted and ask for confirmation.
3. **Batch intelligently.** For operations on many items, process them sequentially and report progress (e.g., "Updated 3 of 10 items...").
4. **Use updates for context.** When changing an item's status or assignee, post a `create_update` explaining the change — this creates an audit trail.
5. **Present board links.** After creating or modifying items, provide the monday.com URL: `https://{workspace}.monday.com/boards/{board_id}`.
6. **Handle the "I don't know the board ID" case.** If the user refers to a board by name, use dynamic API tools (if available) or ask the user to provide the board ID or URL.
7. **Respect the user's terminology.** Users may say "task", "ticket", "card", or "row" — they all mean "item" in monday.com.

## Integration Patterns

### monday.com + Google Calendar
When creating items with due dates, offer to also create Google Calendar events for deadlines using the Google Calendar MCP tools.

### monday.com + Gmail
After triaging or creating items, offer to draft email notifications to assignees via Gmail MCP tools.

### monday.com + Fireflies
After meetings, use Fireflies transcripts to extract action items and create them as monday.com items automatically.

## Reference Files

- `references/column-formats.md` — Complete column value format reference for all column types. **Read this before setting any column values.**
- `references/workflows.md` — Detailed step-by-step workflow templates for common scenarios.
