# Clickup

ClickUp MCP — wraps the ClickUp REST API v2 (BYO API key)

## clickup_list_tasks

List all tasks in a ClickUp list. Returns task ID, name, status, priority, assignees, due date, and 

## clickup_get_task

Fetch full task details including name, description, status, priority, assignees, tags, and time tra

## clickup_create_task

Create a new task in a ClickUp list. Provide list ID, task name, and optionally priority and assigne

## clickup_list_spaces

List all spaces in your ClickUp workspace. Returns space ID, name, and status.

## clickup_list_folders

List all folders in a ClickUp space. Provide space ID (e.g., "789"). Returns folder ID, name, and li

```json
{
  "mcpServers": {
    "clickup": {
      "url": "https://gateway.pipeworx.io/clickup/mcp"
    }
  }
}
```
