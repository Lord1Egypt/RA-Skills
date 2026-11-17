# Helios Kanban REST API Reference

Base URL: `$HELIOS_KANBAN_URL` (no trailing slash). All paths under `/api`.

Response envelope:

```json
{ "success": true, "data": { ... }, "message": null, "error_data": null }
```

Read `.data` on success; read `.message` on failure.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness check |
| GET | `/info` | Server/user config (includes default `executor_profile`) |
| GET | `/projects` | List projects (`description`, repos via separate call) |
| POST | `/projects` | Create project |
| GET | `/projects/{project_id}` | Get project |
| PUT | `/projects/{project_id}` | Update project (`name`, `description`) |
| GET | `/projects/{project_id}/repositories` | List repos |
| GET | `/repos/{repo_id}` | Repo details (`default_target_branch`) |
| GET | `/repos/{repo_id}/branches` | List branches |
| GET | `/tasks?project_id={uuid}` | List tasks |
| POST | `/tasks` | Create task |
| GET | `/tasks/{task_id}` | Get task |
| PUT | `/tasks/{task_id}` | Update task |
| DELETE | `/tasks/{task_id}` | Delete task |
| POST | `/tasks/create-and-start` | Create task + start agent |
| POST | `/task-attempts` | Start agent on existing task |
| GET | `/task-attempts?task_id={uuid}` | List workspaces for task |
| POST | `/task-attempts/summary` | Workspace summaries (diff/approvals) |
| POST | `/task-attempts/{workspace_id}/stop` | Stop running agent |
| GET | `/sessions?workspace_id={uuid}` | List sessions |
| POST | `/sessions/{session_id}/follow-up` | Send follow-up prompt |
| POST | `/sessions/{session_id}/queue` | Queue follow-up while running |
| GET | `/approvals` | List pending approvals |
| POST | `/approvals/{id}/respond` | Approve / deny |

## Default executor profile

```bash
hk info | jq '.config.executor_profile'
```

## Create project

```json
POST /api/projects
{
  "name": "My project",
  "description": "What this project is for",
  "repositories": [
    { "display_name": "my-repo", "git_repo_path": "/abs/path/on/server" }
  ]
}
```

`git_repo_path` is a path on the kanban **server** host, not the bot host. `repositories` may be empty.

```bash
hk projects create "My project" --repo-path /abs/path/on/server
```

## Project description (for agents)

Projects may include a human/agent-facing `description`. Use it (with linked repo names) to choose `project_id` before creating tasks.

```bash
hk projects
hk projects update <project_id> --description "Helios Kanban app — create tasks here for UI/API work"
```

```json
PUT /api/projects/{project_id}
{ "description": "What this project is for" }
```

Pass `""` to clear. Omit the field to keep the existing value.

```json
GET /api/info
{
  "config": {
    "executor_profile": {
      "executor": "CODEX",
      "variant": "DEFAULT"
    }
  }
}
```

Use this when starting an agent unless the user names a specific executor. Fresh installs default to `CLAUDE_CODE` until changed in Settings → Agents.

## Create task

```json
POST /api/tasks
{
  "project_id": "uuid",
  "title": "Fix login bug",
  "description": "Optional details",
  "status": "todo",
  "priority": "high",
  "iteration": "260717"
}
```

`priority` is optional: `urgent` | `high` | `medium` | `low` (default `medium`).

## Update task

```json
PUT /api/tasks/{task_id}
{
  "status": "inprogress",
  "priority": "urgent",
  "title": "New title",
  "description": "Updated desc",
  "iteration": "260717"
}
```

## Start agent (existing task)

```json
POST /api/task-attempts
{
  "task_id": "uuid",
  "executor_profile_id": {
    "executor": "CODEX",
    "variant": "DEFAULT"
  },
  "repos": [
    { "repo_id": "uuid", "target_branch": "main" }
  ]
}
```

Prefer reading `executor` / `variant` from `GET /api/info` → `config.executor_profile` rather than hardcoding.

`target_branch` is the base branch. Prefer `GET /api/repos/{repo_id}` → `default_target_branch` when the user does not name a branch.

## Create and start (one shot)

```json
POST /api/tasks/create-and-start
{
  "task": {
    "project_id": "uuid",
    "title": "Fix login bug",
    "description": "...",
    "priority": "high",
    "iteration": "260717"
  },
  "executor_profile_id": {
    "executor": "CODEX",
    "variant": null
  },
  "repos": [
    { "repo_id": "uuid", "target_branch": "develop" }
  ]
}
```

## Cancel vs delete vs stop

| Action | Method | Path / CLI |
|--------|--------|------------|
| Soft cancel | `PUT` | `/tasks/{id}` `{ "status": "cancelled" }` → `hk tasks cancel` |
| Hard delete | `DELETE` | `/tasks/{id}` → `hk tasks delete` (confirm first) |
| Stop agent | `POST` | `/task-attempts/{workspace_id}/stop` → `hk stop` |

## Follow-up

```json
POST /api/sessions/{session_id}/follow-up
{
  "prompt": "请补充单元测试",
  "executor_profile_id": { "executor": "CODEX", "variant": null }
}
```

If the agent is already running, queue instead:

```json
POST /api/sessions/{session_id}/queue
{
  "message": "请补充单元测试",
  "executor_profile_id": { "executor": "CODEX" }
}
```

`hk follow-up` picks queue vs follow-up automatically.

## Approvals

```json
GET /api/approvals
→ [{ "approval_id", "tool_name", "execution_process_id", "is_question", ... }]

POST /api/approvals/{approval_id}/respond
{
  "execution_process_id": "uuid",
  "status": { "status": "approved" }
}
```

Deny: `{ "status": "denied", "reason": "optional" }`. Question-type approvals (`is_question: true`) need the Web UI for structured answers.

## Status / summary

```json
POST /api/task-attempts/summary
{ "archived": false }
```

Returns per-workspace diff stats, `has_pending_approval`, latest process status. `hk status <task_id>` composes task + workspaces + matching summaries.

## Tags (`@tagname`)

`GET /api/tags` returns `{ id, tag_name, content }`.

In `hk tasks create/update --desc` and `hk follow-up`, `@tagname` is expanded to the tag content (same as MCP).

```bash
hk tags
hk tasks create "Fix" --desc "Follow @coding-standards"
```

## Executors (from default_profiles.json)

`CLAUDE_CODE`, `AMP`, `GEMINI`, `CODEX`, `COPILOT`, `REASONIX`, `CURSOR_AGENT`, `QWEN_CODE`, `OPENCODE`, `ECHO`, and others.

Common variants: `DEFAULT`, `PLAN`, `OPUS`, `APPROVALS`, `FLASH`, `PRO`, `HIGH`, `MAX`.

## Origin header

If accessing via a custom domain behind reverse proxy, server must have `VK_ALLOWED_ORIGINS` set. Direct IP/Tailscale access typically works without it.
