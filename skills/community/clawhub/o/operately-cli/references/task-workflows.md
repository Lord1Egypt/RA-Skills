# Task Workflows

Task management best practices in Operately, covering task creation, assignment, status management, and organization patterns for both project and space tasks.

## Task Basics

### Creating Tasks

**Project Tasks:**

```bash
# Basic project task
operately tasks create \
  --type project \
  --id p1 \
  --name "Design mockups" \
  --milestone-id m1 \
  --assignee-id null \
  --due-date null

# Project task with assignee and due date
operately tasks create \
  --type project \
  --id p1 \
  --name "Implement login flow" \
  --milestone-id m1 \
  --assignee-id u1 \
  --due-date 2024-06-15

# Project task with description
operately tasks create \
  --type project \
  --id p1 \
  --name "Write API documentation" \
  --milestone-id m1 \
  --assignee-id u2 \
  --due-date null

operately tasks update_description \
  --task-id t3 \
  --type project \
  --description "# API Documentation\n\n## Endpoints to Document\n- /api/users\n- /api/projects\n- /api/goals"
```

**Space Tasks:**

```bash
# Basic space task
operately tasks create \
  --type space \
  --id s1 \
  --name "Update team documentation" \
  --milestone-id null \
  --assignee-id u1 \
  --due-date 2024-06-15

# Unassigned space task
operately tasks create \
  --type space \
  --id s1 \
  --name "Review onboarding process" \
  --milestone-id null \
  --assignee-id null \
  --due-date null

# Space task with description
operately tasks create \
  --type space \
  --id s1 \
  --name "Organize team resources" \
  --milestone-id null \
  --assignee-id u2 \
  --due-date 2024-06-20

operately tasks update_description \
  --task-id t3 \
  --type space \
  --description "# Resource Organization\n\n## Tasks\n- Categorize documents\n- Update links\n- Archive old files"
```

**Note:** Tasks require `--type` ("project" or "space") and `--id` (project or space ID) parameters. Space tasks cannot belong to milestones and must have `--milestone-id null`.

### Getting Task Details

```bash
operately tasks get --id t1
```

### Listing Tasks

```bash
# List tasks in a project
operately tasks list --project-id p1

# List tasks in a space
operately spaces list_tasks --space-id s1
```

**Note:** Use `tasks list` for projects and `spaces list_tasks` for spaces.

## Task Assignment

### Assigning Tasks

```bash
# Assign project task to user
operately tasks update_assignee \
  --task-id t1 \
  --type project \
  --assignee-id u1

# Assign space task to user
operately tasks update_assignee \
  --task-id t2 \
  --type space \
  --assignee-id u2

# Unassign (set to null)
operately tasks update_assignee \
  --task-id t1 \
  --type project \
  --assignee-id null
```

### Finding Potential Assignees

```bash
# For project tasks
operately tasks list_potential_assignees \
  --id t1 \
  --type project

# For space tasks
operately tasks list_potential_assignees \
  --id t2 \
  --type space
```

## Status Management

### Updating Task Status

```bash
# Mark project task as in progress
operately tasks update_status \
  --task-id t1 \
  --type project \
  --status.id in_progress \
  --status.label "In Progress" \
  --status.color blue \
  --status.index 1 \
  --status.value in_progress \
  --status.closed false

# Mark space task as in progress
operately tasks update_status \
  --task-id t2 \
  --type space \
  --status.id in_progress \
  --status.label "In Progress" \
  --status.color blue \
  --status.index 1 \
  --status.value in_progress \
  --status.closed false

# Mark as completed
operately tasks update_status \
  --task-id t1 \
  --type project \
  --status.id done \
  --status.label "Done" \
  --status.color green \
  --status.index 2 \
  --status.value done \
  --status.closed true

# Mark as blocked
operately tasks update_status \
  --task-id t1 \
  --type project \
  --status.id blocked \
  --status.label "Blocked" \
  --status.color red \
  --status.index 3 \
  --status.value blocked \
  --status.closed false
```

### Custom Status Workflows

Task statuses are project-specific or space-specific.

**Project task statuses:**

