---
name: "project-orchestration"
description: "Complete project orchestration: model routing, coding workflow, scripts, session logging, decision tracking, price checks"
homepage: "https://clawhub.com/packages/project-orchestration"
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["bash", "curl", "python3"] },
      "description": "Full-stack AI project orchestration: model management, routing, session logging, decision tracking, price monitoring, project scaffolding, and a real-time dashboard. Designed as a thin index skill — SKILL.md is ~5KB, all detail in on-demand files."
    }
  }
---

# Genor's Project Orchestration

## Core Principles
1. **Repowise First** — Never touch code without codebase intelligence
2. **Plan Before Act** — `update_plan` for anything beyond one edit
3. **Verify Before Claim** — No completion claim without fresh evidence
4. **Self-Review** — Every output gets audited before delivery
5. **Fail Gracefully** — Every step has a fallback chain
6. **Document Everything** — Log sessions, decisions, and architecture

## Data Directory
All private data (models, sessions, prices) lives outside the skill.
Set `ORCHESTRATOR_DATA_DIR` to point to your data directory.
Default: `../../orchestrator-data/` from the skill root (i.e. `<workspace>/orchestrator-data/`)

### File Naming Convention
All generated files use consistent, sortable naming for cross-session compatibility:

| Location | Format | Example |
|----------|--------|--------|
| `sessions/` | `YYYY-MM-DD-HHMM-<project-slug>-<task-slug>.md` | `2026-06-08-1134-project-orchestration-publish.md` |
| `projects/` | `<project-slug>-<path-slug>.md` | `kfinance-projects-kfinance.md` |
| `session_log.md` | Flat table (append-only quick reference) | — |
| `models.json` | JSON inventory | — |
| `price_changes.log` | Flat log (append-only) | — |
| Per-project `.planning/ADRs/` | `YYYY-MM-DD-<title-slug>.md` | `2026-06-08-use-postgres.md` |

### Cross-Session Resume
Session state files in `sessions/` persist across OpenClaw sessions. When a conversation is compacted or a new session starts, the LLM can read the last session state file to continue where it left off — no dependency on conversation history.

## 🆕 Fresh Installation — First-Run Onboarding
If this is a fresh skill install with no data yet, run onboarding:
```
bash {baseDir}/scripts/onboard.sh
```
or ask the LLM: **"Set up orchestrator"** or **"/project-orchestration onboard"**

This walks through:
1. Data directory setup — where to store config
2. Provider discovery — what services you have
3. Model cataloguing — what models you use
4. Project discovery — existing projects
5. Routing rules — initial routing table
6. Cron setup — nightly price checks
7. Logging — first session recorded

If you're in an LLM session, the LLM will guide you through each step.

## 🆕 Project Onboarding
When starting a new project or adding an existing one:
```
bash {baseDir}/scripts/init-project.sh <project-path> <Project Name> [stack]
```
or ask the LLM: **"Start project <name>"**

This creates `.planning/` with:
- `CONFIG.md` — project config, ports, tech stack
- `STATE.md` — current state tracker
- `ROADMAP.md` — planned work
- `REQUIREMENTS.md` — requirements
- `ADRs/` — architecture decisions

For existing projects, the LLM will also run Repowise/scan, detect tech stack, and initialise the project in the orchestrator.

## Slash Commands
When invoked via `/project-orchestration`, interpret the subcommand:

| Command | Action |
|---------|--------|
| `/project-orchestration onboard` | Full fresh-install onboarding |
| `/project-orchestration webui` | Start dashboard: `bash {baseDir}/dashboard/serve.sh` |
| `/project-orchestration project <path> [name]` | Onboard a project (new or existing) |
| `/project-orchestration status` | Show orchestration state |
| `/project-orchestration resume <id>` | Resume session: `bash {baseDir}/scripts/resume-session.sh <id>` (id = filename, partial match, or 'last') |
| `/project-orchestration check-prices` | Check prices: `bash {baseDir}/scripts/check-prices.sh` |
| `/project-orchestration log-session <project> <task> <model> <status> [notes]` | Log a session run |
| `/project-orchestration log-decision <path> <title> <context> <decision> [alt] [cons]` | Log an architecture decision |

## Quick Scripts

### Active Tools (do real work)
| Script | What it does |
|--------|-------------|
| `bash {baseDir}/scripts/onboard.sh` | Fresh-install onboarding (interactive) |
| `bash {baseDir}/scripts/init-project.sh <path> <name> [stack]` | Scaffold a new project |
| `bash {baseDir}/scripts/log-session.sh ...` | Log a session run (with full state for resume) |
| `bash {baseDir}/scripts/log-decision.sh ...` | Log an architecture decision |
| `bash {baseDir}/scripts/check-prices.sh` | Check cloud model prices |
| `bash {baseDir}/scripts/discover-models.sh` | Probe providers for models |
| `bash {baseDir}/scripts/test-model.sh <id>` | Check model endpoint connectivity |
| `bash {baseDir}/scripts/resume-session.sh <id>` | Resume a previous session (id = filename, partial match, or 'last') |
| `bash {baseDir}/dashboard/serve.sh` | Start orchestration dashboard |

### Guidance Scripts (print instructions for OpenClaw session tools)
| Script | What it does |
|--------|-------------|
| `bash {baseDir}/scripts/show-tree.sh` | Show data dir state + OpenClaw tool guidance |
| `bash {baseDir}/scripts/find-stuck.sh` | Show how to find stuck subagents from session |
| `bash {baseDir}/scripts/cleanup-stale.sh` | Show how to clean stale subagents from session |
| `bash {baseDir}/scripts/find-stray.sh` | Show how to find stray subagents from session |

## On-Demand Reading
When you need detailed instructions, read the relevant file:
- `{baseDir}/README.md` — Full documentation (all procedures)
- `{baseDir}/ROUTING.md` — Model routing table template
- `$ORCHESTRATOR_DATA_DIR/models.json` — Your model inventory
- `$ORCHESTRATOR_DATA_DIR/session_log.md` — Quick reference session history
- `$ORCHESTRATOR_DATA_DIR/sessions/` — Detailed session state files (for resume)

## Using External Skills
For specialised tasks, use whatever skills are available in your instance.
Always fall back to built-in tools (`edit`, `exec`, `read`, `web_search`, `web_fetch`, `browser`) when specialised skills are unavailable.

## Prompt Injection
Every spawned sub-agent or Cursor session MUST include:
```
IMPORTANT: Follow Genor's Project Orchestration conventions:
- Repowise first (or exec find as fallback)
- Plan before coding (update_plan or mental plan)
- Verify before claiming (build, test, screenshot, vision Q&A)
- Self-review your output before returning
- Fallback chains: if a tool is unavailable, use the next fallback
- Document decisions, log sessions
```
