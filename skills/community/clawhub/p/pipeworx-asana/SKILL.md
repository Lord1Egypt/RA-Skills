# Asana

Asana MCP — wraps the Asana REST API (OAuth)

## asana_list_workspaces

Get all accessible Asana workspaces. Returns workspace names and IDs needed to list projects and tas

## asana_list_tasks

List tasks in a project. Returns task ID, name, completion status, assignee, and due date. Requires 

## asana_get_task

Get full task details including name, description, assignee, projects, tags, subtasks, and status. R

## asana_create_task

Create a new task in a project. Returns task ID, name, and permalink. Requires project ID and task n

## asana_list_projects

List all projects in a workspace. Returns project ID, name, and archived status. Requires workspace 

## asana_search_tasks

Search tasks across a workspace by keyword. Returns matching tasks with ID, name, completion status,

```json
{
  "mcpServers": {
    "asana": {
      "url": "https://gateway.pipeworx.io/asana/mcp"
    }
  }
}
```