```bash
# Get available statuses
operately projects get --id p1

# Update project task statuses
operately projects update_task_statuses \
  --project-id p1 \
  --task-statuses.0.id ts1 \
  --task-statuses.0.label "To Do" \
  --task-statuses.1.id ts2 \
  --task-statuses.1.label "In Progress" \
  --task-statuses.2.id ts3 \
  --task-statuses.2.label "In Review" \
  --task-statuses.3.id ts4 \
  --task-statuses.3.label "Done"
```

**Space task statuses:**

```bash
# Update space task statuses
operately spaces update_task_statuses \
  --space-id s1 \
  --task-statuses.0.id ts1 \
  --task-statuses.0.label "To Do" \
  --task-statuses.0.color gray \
  --task-statuses.0.index 0 \
  --task-statuses.0.value todo \
  --task-statuses.0.closed false \
  --task-statuses.1.id ts2 \
  --task-statuses.1.label "In Progress" \
  --task-statuses.1.color blue \
  --task-statuses.1.index 1 \
  --task-statuses.1.value in_progress \
  --task-statuses.1.closed false \
  --task-statuses.2.id ts3 \
  --task-statuses.2.label "Done" \
  --task-statuses.2.color green \
  --task-statuses.2.index 2 \
  --task-statuses.2.value done \
  --task-statuses.2.closed true
```

## Task Updates

### Updating Task Name

```bash
# Update project task name
operately tasks update_name \
  --task-id t1 \
  --type project \
  --name "Updated task name"

# Update space task name
operately tasks update_name \
  --task-id t2 \
  --type space \
  --name "Updated space task name"
```

### Updating Task Description

```bash
# Update project task description
operately tasks update_description \
  --task-id t1 \
  --type project \
  --description "# Updated Description\n\n## Details\nAdditional context and requirements."

# Update space task description
operately tasks update_description \
  --task-id t2 \
  --type space \
  --description "# Space Task Details\n\n## Context\nTeam-wide task for documentation."
```

### Updating Due Date

```bash
# Set due date for project task
operately tasks update_due_date \
  --task-id t1 \
  --type project \
  --due-date 2024-06-20

# Set due date for space task
operately tasks update_due_date \
  --task-id t2 \
  --type space \
  --due-date 2024-06-25

# Remove due date
operately tasks update_due_date \
  --task-id t1 \
  --type project \
  --due-date null
```

## Task Organization

### Moving Tasks Between Milestones

**Note:** Only project tasks can be moved between milestones. Space tasks cannot belong to milestones.

```bash
# Simple move (project tasks only)
operately tasks update_milestone \
  --task-id t1 \
  --milestone-id m2

# Move with specific ordering (project tasks only)
operately tasks update_milestone_and_ordering \
  --task-id t1 \
  --milestone-id m2 \
  --milestones-ordering-state.0.milestone-id m2 \
  --milestones-ordering-state.0.ordering-state.0 t1
```

### General Task Movement

```bash
# Move task from one project to another
operately tasks move \
  --task-id t1 \
  --destination-type project \
  --destination-id p2

# Move task from project to space
operately tasks move \
  --task-id t1 \
  --destination-type space \
  --destination-id s1

# Move task from one space to another
operately tasks move \
  --task-id t2 \
  --destination-type space \
  --destination-id s2
```

**Note:** When moving a project task to a space, the milestone association is removed since space tasks cannot have milestones.

### Deleting Tasks

```bash
# Delete project task
operately tasks delete --task-id t1 --type project

# Delete space task
operately tasks delete --task-id t2 --type space
```

## Task Patterns

### Sprint Planning Pattern

```bash
# 1. Create sprint milestone
operately projects create_milestone \
  --project-id p1 \
  --name "Sprint 5" \
  --due-date 2024-06-15

# 2. Create sprint backlog
operately tasks create \
  --type project \
  --id p1 \
  --name "User story: Login with SSO" \
  --milestone-id m5 \
  --assignee-id u1

operately tasks update_description \
  --task-id t1 \
  --type project \
  --description "# User Story\n\nAs a user, I want to login with SSO so that I don't need another password.\n\n## Acceptance Criteria\n- Google OAuth integration\n- Microsoft OAuth integration\n- Fallback to email/password"

operately tasks create \
  --type project \
  --id p1 \
  --name "User story: Dashboard widgets" \
  --milestone-id m5 \
  --assignee-id u2

operately tasks create \
  --type project \
  --id p1 \
  --name "Bug: Fix pagination" \
  --milestone-id m5 \
  --assignee-id u3

# 3. Daily updates
operately tasks update_status --task-id t1 --type project --status.id in_progress --status.label "In Progress" --status.color blue --status.index 1 --status.value in_progress --status.closed false
operately tasks update_status --task-id t2 --type project --status.id done --status.label "Done" --status.color green --status.index 2 --status.value done --status.closed true

# 4. Sprint end
operately tasks update_status --task-id t3 --type project --status.id done --status.label "Done" --status.color green --status.index 2 --status.value done --status.closed true
```

