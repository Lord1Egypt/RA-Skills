# Oz Agent REST API Reference

## Base URL
```
https://app.warp.dev/api/v1
```

## Authentication
Bearer token via API key (starts with `wk-`).
```
Authorization: Bearer <WARP_API_KEY>
```
Set `WARP_API_KEY` env var, or configure `OP_WARP_REFERENCE` to point to your 1Password vault item.

## Agent Endpoints

### POST /agent/run — Create a run
```json
{
  "prompt": "string (required unless skill specified)",
  "title": "string (optional, auto-generated if omitted)",
  "team": false,
  "skill": "repo:skill_name or org/repo:skill_name (shorthand for config.skill_spec)",
  "conversation_id": "UUID — continue existing conversation (multi-turn)",
  "interactive": false,
  "attachments": [{"filename": "string", "content": "base64", "content_type": "string"}],
  "config": {
    "name": "string — label for filtering/tracing",
    "model_id": "string — LLM model (team default if omitted)",
    "base_prompt": "string — system prompt shaping agent behavior",
    "environment_id": "string — UID of environment",
    "skill_spec": "owner/repo:skill-name or owner/repo:path/to/SKILL.md",
    "mcp_servers": {
      "<name>": {
        "warp_id": "UUID (shared MCP server)",
        "command": "string (stdio transport)",
        "args": ["string"],
        "url": "string (SSE/HTTP transport)",
        "env": {"KEY": "VALUE"},
        "headers": {"KEY": "VALUE"}
      }
    }
  }
}
```
Response (200): `{ "run_id": "string", "task_id": "string", "state": "QUEUED", "at_capacity": false }`

### GET /agent — List agents (skills)
Query params:
- `repo` — filter by repo (`owner/repo`)
- `refresh` — force cache refresh (boolean)
- `sort_by` — `name` (default) or `last_run`
- `include_malformed_skills` — include broken SKILL.md files (boolean)

Response: `{ "agents": [AgentSkill...] }`

### GET /agent/runs — List runs
Query params:
- `limit` (1-500, default 20)
- `cursor` (pagination)
- `state` (repeatable: QUEUED, PENDING, CLAIMED, INPROGRESS, SUCCEEDED, FAILED)
- `config_name` — filter by config name
- `model_id`, `creator`, `source` (LINEAR|API|SLACK|LOCAL|SCHEDULED_AGENT|WEB_APP)
- `created_after`, `created_before` (RFC3339)

Response: `{ "runs": [RunItem...], "page_info": { "has_next_page": bool, "next_cursor": "string" } }`

### GET /agent/runs/{runId} — Get run details
Response: RunItem (see below).

### POST /agent/runs/{runId}/cancel — Cancel a run
Cancels an in-progress or queued run.
Response: string (confirmation).

### GET /agent/artifacts/{artifactUid} — Get artifact
Retrieve an artifact produced by a run (PRs, files, reports).
Response: ArtifactItem with content/metadata.

## Schedule Endpoints

### POST /agent/schedules — Create schedule
```json
{
  "prompt": "string (required unless skill_spec in agent_config)",
  "cron_schedule": "string (required, cron expression e.g. '0 9 * * *')",
  "name": "string (required, human-readable label)",
  "enabled": true,
  "team": true,
  "agent_config": {
    "environment_id": "string",
    "model_id": "string",
    "base_prompt": "string",
    "skill_spec": "owner/repo:skill-name",
    "mcp_servers": { ... }
  }
}
```
Response: ScheduledAgentItem.

### GET /agent/schedules — List schedules
Response: `{ "schedules": [ScheduledAgentItem...] }`

### GET /agent/schedules/{scheduleId} — Get schedule
Response: ScheduledAgentItem.

### PUT /agent/schedules/{scheduleId} — Update schedule
Required fields: `cron_schedule`, `name`, `enabled`. Optional: `prompt`, `agent_config`.
Response: ScheduledAgentItem.

### DELETE /agent/schedules/{scheduleId} — Delete schedule
Response: confirmation.

### POST /agent/schedules/{scheduleId}/pause — Pause schedule
Response: ScheduledAgentItem (paused).

### POST /agent/schedules/{scheduleId}/resume — Resume schedule
Response: ScheduledAgentItem (active).

## Session Endpoints

### GET /agent/sessions/{sessionUuid}/redirect — Session redirect
Get the viewable URL for a session.
Response: `{ "url": "string" }`

## RunItem Object
```json
{
  "run_id": "string",
  "task_id": "string",
  "title": "string",
  "state": "QUEUED|PENDING|CLAIMED|INPROGRESS|SUCCEEDED|FAILED",
  "prompt": "string",
  "created_at": "RFC3339",
  "updated_at": "RFC3339",
  "started_at": "RFC3339 | null",
  "status_message": { "message": "string" },
  "source": "API|LINEAR|SLACK|LOCAL|SCHEDULED_AGENT|WEB_APP",
  "session_id": "UUID",
  "session_link": "URL",
  "creator": { "type": "user|service_account", "uid": "string", "display_name": "string", "email": "string" },
  "agent_config": { "name": "string", "model_id": "string", "environment_id": "string", ... },
  "request_usage": { "compute_cost": number, "inference_cost": number },
  "artifacts": [ArtifactItem...],
  "conversation_id": "UUID",
  "is_sandbox_running": boolean
}
```

## Run States
```
QUEUED → PENDING → CLAIMED → INPROGRESS → SUCCEEDED | FAILED
```

## Warp Skills via Git

Oz agents discover skills from repos configured in environments. To create a Warp skill, push a `SKILL.md` to one of these directories in the repo:

```
.agents/skills/<skill-name>/SKILL.md   (recommended)
.warp/skills/<skill-name>/SKILL.md
.claude/skills/<skill-name>/SKILL.md
```

SKILL.md format:
```markdown
---
name: skill-name
description: What this skill does and when to use it
---
Instructions for the agent...
```

Supporting files (scripts, templates) go alongside SKILL.md. Once pushed, invoke via API:
```bash
oz-api.sh run "task" --skill "org/repo:skill-name"
```

Or in config: `"skill_spec": "org/repo:skill-name"` or `"skill_spec": "org/repo:path/to/SKILL.md"`

Skills support argument placeholders (`$0`, `$1`, `$ARGUMENTS`) for parameterized invocation.

## Errors (RFC 7807)
- 400 `invalid_request`: Malformed request
- 401 `authentication_required`: Invalid/missing API key
- 403 `not_authorized`: No permission
- 404 `resource_not_found`: Run/schedule not found
- 409 `conflict`: Resource state conflict
- 422: Unprocessable entity
- 429: Rate limited (auto-retry recommended)
- `insufficient_credits`: Out of credits
- `feature_not_available`: Plan upgrade needed
- `environment_setup_failed`: Docker/repo/setup issue
- `external_authentication_required`: GitHub auth needed (follow auth_url)
- `budget_exceeded`: Spending limit hit
- `content_policy_violation`: Prompt flagged
