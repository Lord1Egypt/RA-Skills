---
name: oz
description: Dispatch coding tasks to Warp Oz cloud agents and chain them into multi-agent pipelines — all from chat. Includes a bash wrapper covering every Oz API endpoint (runs, schedules, artifacts, agents) and a Python pipeline orchestrator that chains specialized agents (e.g., architect → developer → security → red-teamer) with automatic severity-based retry loops. Use when you want to kick off cloud coding agents, poll run status, manage cron schedules, run multi-turn conversations in a shared sandbox, or orchestrate multi-agent review pipelines. NOT for local Warp terminal usage.
metadata:
  {
    "openclaw":
      {
        "requires": {
          "bins": ["curl", "jq", "python3"],
          "env": ["WARP_API_KEY"]
        },
        "credentials": [
          {
            "name": "WARP_API_KEY",
            "description": "Warp Oz API Bearer token (wk-*). Get from app.warp.dev → Settings → API Keys.",
            "required": true,
            "alternatives": ["OP_WARP_REFERENCE"]
          },
          {
            "name": "OP_WARP_REFERENCE",
            "description": "1Password secret reference for the Warp API key (e.g., op://vault/item/field). Requires the op CLI. Used as fallback when WARP_API_KEY is not set.",
            "required": false
          }
        ],
        "optionalBins": ["op"]
      }
  }
---

# Oz Cloud Agent Orchestration

Turn your OpenClaw agent into a development team manager. Dispatch coding tasks to Warp Oz cloud agents from chat, chain them into multi-stage pipelines, and get PRs back — no IDE required.

**What you get:**
- `oz-api.sh` — bash wrapper covering every Oz API endpoint (runs, polls, schedules, artifacts, agents)
- `orchestrator.py` — Python pipeline runner that chains agents with automatic severity-based retry loops
- `references/agent-roles.md` — battle-tested base prompts for 6 specialized agent roles

**Example pipeline:** "Build a market maker" →
1. **Architect** designs the system → ARCHITECTURE.md + PR
2. **Trading engineer** implements it → 10 modules, 36 tests, PR
3. **Security engineer** reviews → finds 1 critical, 2 high
4. **Red teamer** attacks → finds 2 more exploits
5. Orchestrator auto-loops developer on critical findings

All from a single command. Each agent runs in an isolated Docker container with your repo cloned.

## Setup

1. Get a Warp API key from app.warp.dev → Settings → API Keys
2. `export WARP_API_KEY=wk-...` (or set `OP_WARP_REFERENCE` for 1Password)
3. Create an environment at oz.warp.dev and note the ID

## Quick Start

```bash
# Kick off a single agent
oz-api.sh run "Implement user authentication" --env YOUR_ENV_ID --name developer

# Poll until done
oz-api.sh poll <run_id>

# Run a full pipeline (architect → developer → security → red-teamer)
python3 orchestrator.py \
  --env YOUR_ENV_ID \
  --task "Build a REST API for user management" \
  --stages architect,developer,security-engineer,red-teamer \
  --skill-prefix owner/repo-name
```

## Commands

```bash
# Runs
oz-api.sh run "prompt" [--env ID] [--name N] [--base-prompt T] [--model M] [--title T] [--team] [--skill S] [--conversation-id ID] [--interactive]
oz-api.sh status <run_id>
oz-api.sh list [--state S] [--limit N] [--name N] [--source S]
oz-api.sh poll <run_id> [--interval 10] [--timeout 600]
oz-api.sh cancel <run_id>

# Artifacts & sessions
oz-api.sh artifacts <artifact_uid>
oz-api.sh agents
oz-api.sh session-link <session_uuid>

# Schedules
oz-api.sh schedule-create "prompt" --cron "EXPR" --name "N" [--env ID] [--base-prompt T] [--disabled]
oz-api.sh schedule-list
oz-api.sh schedule-get <id>
oz-api.sh schedule-update <id> --cron "EXPR" --name "N" [--prompt T] [--env ID] [--enabled true|false]
oz-api.sh schedule-delete <id>
oz-api.sh schedule-pause <id>
oz-api.sh schedule-resume <id>
```

## Multi-Turn Conversations

Use `--conversation-id` to continue where a previous run left off (same sandbox, same context):
```bash
# First run returns conversation_id in response
oz-api.sh run "Build the auth module" --env ID --name developer
# Continue in same session
oz-api.sh run "Now add rate limiting" --conversation-id <conversation_id>
```

## Pipeline Orchestrator

`orchestrator.py` chains agent runs in sequence with:
- **Automatic context forwarding** — each stage gets the previous stage's summary + session link
- **Severity detection** — parses status messages for CRITICAL/HIGH/MEDIUM/LOW findings
- **Retry loops** — auto-loops back to the developer when reviewers find critical/high issues (configurable max retries)
- **Shared sandbox** — optional `conversation_id` sharing so agents continue in the same environment
- **JSON summary** — outputs structured pipeline results to stdout

```bash
python3 orchestrator.py \
  --env YOUR_ENV_ID \
  --task "Your task description" \
  --stages architect,developer,security-engineer,red-teamer \
  --skill-prefix owner/repo-name \
  --poll-interval 15 \
  --poll-timeout 5400 \
  --max-retries 2 \
  --no-conversation  # optional: isolate each stage's sandbox
```

## Custom Agent Roles

Define specialized agents by pushing `.agents/skills/<name>/SKILL.md` to your repo. Oz auto-discovers them. See `references/agent-roles.md` for 6 production-tested role prompts (architect, trading-engineer, quant, security-engineer, red-teamer, risk-manager).

## Known Limitations

- Cancel returns 422 on Docker sandbox workers (Warp-side limitation)
- Artifacts endpoint returns 500 (not 404) for nonexistent UIDs
- No API endpoint to list/manage environments — use oz.warp.dev GUI

## Reference

- **API endpoints & schemas:** `references/api.md`
- **Agent role base prompts:** `references/agent-roles.md`
- **Creating Warp skills in repos:** `references/api.md` → "Warp Skills via Git" section