### Kanban Board Pattern

```bash
# 1. Set up custom statuses
operately projects update_task_statuses \
  --project-id p1 \
  --task-statuses.0.label "Backlog" \
  --task-statuses.1.label "Ready" \
  --task-statuses.2.label "In Progress" \
  --task-statuses.3.label "Review" \
  --task-statuses.4.label "Done"

# 2. Create tasks in backlog
operately tasks create --type project --id p1 --name "Feature A" --milestone-id m1
operately tasks create --type project --id p1 --name "Feature B" --milestone-id m1
operately tasks create --type project --id p1 --name "Feature C" --milestone-id m1

# 3. Move through workflow
operately tasks update_status --task-id t1 --type project --status.id ready --status.label "Ready" --status.color blue --status.index 1 --status.value ready --status.closed false
operately tasks update_status --task-id t1 --type project --status.id in_progress --status.label "In Progress" --status.color blue --status.index 2 --status.value in_progress --status.closed false
operately tasks update_status --task-id t1 --type project --status.id review --status.label "Review" --status.color yellow --status.index 3 --status.value review --status.closed false
operately tasks update_status --task-id t1 --type project --status.id done --status.label "Done" --status.color green --status.index 4 --status.value done --status.closed true
```

### Space Task Board Pattern

```bash
# 1. Enable tasks tool for space
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled true \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true

# 2. Set up custom statuses for space
operately spaces update_task_statuses \
  --space-id s1 \
  --task-statuses.0.id backlog \
  --task-statuses.0.label "Backlog" \
  --task-statuses.0.color gray \
  --task-statuses.0.index 0 \
  --task-statuses.0.value backlog \
  --task-statuses.0.closed false \
  --task-statuses.1.id in_progress \
  --task-statuses.1.label "In Progress" \
  --task-statuses.1.color blue \
  --task-statuses.1.index 1 \
  --task-statuses.1.value in_progress \
  --task-statuses.1.closed false \
  --task-statuses.2.id done \
  --task-statuses.2.label "Done" \
  --task-statuses.2.color green \
  --task-statuses.2.index 2 \
  --task-statuses.2.value done \
  --task-statuses.2.closed true

# 3. Create space tasks (no milestones)
operately tasks create --type space --id s1 --name "Update documentation" --milestone-id null --assignee-id u1 --due-date 2024-06-15
operately tasks create --type space --id s1 --name "Review team processes" --milestone-id null --assignee-id u2 --due-date null
operately tasks create --type space --id s1 --name "Organize resources" --milestone-id null --assignee-id null --due-date null

# 4. Move through workflow
operately tasks update_status --task-id t1 --type space --status.id in_progress --status.label "In Progress" --status.color blue --status.index 1 --status.value in_progress --status.closed false
operately tasks update_status --task-id t1 --type space --status.id done --status.label "Done" --status.color green --status.index 2 --status.value done --status.closed true
```

**Note:** Space tasks work like project tasks but cannot have milestones. This makes them ideal for ongoing team tasks that aren't tied to specific project milestones.

### Department Task Management Pattern

```bash
# 1. Create department space
operately spaces create \
  --name "Engineering" \
  --mission "Build and maintain product infrastructure" \
  --company-permissions 10 \
  --public-permissions 0

# 2. Enable tasks
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled true \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true

# 3. Create recurring team tasks
operately tasks create \
  --type space \
  --id s1 \
  --name "Weekly on-call rotation" \
  --milestone-id null \
  --assignee-id u1 \
  --due-date 2024-06-07

operately tasks create \
  --type space \
  --id s1 \
  --name "Monthly security review" \
  --milestone-id null \
  --assignee-id u2 \
  --due-date 2024-06-30

operately tasks create \
  --type space \
  --id s1 \
  --name "Update team documentation" \
  --milestone-id null \
  --assignee-id null \
  --due-date null

# 4. Track completion
operately tasks update_status --task-id t1 --type space --status.id done --status.label "Done" --status.color green --status.index 2 --status.value done --status.closed true
```

