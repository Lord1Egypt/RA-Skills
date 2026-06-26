---
name: orgx
description: Use when managing work with OrgX — reporting progress, requesting decisions, registering artifacts, syncing memory, checking quality gates, or viewing org status. Activates for phrases like "report progress", "request approval", "create initiative", "check orgx", "sync with orgx", "register artifact".
version: 2.1.0
user-invocable: true
tags:
  - orchestration
  - multi-agent
  - productivity
  - reporting
---

# OrgX Integration

Connect to OrgX for multi-agent orchestration, decision workflows, initiative tracking, model routing, quality gates, and structured work reporting.

## Quick Start

```bash
# Install the plugin
openclaw plugins install @useorgx/openclaw-plugin

# Or via npx
npx @useorgx/openclaw-plugin
```

After installing, pair with OrgX via the live dashboard at `http://127.0.0.1:18789/orgx/live` or set `ORGX_API_KEY` in your environment.

## MCP Tools Reference

### Work Reporting (use these regularly)

**`orgx_report_progress`** — Report what you've accomplished.
```
orgx_report_progress({
  summary: "Fixed the authentication bug and added tests",
  phase: "testing",           // researching | implementing | testing | reviewing | blocked
  progress_pct: 75,           // 0-100 (optional)
  next_step: "Run full CI suite"  // (optional)
})
```

**`orgx_request_decision`** — Ask the user to decide something before continuing.
```
orgx_request_decision({
  question: "Deploy to production now or wait for load testing?",
  context: "All unit tests pass. Load testing would take ~2 hours.",
  options: ["Deploy now", "Wait for load testing", "Deploy to staging first"],
  urgency: "medium",          // low | medium | high | urgent
  blocking: true              // pause work until decided (default: true)
})
```

**`orgx_register_artifact`** — Register a deliverable (PR, document, config, etc.).
```
orgx_register_artifact({
  name: "PR #107: Fix Vercel build size",
  artifact_type: "pr",        // pr | commit | document | config | report | design | other
  description: "Reduced function size by pruning recursive assets",
  url: "https://github.com/org/repo/pull/107"  // (optional)
})
```

### Org Status & Sync

**`orgx_status`** — View active initiatives, agent states, pending decisions, tasks.

**`orgx_sync`** — Push local memory/daily log to OrgX, receive org context back.
```
orgx_sync({
  memory: "Contents of MEMORY.md",
  dailyLog: "Today's session summary"
})
```

### Quality & Spawning

**`orgx_spawn_check`** — Check quality gate + get model routing before spawning a sub-agent.
```
orgx_spawn_check({ domain: "engineering", taskId: "..." })
// Returns: { allowed: true, modelTier: "sonnet", checks: {...} }
```

**`orgx_quality_score`** — Record quality score (1-5) for completed work.
```
orgx_quality_score({
  taskId: "...",
  domain: "engineering",
  score: 4,
  notes: "Clean implementation, good test coverage"
})
```

### Entity Management

**`orgx_create_entity`** — Create an initiative, workstream, task, decision, milestone, artifact, or blocker.

**`orgx_update_entity`** — Update status/fields on any entity.

**`orgx_list_entities`** — Query entities by type and status.

### Run Control

**`orgx_delegation_preflight`** — Score scope quality and estimate ETA/cost before execution.

**`orgx_run_action`** — Pause, resume, cancel, or rollback a run.

**`orgx_checkpoints_list`** / **`orgx_checkpoint_restore`** — List and restore run checkpoints.

## Reporting Protocol

When working on a task or initiative, report your progress to OrgX at key moments. This keeps the dashboard accurate and helps the team track your work.

### On task start
Call `orgx_report_progress` with `phase: "researching"` or `"implementing"` and a brief summary of what you're about to do.

### At meaningful progress points
Call `orgx_report_progress` at natural checkpoints: after finishing research, after a first implementation pass, after tests pass, etc. Include `progress_pct` when you can estimate it.

### When you need a human decision
Call `orgx_request_decision` with a clear question, context, and options. Set `blocking: true` if you should wait for the answer before continuing. Set urgency appropriately:
- **low** — Can wait hours/days
- **medium** — Should be decided today
- **high** — Blocking progress, needs attention soon
- **urgent** — Critical path, needs immediate attention

### When you produce a deliverable
Call `orgx_register_artifact` for anything the team should see: PRs, documents, config changes, reports, design files. Include a URL when available.

### On task completion
1. Call `orgx_report_progress` with `phase: "reviewing"` and `progress_pct: 100`
2. Call `orgx_quality_score` to self-assess your work (1-5 scale)
3. Call `orgx_update_entity` to mark the task as completed

### On blockers
Call `orgx_report_progress` with `phase: "blocked"` and describe the blocker in the summary. If you need human help, also call `orgx_request_decision`.

## Model Routing

OrgX classifies tasks for model selection:

| Task Type | Tier | Model |
|---|---|---|
| Architecture, strategy, decisions, RFCs | **opus** | `anthropic/claude-opus-4-6` |
| Implementation, code, features, docs | **sonnet** | `anthropic/claude-sonnet-4` |
| Status checks, formatting, templates | **local** | `ollama/qwen2.5-coder:32b` |

Always call `orgx_spawn_check` before spawning sub-agents to get the right model tier.

## Live Dashboard

The plugin serves a live dashboard at `http://127.0.0.1:18789/orgx/live` showing:
- **Activity Timeline** — Real-time feed of agent work with threaded session views
- **Agents/Chats** — Active sessions grouped by agent
- **Decisions** — Pending approvals with inline approve/reject
- **Initiatives** — Active workstreams and progress

## Entity API

For direct API access:
```
GET  /api/entities?type={type}&status={status}&limit={n}
POST /api/entities
PATCH /api/entities
POST /api/entities/{type}/{id}/{action}
```

Entity types: `initiative`, `workstream`, `task`, `decision`, `milestone`, `artifact`, `agent`, `blocker`

## MCP Server (mcp.useorgx.com)

For environments that support MCP servers directly (Claude Desktop, Cursor, etc.), connect to `mcp.useorgx.com` for the full suite of 26+ OrgX tools including initiative management, decision workflows, and agent orchestration.
