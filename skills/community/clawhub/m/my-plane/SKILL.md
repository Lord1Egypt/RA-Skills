---
name: my-plane
description: "Manage Plane.so projects and work items using the `plane` CLI. List projects, create/update/search issues, manage cycles and modules, add comments, and assign members."
metadata: {"moltbot":{"requires":{"bins":["plane"],"env":["PLANE_API_KEY","PLANE_WORKSPACE"]},"primaryEnv":"PLANE_API_KEY","emoji":"✈️","homepage":"https://github.com/HonLuk/my-plane","install":[{"id":"github","kind":"download","url":"https://github.com/HonLuk/my-plane/releases/latest/download/plane","targetDir":"~/.local/bin/","bins":["plane"],"label":"Download plane CLI from GitHub"}]}}
---

# Plane Skill

Interact with [Plane.so](https://plane.so) project management via the `plane` CLI.

## Installation

Download the single executable file:

```bash
curl -L -o ~/.local/bin/plane https://github.com/HonLuk/my-plane/releases/latest/download/plane
chmod +x ~/.local/bin/plane
```

Make sure `~/.local/bin` is in your PATH.

## Setup

```bash
export PLANE_API_KEY="your-api-key"
export PLANE_WORKSPACE="your-workspace-slug"
# Optional: for self-hosted Plane (default: https://api.plane.so)
export PLANE_BASE_URL="https://api.plane.so"
```

Get your API key from: **Plane → Profile Settings → Personal Access Tokens**

The workspace slug is the URL path segment (e.g., for `https://app.plane.so/my-team/` the slug is `my-team`).

## Commands

### Current User

```bash
plane me                      # Show authenticated user info
```

### Workspace Members

```bash
plane members                 # List all workspace members (name, email, role, ID)
```

### Projects

```bash
plane projects list                                      # List all projects
plane projects get PROJECT_ID                            # Get project details
plane projects create --name "My Project" --identifier "PROJ"  # Create project
```

### Work Items (Issues)

```bash
# List work items
plane issues list -p PROJECT_ID
plane issues list -p PROJECT_ID --priority high --assignee USER_ID
plane issues list -p PROJECT_ID --state STATE_ID

# Get details
plane issues get -p PROJECT_ID ISSUE_ID
plane issues get-short PROJ-SEQ  # e.g., PROJ-123 (fastest way)

# Create
plane issues create -p PROJECT_ID --name "Fix login bug" --priority high
plane issues create -p PROJECT_ID --name "Feature" --assignee USER_ID --label LABEL_ID

# Update
plane issues update -p PROJECT_ID ISSUE_ID --state STATE_ID --priority medium

# Assign to members
plane issues assign -p PROJECT_ID ISSUE_ID USER_ID_1 USER_ID_2

# Delete
plane issues delete -p PROJECT_ID ISSUE_ID

# Search across workspace
plane issues search "login bug"
```

### Comments

```bash
plane comments list -p PROJECT_ID -i ISSUE_ID            # List comments on a work item
plane comments list -p PROJECT_ID -i ISSUE_ID --all      # Show all activity (not just comments)
plane comments add -p PROJECT_ID -i ISSUE_ID "Looks good, merging now"  # Add a comment
```

### Cycles (Sprints)

```bash
plane cycles list -p PROJECT_ID
plane cycles get -p PROJECT_ID CYCLE_ID
plane cycles create -p PROJECT_ID --name "Sprint 1" --start 2026-01-27 --end 2026-02-10
```

### Modules

```bash
plane modules list -p PROJECT_ID
plane modules get -p PROJECT_ID MODULE_ID
plane modules create -p PROJECT_ID --name "Auth Module" --description "Authentication features"
```

### States & Labels

```bash
plane states -p PROJECT_ID    # List workflow states (useful for getting state IDs)
plane labels -p PROJECT_ID    # List labels (useful for getting label IDs)
```

## Output Formats

Default output is a formatted table. Add `-f json` for raw JSON:

```bash
plane projects list -f json
plane issues list -p PROJECT_ID -f json
```

## Pagination

All list commands support cursor-based pagination. Pagination info is displayed above results:

```bash
plane projects list
# Shows:
# Pagination: total: 50 | pages: 5 | showing: 10
# Next page: --cursor 10:1:0

# Use cursor to navigate
plane issues list -p PROJECT_ID --cursor "10:1:0"

# Control page size
plane issues list -p PROJECT_ID --per-page 20
```

## Field Selection

```bash
# Return only specific fields
plane issues list -p PROJECT_ID --fields "id,name,state"

# Expand related objects
plane issues list -p PROJECT_ID --expand "assignees,state"

# Sort results
plane issues list -p PROJECT_ID --order-by "-created_at"
```

## Getting Help

Every command has detailed help:

```bash
plane --help
plane issues --help
plane issues create --help
```

## Typical Workflow

1. `plane projects list` — find your project ID
2. `plane states -p PROJECT_ID` — see available states
3. `plane members` — find member IDs for assignment
4. `plane issues create -p PROJECT_ID --name "Task" --priority high --assignee USER_ID`
5. `plane comments add -p PROJECT_ID -i ISSUE_ID "Started working on this"`