### Bug Tracking Pattern

```bash
# 1. Create bug tasks
operately tasks create \
  --type project \
  --id p1 \
  --name "Bug: Login fails on Safari" \
  --milestone-id bugs_milestone

operately tasks update_description \
  --task-id t1 \
  --type project \
  --description "# Bug Report\n\n## Steps to Reproduce\n1. Open Safari\n2. Go to login page\n3. Enter credentials\n4. Click login\n\n## Expected\nUser logs in\n\n## Actual\nError message appears\n\n## Priority\nHigh"

# 2. Assign to developer
operately tasks update_assignee --task-id t1 --type project --assignee-id u1

# 3. Track progress
operately tasks update_status --task-id t1 --type project --status.id in_progress --status.label "In Progress" --status.color blue --status.index 1 --status.value in_progress --status.closed false

# 4. Mark as fixed
operately tasks update_status --task-id t1 --type project --status.id done --status.label "Done" --status.color green --status.index 2 --status.value done --status.closed true
operately tasks update_description \
  --task-id t1 \
  --type project \
  --description "# Bug Report\n\n[original description]\n\n## Resolution\nFixed Safari-specific cookie handling issue. Deployed in v1.2.3."
```

## Task Comments and Collaboration

### Adding Comments

```bash
operately comments create \
  --entity-id t1 \
  --entity-type "task" \
  --content "Started working on this. Will have it done by EOD."

operately comments create \
  --entity-id t1 \
  --entity-type "task" \
  --content "Blocked on API access. Need credentials from DevOps."
```

### Listing Comments

```bash
operately comments list \
  --entity-id t1 \
  --entity-type "task"
```

## Task Metrics and Reporting

### Listing Tasks by Status

Get all tasks and filter by status in your script:

```bash
# Get all tasks and process with jq or similar
operately tasks list --project-id p1 --compact | jq '.[] | select(.status == "in_progress")'
```

### Listing Tasks by Assignee

```bash
# Get user's assignments
operately people list_assignments

# Get assignment count
operately people get_assignments_count
```

## Gotchas

### Project vs Space Tasks

**Key differences:**
- **Project tasks** can belong to milestones (`--milestone-id m1`)
- **Space tasks** cannot belong to milestones (always `--milestone-id null`)
- Both use the same task commands with different `--type` parameter
- Moving a project task to a space removes its milestone association

### Task Status IDs

Task statuses are project-specific or space-specific. Always get the status IDs first:

```bash
# For project tasks
operately projects get --id p1

# For space tasks, check space tools
operately spaces list_tools --space-id s1
```

Don't assume status IDs like "completed" or "in_progress" - use the actual IDs from the project or space.

### Space Tasks Require Tool Enablement

Before creating space tasks, enable the tasks tool:

```bash
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled true \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true
```

### Listing Tasks

Different commands for projects vs spaces:
- **Project tasks**: `operately tasks list --project-id p1`
- **Space tasks**: `operately spaces list_tasks --space-id s1`

### Milestone Association

- **Project tasks** can be associated with a milestone or not
- **Space tasks** cannot have milestones (limitation)
- All tasks must belong to either a project or space

### Due Dates Are Optional

Due dates are optional but recommended for prioritization.

### Assignee vs Creator

The task creator and assignee can be different people. Use `--assignee-id` to assign to someone else.

### Task Descriptions Support Markdown

Use markdown for rich task descriptions. For longer content, use `--description-file <path>` to load the markdown from a file:

```bash
operately tasks create \
  --type project \
  --id p1 \
  --name "Complex feature" \
  --milestone-id m1

operately tasks update_description \
  --task-id t1 \
  --type project \
  --description "# Feature: Advanced Search\n\n## Requirements\n- Full-text search\n- Filters by date, author, type\n- Sort options\n\n## Technical Notes\n- Use Elasticsearch\n- Index updates via queue\n\n## Acceptance Criteria\n- [ ] Search returns relevant results\n- [ ] Filters work correctly\n- [ ] Performance < 200ms"

operately tasks update_description \
  --task-id t1 \
  --type project \
  --description-file ./advanced-search.md
```
