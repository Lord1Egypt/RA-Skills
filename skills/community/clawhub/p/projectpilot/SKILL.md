---
name: ProjectPilot
description: "Lightweight project management for agents. Create projects, track tasks, set priorities and deadlines."
permissions: Bash
triggers:
  - project
  - task
  - sprint
  - deadline
  - burndown
  - overdue
  - priority
  - kanban
  - todo list
  - status report
---

# ProjectPilot

Lightweight project management for agents. Track tasks, deadlines, and priorities with a zero-dependency Python CLI.

## Quick Start

```bash
# Create a project
python3 scripts/project_tracker.py init my-project

# Add tasks
python3 scripts/project_tracker.py add my-project "Design API schema" --priority H --due 2026-04-05
python3 scripts/project_tracker.py add my-project "Write docs" --priority M --assignee rc

# List tasks
python3 scripts/project_tracker.py list my-project
python3 scripts/project_tracker.py list my-project --status todo --priority H

# Update / complete
python3 scripts/project_tracker.py done my-project <task_id>
python3 scripts/project_tracker.py update my-project <task_id> --status doing

# Insights
python3 scripts/project_tracker.py summary my-project
python3 scripts/project_tracker.py burndown my-project
python3 scripts/project_tracker.py overdue my-project
python3 scripts/project_tracker.py projects
```

All paths are relative to this skill directory.

## Commands Reference

| Command | Purpose |
|---------|---------|
| `init <project>` | Create new project |
| `add <project> <task>` | Add task (opts: `--priority H/M/L`, `--due YYYY-MM-DD`, `--assignee`) |
| `list <project>` | List tasks (opts: `--status todo/doing/done`, `--priority`) |
| `update <project> <id>` | Update task fields (`--status`, `--priority`, `--due`) |
| `done <project> <id>` | Mark task complete |
| `delete <project> <id>` | Remove task |
| `summary <project>` | Stats dashboard with progress bar |
| `burndown <project>` | Visual completion progress |
| `overdue <project>` | Show past-due tasks |
| `projects` | List all projects |

## Generating Status Reports

After running `summary`, format a status report using the template in [references/pm-templates.md](references/pm-templates.md). Include completed items, in-progress work, blockers, and metrics.

## Priority Scoring

Use the RICE framework from [references/pm-templates.md](references/pm-templates.md) when the user needs to prioritize a backlog or compare features.

## Data Storage

Projects are stored as JSON in `data/projects/` under the OpenClaw workspace. Each project is a single file — easy to version, export, or share.
