# Genor's Project Orchestration — Full Documentation

> Read this file when you need detailed instructions for any orchestration task.
> The SKILL.md contains quick-reference pointers; this file has the full procedures.
> All private data (models, sessions, prices) lives in your `orchestrator-data/` directory.
> Set `ORCHESTRATOR_DATA_DIR` to point there, or it defaults to `../../orchestrator-data/` from the skill (i.e. `<workspace>/orchestrator-data/`).
>
> **File naming convention:**
> - `sessions/YYYY-MM-DD-HHMM-<project>-<task-slug>.md` — session state files
> - `projects/<ProjectName>-<path-hash>.md` — project registrations
> - `session_log.md` — quick reference table
> - `models.json` — model inventory
> - `price_changes.log` — price tracking
> - Per-project `.planning/ADRs/YYYY-MM-DD-<title-slug>.md` — architecture decisions
>
> **Cross-session resume:** Session state files persist across OpenClaw sessions. Use `bash scripts/resume-session.sh <id>` to continue where you left off.

---

## Table of Contents
1. [Fresh Installation Onboarding](#1-fresh-installation-onboarding)
2. [Model Management](#2-model-management)
3. [Project Onboarding](#3-project-onboarding)
4. [Planning & Design](#4-planning--design)
5. [Execution](#5-execution)
6. [Verification & Review](#6-verification--review)
7. [Logging & Tracking](#7-logging--tracking)
8. [Debugging & Fixes](#8-debugging--fixes)
9. [Quality Gates](#9-quality-gates)
10. [Tool Fallback Master Table](#10-tool-fallback-master-table)

---

## 1. Fresh Installation Onboarding

> Follow this procedure when the skill is first installed. The LLM drives this interactively — you talk, it probes, you confirm.
> Skip this if you already have data in `$ORCHESTRATOR_DATA_DIR`.

### 1.1 Detection
On first load, the LLM checks:
- Does `$ORCHESTRATOR_DATA_DIR` exist or is `ORCHESTRATOR_DATA_DIR` set?
- Does `models.json` exist with catalogue data?
- If neither → **fresh install detected** → start onboarding.

### 1.2 Welcome & Overview
```
Welcome to Genor's Project Orchestration!

This skill helps you:
• Manage all your AI models in one inventory
• Route tasks to the right model automatically
• Log sessions, decisions, and project state
• Check cloud pricing and avoid bill surprises
• Bootstrap projects with docs, ADRs, and plans

Let's get you set up. This takes about 5-10 minutes.
```

### 1.3 Data Directory Setup
Find or create the data directory:
```
# Step-by-step:
1. Check if ORCHESTRATOR_DATA_DIR is already set
2. If not, ask the user where to store data
3. Default: <workspace>/orchestrator-data/
4. Create the directory
5. Log: "Data directory: $ORCHESTRATOR_DATA_DIR"
```

### 1.4 Provider Discovery
Probe every provider you can reach:

| Check | What to do |
|-------|-----------|
| **OpenRouter** | `web_fetch https://openrouter.ai/api/v1/key` or ask for API key |
| **LM Studio** | `curl -s --max-time 3 http://localhost:1234/v1/models` |
| **OpenCode** | Check `opencode` CLI, ask about subscription |
| **Cursor** | Check `cursor` CLI, ask about subscription |
| **Local GPU** | Probe GPU, VRAM, CUDA version |
| **Other endpoints** | Ask: any other local/remote endpoints? |

For each provider found, ask the user:
```
Found: OpenRouter
→ What's your typical monthly spend?
→ Any models you specifically use or avoid?
```

### 1.5 Model Cataloguing
For each discovered model, collect:
- **id** — model identifier
- **name** — display name
- **provider** — where it runs
- **host** — which machine/endpoint
- **context_window** — max context
- **speed_rating** — slow/medium/fast
- **agent_ready** — can it run tools?
- **user_notes** — your impressions

Walk through one by one:
```
Model: deepseek-v4-flash (OpenRouter)
Context: 128K | Speed: fast | Cost: $0.15/M input

How would you rate this for:
  • Coding? [primary/acceptable/avoid]
  • Research? [primary/acceptable/avoid]
  • Creative? [primary/acceptable/avoid]
  • Vision? [yes/no]
```

Use the helper script for bulk tasks:
```
bash scripts/discover-models.sh  # probe providers
```

### 1.6 Routing Rules
After cataloguing, generate initial routing rules:
```
For each task type (coding, research, creative, vision, quick):
  → Assign primary model, fallback 1, fallback 2, last resort
  → Add to $ORCHESTRATOR_DATA_DIR/models.json as "routes"
  → Write human-readable summary to MODEL_CATALOG.md
```

### 1.7 Project Discovery
Check common project locations:
```
Look for:
  ~/projects/
  ~/code/
  ~/src/
  any .planning/ or .git directories

For each found:
  → Ask: "Would you like to onboard this project?"
  → If yes: run project onboarding (section 3)
  → If no: skip
```

### 1.8 Price Check Cron
Ask if they want nightly price checks:
```
→ "Would you like me to set up nightly price checks at 2 AM?"
→ If yes: install cron job via cron tool
→ If no: skip, they can run manually
```

### 1.9 Dashboard Test
Offer to start the dashboard:
```
→ "Want to test the orchestration dashboard?"
→ If yes: bash dashboard/serve.sh → open browser
→ If no: skip
```

### 1.10 Summary & Logging
After all steps, write a summary:
```
═══ Onboarding Complete ═══

Data directory: $ORCHESTRATOR_DATA_DIR
Providers:      OpenRouter, LM Studio, ...
Models:         12 catalogued (8 active, 4 fallback)
Projects:       3 onboarded
Price checks:   Nightly at 2 AM
Dashboard:      Ready on port 8766

Try these next:
• "/project-orchestration status" — see your setup
• "/project-orchestration project <path>" — onboard a project
• "Start project MyThing" — new project scaffold
```

Log the session:
```
bash scripts/log-session.sh orchestrator "Fresh install onboarding" "-" complete "X models, Y providers, Z projects"
```

### 1.11 Re-Onboarding
Run this again later by:
```
bash scripts/onboard.sh          # re-runs discovery + interview
bash scripts/onboard.sh --force # force full re-onboarding
```

### 1.12 Data Directory
All persistent data lives outside the skill in `orchestrator-data/`:

```
orchestrator-data/
├── models.json         — Your model inventory
├── session_log.md      — Session run history
├── price_changes.log   — Price change history
├── MODEL_CATALOG.md    — Generated model catalog
└── projects/           — Per-project data
```

Override with: `export ORCHESTRATOR_DATA_DIR=/path/to/your/data`

### 1.13 Price Check
Cloud model pricing changes frequently. Run:
```
bash scripts/check-prices.sh
```
A nightly cron job can be configured to run this automatically.

---

## 2. Model Management

### 2.1 Model Cataloguing Procedure
When new models are added to your OpenClaw config:

**Phase 1: Discover** — Read OpenClaw config, probe LM Studio endpoints, check provider APIs
**Phase 2: Interview** — Go through each uncatalogued model with the user
**Phase 3: Research** — Web search + fetch benchmarks for each model
**Phase 4: Synthesize** — Combine into `models.json` in your data directory
**Phase 5: Route** — Update routing rules based on new catalogue

### 2.2 Model Routing
Consult `ROUTING.md` for the routing table. Model routing decisions depend on:
- Task type (coding, research, creative, vision, etc.)
- Model availability (free tier limits, local hardware status)
- Cost considerations (subscription caps, pay-per-token budgets)

### 2.3 Resource Awareness
Before spawning a subagent, check:
- `session_status` for current model and usage
- Provider health (LM Studio endpoints, OpenRouter availability)
- Quota/rate limits for free tier models
- Fallback chain if primary model fails

---

## 3. Project Onboarding

> Follow this when starting a new project or adding an existing one to the orchestrator.
> This creates the full documentation scaffold + sets up codebase intelligence.

### 3.1 Detection
On first mention of a project, the LLM checks:
- Does `$ORCHESTRATOR_DATA_DIR/projects/<project-name>/` exist?
- Does the project directory have `.planning/`?
- If not → **project needs onboarding** → start procedure.

### 3.2 Quick Start
```
# New project:
bash scripts/init-project.sh ~/projects/my-app "My App" "nextjs,shadcn,postgres"

# Existing project (just add planning):
bash scripts/init-project.sh ~/projects/legacy-app "Legacy App"
```

Or ask the LLM:
```
→ "Start project MyApp"
→ "Onboard project ~/projects/my-app as My App"
→ "Add planning to this existing project"
```

### 3.3 Step-by-Step LLM Procedure

#### Step 1: Project Info
Collect from the user:
```
- Project path (where does it live?)
- Project name (display name)
- Tech stack (what are they using?)
- What does it do? (one-line summary)
- Is it new or existing?
```

#### Step 2: Scaffold Planning Directory
```
bash scripts/init-project.sh <path> "<Name>" "<stack>"

Creates:
  .planning/
  ├── CONFIG.md         — ports, env vars, build commands
  ├── STATE.md          — current state, what's been done
  ├── ROADMAP.md        — planned work with priorities
  ├── REQUIREMENTS.md   — functional + non-functional
  ├── ADRs/             — architecture decision records
  └── AUDIT.md          — audit findings (when applicable)
```

#### Step 3: Codebase Intelligence (for existing projects)
```
Primary:  Run repowise if available
Fallback: exec find . -type f | head -200 (list all files)
Fallback: Check package.json, requirements.txt, Cargo.toml

→ Detect tech stack from config files
→ List key directories and entry points
→ Note test framework, build system, deployment config
```

#### Step 4: Requirement Gathering
Prompt the user:
```
→ "What does this project do?" (capture in REQUIREMENTS.md)
→ "Who is it for?"
→ "What are the current pain points?"
→ "Any key constraints?" (performance, security, timeline)
```

For new projects, also capture:
```
→ "What's the first feature you want to build?"
→ "Any architectural preferences?"
→ "Deployment target?"
```

#### Step 5: Architecture Documentation
```
Check if ADRs exist:
  → If no: create ADRs/ directory
  → If yes: read existing ADRs for context

Create initial ADRs for any early decisions:
  bash scripts/log-decision.sh <path> \
    "<Title>" "<Context/Why>" "<Decision>" \
    "[Alternatives]" "[Consequences]"

Update CONFIG.md with detected or confirmed config:
  - Port numbers
  - Environment variables
  - Build and run commands
  - Database URLs
  - External service dependencies
```

#### Step 6: Track in Orchestrator
```
Log the project to the orchestrator:
  → Update $ORCHESTRATOR_DATA_DIR/projects/<name>/
  → Add entry to project index if tracking multiple projects

Register the project for session logging:
  bash scripts/log-session.sh <project> "Project onboarding" "-" complete

Log key decisions:
  bash scripts/log-decision.sh <path> "Tech stack: <X>" ...
  bash scripts/log-decision.sh <path> "Architecture: <Y>" ...
```

#### Step 7: Summary
```
═══ Project Onboarding Complete ═══

Project:  My App
Path:     ~/projects/my-app/
Stack:    Next.js 15, shadcn/ui, PostgreSQL
State:    Requires/Roadmap are set up, ADRs ready

What's next:
• "Plan the first feature for MyApp"
• "Add ADR for database choice"
• "Run audit on MyApp"
```

### 3.4 Existing Projects — Additional Steps
For projects that already have code:

#### 3.4.1 Architecture Audit
```
- Run repowise or scan for:
  - Dependency structure
  - Dead code candidates
  - Circular dependencies
  - Test coverage gaps
- Write findings to AUDIT.md
```

#### 3.4.2 Cost/Benefit Assessment
```
- What's the codebase size? (# files, LOC)
- Build time?
- Test suite speed?
- Deployment complexity?
- Document in CONFIG.md under "project health"
```

#### 3.4.3 Quick Wins Log
```
Create a "Quick Wins" section in ROADMAP.md:
  - Low-effort, high-impact improvements
  - Tech debt that keeps biting
  - Documentation gaps
```

### 3.5 Project Health Checks
Include in every project's `.planning/CONFIG.md`:
```
## Health
- Build: [passing/failing]
- Tests: [N passing, N failing]
- Coverage: [%]
- Audit: [date]
- Last deployed: [date]
```

### 3.6 Research Phase
1. **Repowise first** — if the project exists, index + search. Fallback: `exec find` for file listing
2. **Web research** — library APIs, best practices, patterns. Fallback: `web_fetch`
3. **Memory search** — similar past work, decisions made. Fallback: `lcm_grep`
4. **Decision log** — capture every significant choice as an ADR

---

## 4. Planning & Design

### 4.1 The Plan Tool — MANDATORY
Always call `update_plan` for anything beyond a single read/edit. One step `in_progress` at a time.
**Fallback:** If `update_plan` fails, proceed with mental plan and note it.

### 4.2 Architecture Decisions
For any significant design choice, log an ADR:
```
bash scripts/log-decision.sh ~/projects/<name> "<title>" "<context>" "<decision>" "<alternatives>" "<consequences>"
```

### 4.3 Work Sizing
Break work into units that fit ONE ACP session (~200K tokens):
- Small: 1-3 files → one-shot Cursor
- Medium: 3-8 files → one-shot Cursor with detailed spec
- Large: 8+ files → decompose into parallel waves

---

## 5. Execution

### 5.1 Decision Matrix

| Scenario | Primary | Fallback |
|---|---|---|
| Single-line edit | `edit` tool | `exec sed` |
| Multi-file change (3+) | Cursor ACP one-shot | Manual `edit` serially |
| Deep research | Sub-agent | Web search yourself |
| Debugging | Diagnose protocol (section 8) | Read + mental trace |
| UI/design work | Available UI tools from installed skills | Manual |
| Testing | Available testing tools from installed skills | Manual |
| Image gen / music | Dedicated gen tools | Signal "can't do this" |

### 5.2 Cursor Protocol

#### Methods
1. **Cursor ACP:** `sessions_spawn({ runtime: "acp", agentId: "cursor", mode: "run" })`
2. **Cursor CLI:** `cursor --agent "task description"`

#### Prompt Template
```
## Task: [TITLE]
**Project:** /path/to/project
**Context:** 2-3 sentences

### Files to modify:
- path/to/file — what to change

### Requirements:
1. Concrete requirements

### Constraints:
- Non-negotiables, what NOT to change

### IMPORTANT RULES:
- READ files first
- DO NOT touch unrelated files
- Run build after changes
- No breaking changes

### Testing criteria:
- What to verify
```

#### Fallback Chain
1. Cursor ACP fails → fix prompt, retry
2. Still fails → Cursor CLI direct
3. Subscription exhausted → OC-Go via ACP
4. All unavailable → Manual `edit` tool

### 5.3 Sub-Agent for Research
```json
{ "task": "Research X", "model": "...", "runtime": "subagent", "context": "isolated" }
```

### 5.4 Parallel Execution
- Group independent tasks (no shared files)
- Max 4 concurrent sessions
- `sessions_yield` to wait for completions
- **Fallback:** Serial if parallel fails

---

## 6. Verification & Review

### 6.1 Verification Gate — NEVER SKIP
After ANY code change, run: build → test → lint → typecheck.
**Evidence required:** Show command output. "I believe it works" is not evidence.

### 6.2 Vision Q&A
After UI changes: screenshot → vision analysis.
Fallback chain: cloud vision → local vision → laptop → slow edge → manual describe.

### 6.3 Self-Review Checklist
```
[ ] Did I repowise first?
[ ] Did I use the plan tool?
[ ] Does the build pass?
[ ] Do tests pass?
[ ] Did I check for visual issues (if UI)?
[ ] Did I log the session? (bash scripts/log-session.sh ...)
[ ] Did I update STATE.md?
[ ] Did I log decisions? (bash scripts/log-decision.sh ...)
```

---

## 7. Logging & Tracking

### 7.1 Session Logging — MANDATORY
Every significant session MUST be logged:
```
bash scripts/log-session.sh <project> <task> <model> <status> [notes]
```

### 7.2 Decision Logging
Every architecture decision MUST be logged:
```
bash scripts/log-decision.sh <path> <title> <context> <decision> [alt] [cons]
```

### 7.3 State & Roadmap
- Keep `.planning/STATE.md` current
- Keep `.planning/ROADMAP.md` as high-level plan

### 7.4 Workboard (if available)
Use `workboard_create` / `workboard_claim` / `workboard_complete` for complex multi-card work.
**Fallback:** Manual tracking in STATE.md.

### 7.5 Handoff
When switching contexts, write a handoff document with current state, decisions, open questions.

---

## 8. Debugging & Fixes

### 8.1 Diagnose Protocol
1. Build feedback loop (failing test, curl, CLI, screenshot)
2. Reproduce the bug
3. Hypothesise (3-5 ranked causes)
4. Instrument (one variable at a time)
5. Fix + regression test
6. Cleanup debug logs

### 8.2 Common Error Recovery
| Error | Fix |
|---|---|
| Build fails | Read error, fix, rebuild |
| Test fails | Read output, fix code |
| Package missing | `npm install` |
| Git conflict | `git stash`, rebase, pop |
| No internet | Use local fallbacks |

---

## 9. Quality Gates

```
[Build passes] → [Tests pass] → [Lint clean] → [Types check]
```
If any fails → Diagnosis → Fix → Retry.

For UI: `[Screenshot] → [Vision analysis] → [Fix issues]`

Post-ship: `[Log session] → [Log decisions] → [Update STATE.md] → [Update roadmap]`

---

## 10. Tool Fallback Master Table

| Tool | Primary | Fallback 1 | Fallback 2 |
|---|---|---|---|
| `repowise` | `repowise` | `exec find` | Skip |
| `update_plan` | Normal call | Mental plan | Skip |
| `sessions_spawn` (ACP) | Cursor ACP | Cursor CLI | Manual `edit` |
| `sessions_spawn` (subagent) | Subagent | Web search | Ask human |
| `edit` | `edit` tool | `exec sed` | `write` full file |
| Build/test | `npm run build/test` | `tsc --noEmit` | Skip |
| Vision | Cloud vision model | Local vision | Manual |
| Memory | `memory_search` | `lcm_grep` | `grep` on files |
| Session log | `scripts/log-session.sh` | Manual append | Skip |
| Decision log | `scripts/log-decision.sh` | Manual ADR | Skip |
| Price check | `scripts/check-prices.sh` | Manual web_fetch | Skip |