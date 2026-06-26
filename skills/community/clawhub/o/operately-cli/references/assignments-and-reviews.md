# Assignments and Reviews

Get items that need your attention or review using the Operately CLI.

## Overview

The `people list_assignments` command retrieves all assignments and items requiring your attention, organized into three categories based on urgency and your role.

## Basic Usage

```bash
operately people list_assignments
```

This returns all items assigned to you or requiring your review, with no additional parameters needed.

## Response Structure

The command returns assignments categorized into three groups:

### 1. `due_soon`
Items you own that require immediate attention:
- **Overdue** - Past their due date
- **Due today** - Due on the current date
- **Due soon** - Due within the next few days

### 2. `needs_review`
Items where you are the reviewer and need to provide acknowledgment:
- Project check-ins awaiting review
- Goal updates requiring acknowledgment
- Milestone completions needing approval

### 3. `upcoming`
Items you own with future due dates:
- Tasks and milestones with upcoming deadlines
- Items without due dates

## Assignment Types

Each assignment includes:

- **`type`** - The kind of item:
  - `project_check_in` - Project status update
  - `goal_check_in` - Goal progress update
  - `milestone` - Project milestone
  - `project_task` - Task within a project
  - `space_task` - Task within a space
  - `goal` - Goal itself

- **`role`** - Your relationship to the item:
  - `owner` - You are responsible for completing it
  - `reviewer` - You need to review/acknowledge it

- **`origin`** - The parent resource (project, goal, or space) containing this assignment

- **`due_date`** - When the item is due (may be null)

- **`due_status`** - Urgency level: `overdue`, `due_today`, `due_soon`, `upcoming`, or `none`

- **`task_status`** - Current state (for tasks): `pending`, `in_progress`, `done`, etc.

## Grouping

Assignments are grouped by their origin (parent project, goal, or space), making it easy to see all related items together. Within each group, assignments are sorted by urgency, with the most critical items first.

## Example Output Structure

```json
{
  "data": {
    "due_soon": [
      {
        "origin": {
          "id": "project-123",
          "name": "Q2 Roadmap",
          "type": "project",
          "path": "/space/projects/q2-roadmap",
          "space_name": "Engineering"
        },
        "assignments": [
          {
            "name": "Complete API design",
            "type": "milestone",
            "role": "owner",
            "due_date": "2026-04-15",
            "due_status": "overdue",
            "due_status_label": "Overdue by 2 days"
          }
        ]
      }
    ],
    "needs_review": [
      {
        "origin": {
          "id": "goal-456",
          "name": "Revenue Growth",
          "type": "goal",
          "path": "/space/goals/revenue-growth",
          "space_name": "Sales"
        },
        "assignments": [
          {
            "name": "Q1 Check-in",
            "type": "goal_check_in",
            "role": "reviewer",
            "author_name": "John Doe",
            "action_label": "Review Q1 Check-in"
          }
        ]
      }
    ],
    "upcoming": [
      {
        "origin": {
          "id": "project-789",
          "name": "Mobile App",
          "type": "project",
          "path": "/space/projects/mobile-app",
          "space_name": "Product"
        },
        "assignments": [
          {
            "name": "Design mockups",
            "type": "project_task",
            "role": "owner",
            "due_date": "2026-05-30",
            "due_status": "upcoming",
            "due_status_label": "Due in 45 days",
            "task_status": "pending"
          }
        ]
      }
    ]
  }
}
```

## Filtering Results

Use `jq` to filter specific categories or types:

```bash
# Only items needing review
operately people list_assignments --compact | jq '.data.needs_review'

# Only overdue items
operately people list_assignments --compact | \
  jq '.data.due_soon[].assignments[] | select(.due_status == "overdue")'

# Count items in each category
operately people list_assignments --compact | \
  jq '{
    due_soon: (.data.due_soon | map(.assignments | length) | add // 0),
    needs_review: (.data.needs_review | map(.assignments | length) | add // 0),
    upcoming: (.data.upcoming | map(.assignments | length) | add // 0)
  }'

# All project check-ins needing review
operately people list_assignments --compact | \
  jq '.data.needs_review[].assignments[] | select(.type == "project_check_in")'
```

## Common Workflows

### Daily Review Routine

Check what needs attention each morning:

```bash
# Get overview
operately people list_assignments

# Focus on urgent items
operately people list_assignments --compact | \
  jq '.data.due_soon, .data.needs_review'
```

### Acknowledge Check-ins

After reviewing items, acknowledge them:

```bash
# List check-ins needing review
operately people list_assignments --compact | \
  jq '.data.needs_review[].assignments[] | select(.type == "project_check_in") | .resource_id'

# Acknowledge a specific check-in
operately projects acknowledge_check_in --check-in-id <id>
```

### Update Task Status

Move tasks forward after working on them:

```bash
# Find your pending tasks
operately people list_assignments --compact | \
  jq '.data.due_soon[].assignments[] | select(.type == "project_task" and .task_status == "pending")'

# Update task status
operately tasks update_status \
  --task-id <id> \
  --type project \
  --status.id in_progress \
  --status.label "In Progress" \
  --status.color blue \
  --status.index 1 \
  --status.value in_progress \
  --status.closed false
```

## Integration with Other Commands

The assignments list provides IDs and context for other operations:

- Use `resource_id` to get full details: `operately projects get_milestone --id <resource_id>`
- Use `origin.id` to navigate to parent: `operately projects get --id <origin.id>`
- Use `path` to construct web URLs for sharing

## Tips

1. **Run daily** - Make `people list_assignments` part of your morning routine to stay on top of work
2. **Filter by urgency** - Focus on `due_soon` and `needs_review` first, then plan `upcoming` work
3. **Group by origin** - The grouping helps you batch related work (e.g., review all items for one project)
4. **Use compact output** - Add `--compact` flag when piping to `jq` for easier parsing
5. **Save to file** - Use `--output assignments.json` to track changes over time
