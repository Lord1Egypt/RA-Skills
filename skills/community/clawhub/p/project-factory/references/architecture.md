# Content Pipeline — Shared Architecture

This document describes the canonical architecture pattern used by all content-pipeline projects (youtube-to-wechat, trend-pipeline, etc.). Use this as the reference when bootstrapping new projects.

---

## Core Pattern

Every content pipeline follows the same 5-stage pattern:

```
Trigger → Worker → Summary → Reporter → Human
```

### Stage Map

| Stage | Responsible Script | Output | State |
|-------|-------------------|--------|-------|
| Polling / Fetching | `<project>_bot.py` | Raw data (JSONL) | `data/<pool>.jsonl` |
| Processing / Transform | `<worker>.py` | Transformed content | `data/<stage>_results/` |
| State Archival | `write_run_summary.py` | `logs/latest_run_summary.json` | Structured JSON |
| Delivery | `<reporter>.py` | Telegram message | Project group thread |
| Human Review | AK / Chief Agent | Approval / intervention | Main chat (exceptions only) |

---

## Thread Routing Convention

Each project has 1–4 logical channels inside one Telegram group. Map each to a dedicated thread_id:

| Thread Key | Purpose | Convention |
|------------|---------|------------|
| `general` | 项目公告、置顶说明、操作约定、轻量协调 | thread 1 |
| `report` | 执行细节、运行状态、定时任务结果、异常告警 | thread 2 |
| `chat` | 项目群聊天、数据汇报、Bug 修复、人工决策和排障 | thread 3 |
| `content` | 内容改写/发布详情汇报 | thread 22 (fashion) or project-specific |

New projects: assign the next available unused thread numbers and record in `config/project_routing.json`.
Do not rely on `channels.telegram.groups."*"` for new projects. Each project should have an explicit numeric `chat_id` entry and explicit topic mapping in `~/.openclaw/openclaw.json`.

Conversation isolation baseline:
- `general` topic is router-only
- `report` and `chat` topics should be owned by a dedicated project assistant
- route config should bind `chat_id -> project_id`, set `contextGate=true`, and declare `topicOwnership`
- project groups are not just delivery surfaces; they are project-scoped conversation surfaces

For shared routing groups, add one more layer:
- every operational topic should also declare `workflowScope`
- `ownerAgent` and `projectScope` may differ from topic label
- extract schema first, mutate runtime later

---

## Summary Schema

All projects use `projects/shared/SUMMARY_SCHEMA.md` as the schema base. Required fields:

```json
{
  "schemaVersion": 1,
  "projectKey": "<project_key>",
  "runId": "<YYYY-MM-DDTHH-MM-SS>",
  "status": "success|warning|error",
  "generatedAt": "<ISO timestamp>",
  "runDate": "<YYYY-MM-DD>",
  "source": "<script_name>",
  "<stage>": { ... }
}
```

Per-stage fields (trend pipeline example):
```json
{
  "trend": { "total": 0, "new": 0, "skipped": 0 },
  "content": { "processed": 0, "draftedCount": 0, "publishFailures": 0 }
}
```

---

## Pipeline Script Convention

Every `run_pipeline.sh` must follow this template:

```bash
#!/bin/bash
set -euo pipefail

ROOT="/path/to/project"
LOG_DIR="$ROOT/logs"
RUN_LOG="$LOG_DIR/daily_pipeline.log"
LOCK_DIR="$ROOT/.locks/daily_pipeline.lock"

finish() {
  PIPELINE_STATUS=$?
  python3 "$ROOT/scripts/write_run_summary.py \
    --trend-log <...> \
    --content-log <...> \
    --summary <...> \
    --run-date <...>" >> "$RUN_LOG" 2>&1 || true
  CRON_JOB_ID="<project_key>" python3 "$ROOT/scripts/pipeline_reporter.py" <...> >> "$RUN_LOG" 2>&1 || true
}

trap 'finish; cleanup; exit 143' TERM
trap 'finish; cleanup' EXIT

# ... pipeline stages ...
```

Key requirements:
- `finish()` function runs summary + reporter on ANY exit (normal, error, SIGTERM)
- `LOCK_DIR` prevents concurrent runs
- All stage logs tee to `$LOG_DIR/.stage_<date>.log`
- `RUN_LOG` captures full pipeline stdout + stderr

---

## Routing Loader

Each project uses `projects/shared/project_routing_loader.py` to read `config/project_routing.json`. Project scripts should never hardcode chat IDs.

```python
from project_routing_loader import load_project_routing
route = load_project_routing(
    project_key='<project_key>',
    default_routing_group='<group>',
    default_chat_id='<chat_id>',
    default_target='<target>'
)
thread_id = route.get('<thread_key>ThreadId')  # e.g. videoReportThreadId
```

---

## Cron Job Registration

Use OpenClaw cron API (not system crontab):

```
openclaw cron add \
  --name "<project>: daily run" \
  --schedule "0 9 * * *" \
  --session-target isolated \
  --payload.agentTurn.message "bash projects/<project>/scripts/run_pipeline.sh" \
  --delivery.announce --to "<chat_id>"
```

Or via API:
```python
cron(action='add', job={
  'name': '<project>: daily run',
  'schedule': {'kind': 'cron', 'expr': '0 9 * * *', 'tz': 'Asia/Shanghai'},
  'sessionTarget': 'isolated',
  'payload': {'kind': 'agentTurn', 'message': '...', 'timeoutSeconds': 1200},
  'delivery': {'mode': 'announce', 'channel': 'telegram', 'to': '<chat_id>'}
})
```

---

## Anti-Patterns to Avoid

1. **Never chain projects**: youtube-to-wechat (Workflow A) and trend-pipeline (Workflow B) must NEVER auto-trigger each other's workers. Each is independent.
2. **Never skip the questionnaire**: required human parameters (bot_token, chat_id) must come from the human.
3. **Never use main chat as routine project output**: project reports go to project group; main chat is for escalations only.
4. **Never write one-off reporters**: every reporter must read from `latest_run_summary.json`, never from live execution state.
5. **Never skip the finish() trap**: without it, SIGTERM from gateway timeout kills reporting and leaves the run un-archived.
