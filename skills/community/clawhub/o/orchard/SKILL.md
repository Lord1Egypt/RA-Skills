---
name: OrchardOS
description: Agentic project and task management plugin for OpenClaw. Persistent SQLite-backed task board with a queue runner that auto-dispatches ready tasks as subagents, REST API, native agent tools, and a web dashboard.
---

# OrchardOS

OrchardOS is an OpenClaw plugin that gives your agents a persistent task board. Create projects, add tasks, and let the built-in queue runner dispatch them as subagents automatically.

## Install

```bash
openclaw plugins install clawhub:openclaw-orchard
openclaw gateway restart
```

## Configure (optional)

Orchard works after install with the plugin entry enabled. If you want to tune models, limits, database path, or queue cadence, configure the `orchard` plugin entry in `openclaw.json`.

Common options:
- `dbPath`
- `roles.executor.model`
- `roles.architect.enabled`
- `limits.maxConcurrentExecutors`
- `queueIntervalMs`

## Agent tools

Available in every agent session after install:

| Tool | Description |
|------|-------------|
| `orchard_project_create` | Create a new project |
| `orchard_project_list` | List all projects |
| `orchard_task_add` | Add a task to a project |
| `orchard_task_list` | List tasks (filter by project, status) |
| `orchard_task_done` | Mark a task done with a summary |
| `orchard_task_block` | Mark a task blocked with a reason |
| `orchard_task_comment` | Add a comment to a task |
| `orchard_wake` | Trigger the queue runner immediately |

## REST API

Main gateway API routes use the normal OpenClaw bearer-token auth model.

| Method | Path | Description |
|--------|------|-------------|
| GET/POST | `/orchard/projects` | List / create projects |
| GET/POST | `/orchard/projects/:id/tasks` | List / add tasks |
| GET/PUT | `/orchard/tasks/:id` | Get / update task |
| POST | `/orchard/tasks/:id/comments` | Add comment |
| GET | `/orchard/tasks/:id/runs` | Run history |
| POST | `/orchard/wake` | Trigger queue runner |
| GET | `/orchard/ui` | Web dashboard |

## How it works

1. Create a project with a goal
2. Add tasks (`ready` status) via tools, API, or dashboard
3. Queue runner polls every 5 minutes (configurable), dispatches ready tasks as subagents
4. Executors use `orchard_task_done` / `orchard_task_block` to report back
5. Architect wakes when queue is empty to generate new tasks toward the project goal
