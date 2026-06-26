# M365 Task Manager Playbook

## Technical execution model

- API: Microsoft Graph
- Auth: delegated Device Code flow
- Token cache: local file for unattended reuse after first login

## CLI command map

- `info` - verify authenticated user and scopes
- `lists` - list Microsoft To Do lists
- `tasks:list` - read tasks from list
- `tasks:create` - create task
- `tasks:update` - patch task fields
- `tasks:delete` - remove task

## Functional guidance

### Use Microsoft To Do when
- Single user personal execution
- Fast operational capture

### Use Planner when
- Team board visibility is required
- Multi-owner orchestration is required

## Status lifecycle

- Open
- In Progress
- Blocked
- Done

## Naming convention

Pattern:
- `<project>-<date>-<person>-<action>`

Examples:
- `ops-2026-02-24-abdelkrim-burn-2-dvd-send-robert`
- `security-2026-02-24-morad-review-m365-license-assignment`
