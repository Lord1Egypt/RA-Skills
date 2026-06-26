---
name: personal-task-tracking
description: Query and manage ClickUp via REST API and the local `scripts/query.sh` helper. Use when listing open or completed tasks, counting due work, looking up spaces or lists, checking assignee workload, fetching task details, creating tasks, or closing tasks in ClickUp.
metadata:
  {
    "openclaw":
      {
        "emoji": "⏫",
        "requires":
          {
            "bins": ["bash", "curl", "jq"],
            "env":
              ["CLICKUP_API_KEY", "CLICKUP_TEAM_ID", "CLICKUP_ASSIGNEE_ID"],
          },
        "primaryEnv": "CLICKUP_API_KEY",
        "install":
          [
            {
              "id": "jq-brew",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
      },
  }
---

# ClickUp Skill

Interact with ClickUp's REST API for task management, reporting, and workflow automation.

## Configuration

Before using this skill, ensure the following are configured:

- **API Token:** `CLICKUP_API_KEY`
- **Team/Workspace ID:** `CLICKUP_TEAM_ID`
- **Task Assignee ID:** `CLICKUP_ASSIGNEE_ID`


Check if they are available as environment variables:
```bash
echo $CLICKUP_API_KEY
echo $CLICKUP_TEAM_ID
echo $CLICKUP_ASSIGNEE_ID
```

If not available, export them as environment variables.
```bash
export CLICKUP_API_KEY={value}
export CLICKUP_TEAM_ID={value}
export CLICKUP_ASSIGNEE_ID={value}
```


## Quick Start

### Using the Helper Script

The fastest way to query ClickUp:

```bash
# Set environment variables
export CLICKUP_API_KEY="pk_..."
export CLICKUP_TEAM_ID="..."
export CLICKUP_ASSIGNEE_ID="..."

# Get open tasks due or overdue by a given end time
./scripts/clickup-query.sh tasks --end "2026-03-28 17:00"

# Get task counts for open tasks due or overdue by a given end time
./scripts/clickup-query.sh task-count --end "2026-03-28 17:00"

# Get tasks completed during a time window
./scripts/clickup-query.sh completed-tasks --start "2026-03-24" --end "2026-03-28 17:00"

# Get spaces under the team 
./scripts/clickup-query.sh spaces

# Get lists under a space_id
./scripts/clickup-query.sh lists 123456

# Create a task with given title and due date, assign to CLICKUP_ASSIGNEE_ID, under a list_id 
./scripts/clickup-query.sh create-task {list_id} "Follow up with customer" "2026-03-28 17:00"

# Close a task with task_id 
./scripts/clickup-query.sh close-task 86e0jmdfe
```

### Direct API Calls

For custom queries or operations not covered by the helper script. Example:

```bash
# Get all open tasks (with subtasks and pagination)
curl "https://api.clickup.com/api/v2/team/{team_id}/task?include_closed=false&subtasks=true" \
  -H "Authorization: {api_key}"
```

## Common Operations

### Get open tasks due or overdue by a given end time
```bash
# Using helper script 
./scripts/clickup-query.sh tasks --end "2026-03-28 17:00"
```

### Get Task Counts due or overdue by a given end time

```bash
# Using helper script 
./scripts/clickup-query.sh task-count --end "2026-03-28 17:00"

```

### Create a Task with given title and due date
step 1. Get all list 

```bash
# Using helper script 
./scripts/clickup-query.sh spaces
./scripts/clickup-query.sh lists {space_id}

```
Step 2: Choose a list that's most relevant to the task 
Step 3: Create the task 
```bash
# Using helper script 
./scripts/clickup-query.sh create-task {list_id} "Follow up with customer" "2026-03-28 17:00"
```

### Close a Task

```bash
# Using helper script 
./scripts/clickup-query.sh close-task {task_id}
```
