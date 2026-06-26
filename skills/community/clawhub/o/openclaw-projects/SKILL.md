---
name: openclaw_projects
description: >
  Builds a Project — a coordinated multi-agent team setup — inside OpenClaw, for
  any kind of team: software development, marketing, real estate, content, sales,
  operations, research, customer success, or anything else where multiple agents
  need to work together toward shared goals. Use this skill whenever someone says
  "set up a project", "create a project", "add a project to my team", "build a
  team", "make my agents work together", "configure agent coordination",
  "set up agent collaboration", "I want a team of agents", "how do I run multiple
  agents on one project", "wire up Asana for my agents", "wire up ClickUp for my
  agents", "add a new project", or anything similar — even if they don't explicitly
  say "project" or "team". Also trigger when someone asks how multiple agents
  should coordinate, share work, escalate, or hand off tasks. This skill creates
  the entire project folder structure (PROJECT.md rulebook, project.json config,
  queue files for inter-agent messaging, project-lock.json phase tracking,
  decision/issue/runbook documents, shared workspace) and updates OpenClaw config
  to wire agent-to-agent communication. It works through a structured interview:
  team identity, work structure, then a comprehensive AI-rewritten team plan for
  user review and fine-tuning before building. Supports any task manager backend
  (Asana, ClickUp) via the user's separately installed dependency skill.
  Multiple projects can coexist; agents can participate in multiple projects.
  Requires the openclaw-administrator skill (EncryptShawn) to be loaded.
  Recommends openclaw-recovery-manager (EncryptShawn) for safety.
  This skill does not make task-manager API calls itself — those are delegated
  to the user's installed Asana or ClickUp dependency skill.
  This skill does not read or store any credentials or secret values.
---

# OpenClaw Projects

This skill adds the concept of a **Project** to OpenClaw — a coordinated multi-agent team setup that lets one or more agents work together toward shared goals. Projects can be any team type: software development, marketing, real estate, content, sales, customer success, research, or anything else.

A Project is:
- A folder at `~/.openclaw/projects/[project-id]/` containing the team rulebook, configuration, shared workspace, and inter-agent message queues
- A defined workflow that takes work from intake through delivery
- A wiring layer that connects multiple agents through OpenClaw's agent-to-agent communication
- A coordination unit that uses one task manager (Asana or ClickUp) as the source of truth for task ownership and status

Multiple projects can coexist. Agents can participate in multiple projects.

---

## Contents

- [What This Skill Does](#what-this-skill-does)
- [Prerequisites](#prerequisites)
- [Credential and Security Model](#credential-and-security-model)
- [Heartbeat Model and Behavior Rules](#heartbeat-model-and-behavior-rules)
- [Step 0 — Safety First](#step-0--safety-first)
- [Step 1 — Discover Existing Setup](#step-1--discover-existing-setup)
- [Step 2 — Pass 1: Team Identity Interview](#step-2--pass-1-team-identity-interview)
- [Step 3 — Pass 2: Work Structure Interview](#step-3--pass-2-work-structure-interview)
- [Step 4 — Pass 3: AI-Drafted Team Plan for Review](#step-4--pass-3-ai-drafted-team-plan-for-review)
- [Step 5 — Capability Check](#step-5--capability-check)
- [Step 6 — Task Manager Setup](#step-6--task-manager-setup)
- [Step 7 — Create Project Folder Structure](#step-7--create-project-folder-structure)
- [Step 8 — Update Agent Workspaces](#step-8--update-agent-workspaces)
- [Step 9 — Update OpenClaw Config](#step-9--update-openclaw-config)
- [Step 10 — Smoke Test](#step-10--smoke-test)
- [Step 11 — Post-Setup Snapshot and Handoff](#step-11--post-setup-snapshot-and-handoff)
- [If Anything Goes Wrong](#if-anything-goes-wrong)

Reference files (read when needed):
- `references/project-files.md` — Full specification of every project folder file
- `references/workflow.md` — Universal workflow phases, escalation rules, queue formats
- `references/interview-questions.md` — Full interview question banks for Pass 1 and Pass 2
- `references/team-archetypes.md` — Common team patterns to draw on for examples
- `references/templates.md` — Parameterized templates for every file this skill generates (PROJECT.md, project.json, queue files, etc.) plus a placeholder reference table

---

## What This Skill Does

1. **Interviews the user** through a structured three-pass discovery process to understand the team
2. **Drafts a comprehensive team plan** — AI-rewrites the user's answers into a complete operational plan, filling gaps and tightening loose answers
3. **Reviews the plan with the user** for fine-tuning and approval before building
4. **Checks agent capabilities** against the planned work and surfaces any concerns (e.g., a vision-required task assigned to an agent without a vision-capable model)
5. **Creates the project folder** at `~/.openclaw/projects/[project-id]/` with all coordination files
6. **Updates each participating agent's workspace** with project references in their AGENTS.md
7. **Updates OpenClaw config** to enable agent-to-agent communication between project participants
8. **Walks through a smoke test** to verify the project is operational

## What This Skill Does NOT Do

- Create agents — agents must already exist (use OpenClaw's agent creation flow first)
- Choose models for agents — that's the user's decision, made when creating the agent
- Hold credentials — the task manager dependency skill handles that
- Make task manager API calls directly — delegated to the user's Asana or ClickUp skill

---

## Prerequisites

**Must be installed before running this skill:**
- **openclaw-administrator** (EncryptShawn) — used to update OpenClaw config and write workspace files

**Must already exist in OpenClaw:**
- Each agent that will participate in the project
- Each agent must have a model and fallback configured (this skill verifies but does not set models)

**Must be installed on the agents that will use it:**
- A task manager dependency skill — either Asana or ClickUp — installed on every agent that needs to read/write tasks. The user is responsible for installing this and configuring its credential (PAT, API key, or token) in their secret management system.

**Strongly recommended:**
- **openclaw-recovery-manager** (EncryptShawn) — provides config snapshots and rollback

**If the user has not yet created their agents**, stop and tell them:
> "Before we build a project, you need to create the agents that will participate in it. Each agent should have its model and fallback configured, and you should install the task manager skill (Asana or ClickUp) on each agent that will read or write tasks. Once your agents exist, come back and we'll set up the project."

---

## Heartbeat Model and Behavior Rules

These rules apply to **every agent on every project created by this skill.** They must be reflected in each agent's HEARTBEAT.md (written in Step 8).

### Heartbeat model selection

Heartbeat runs must use the cheapest available model, not the agent's primary or fallback model. Primary models are expensive for what a heartbeat is — a near-stateless task-manager queue check.

Selection priority:
1. **If OpenRouter is configured on the agent** → use `openrouter/minimax/minimax-m2.7`
2. **If OpenRouter is NOT configured** → use the cheapest model defined in that agent's config. Identify this during Step 8 and record it explicitly in HEARTBEAT.md.

### Heartbeat reasoning level

Heartbeat reasoning must be kept minimal. Do not add a reasoning config key to openclaw.json — that is not a supported field. Control it through the heartbeat prompt instead. Every HEARTBEAT.md must begin with:

```
/think:minimal
```

### Heartbeat failure — fail cheap, never escalate

If a heartbeat fails (task manager unreachable, bad model config, tool error, anything), the agent must **stop immediately and fail cheaply.** It must NOT:

- Retry using the primary model
- Start a troubleshooting loop
- Use `sessions_send` to message itself
- Reason about what went wrong

The correct behavior: log the failure if logging is available, and stop. The next scheduled heartbeat will try again. Most heartbeat failures are config problems (bad model path, missing credential, task manager connection error) that the operator must fix — not something the agent can resolve by spending primary model credits every 30 minutes.

---

## Credential and Security Model

**This skill never reads, stores, requests, or transmits credential values.**

This skill collects only the *names* of env vars (e.g., `PROJ_ASANA_PAT`) — never their values. The dependency skills the user installed (Asana skill, ClickUp skill, any other domain-specific skill) hold and use credentials. This skill passes credential env var *names* to those skills so they know which value to pull from the agent runtime environment.

Credentials must be stored in the user's secret management system (Kubernetes ConfigMap/Secret, .env file, or equivalent) before this skill runs.

---

## Step 0 — Safety First

1. Check if **openclaw-recovery-manager** is installed.
   - **Yes:** Take a snapshot. Label: `pre-project-setup-[project-id]-[date]`
   - **No:** Ask:
     > "I recommend installing openclaw-recovery-manager (EncryptShawn on ClawHub) before we proceed — it lets us roll back if anything goes wrong. Want to install it first, or proceed without it?"

---

## Step 1 — Discover Existing Setup

Before interviewing, gather context using openclaw-administrator:

1. List existing agents and their configured models
2. List existing projects in `~/.openclaw/projects/` (if any)
3. Check which task manager skills are installed on each agent (Asana, ClickUp, or both)

This context informs the interview — for example, if the user has 5 agents already, you can show them the list to pick from rather than asking them to type names.

If `~/.openclaw/projects/` doesn't exist yet, this is the first project. Note this — the agents won't have any "Active Projects" section in their AGENTS.md yet.

---

## Step 2 — Pass 1: Team Identity Interview

Read `references/interview-questions.md` for the full question bank. The goal of Pass 1 is to understand **who is on this team and what they each do.**

Ask the user the questions in order. After each block, briefly summarize what they said back to confirm before moving on.

Core Pass 1 questions:

```
Pass 1 — Team Identity

1. What is this project for? (one-sentence purpose, e.g., "Build and maintain
   the EZBI analytics platform" or "Generate marketing content for client
   campaigns")

2. What kind of team is this?
   - Software development
   - Marketing / creative
   - Real estate
   - Content / editorial
   - Sales / outreach
   - Customer success / support
   - Operations
   - Research
   - Other (describe it briefly)

3. What should this project be called?
   - Display name (e.g., "EZBI Platform")
   - Project ID (lowercase, hyphens or underscores, used in folder names — e.g., "ezbi")

4. Which agents will be on this team? (You can pick from your existing agents.)
   For each agent, what is their role on this project?
   (One agent might be "Project Manager" on this project and "Researcher" on
   another — the role is per-project.)

5. Which agent is client-facing? (Equivalent of a PM — receives requirements,
   talks to clients, owns the intake. There should be exactly one.)

6. Which agent validates feasibility? (Domain expert who reviews whether the
   work is doable before committing — e.g., engineer for dev work, strategist
   for marketing, broker for real estate.)

7. Which agent does quality review? (Reviews completed work before delivery
   to the client — e.g., QA for dev, creative director for marketing.)

8. Is there a human operator? (Final authority for merges, unresolvable
   escalations, client engagement when agents can't reach the client.)
   Yes / No — if yes, what's their alias? (e.g., "operator")

9. Are there any other roles? (Specialized contributors — designers,
   researchers, copywriters, etc.)
```

Record all answers. Confirm back before moving on.

---

## Step 3 — Pass 2: Work Structure Interview

The goal of Pass 2 is to understand **how the team works together day-to-day.**

```
Pass 2 — Work Structure

1. Task manager — which one?
   - Asana
   - ClickUp
   (You should already have the corresponding dependency skill installed on
   your agents. Confirm which one.)

2. What are the stages a piece of work goes through? (These become the
   task manager columns. Default suggestion based on team type — confirm
   or customize.)

3. What is the shared working medium?
   - Where does this team actually produce deliverables?
   - Examples: a git repo (devs), a Google Drive folder (marketing),
     a Notion workspace (content), a CRM system (sales/real estate),
     a shared file folder, or none / not applicable
   - If a git repo: SSH URL(s) for cloning
   - If a folder/workspace: path or link
   - If a CRM/external system: how do agents access it?

4. What does "done" look like before work goes to client review?
   - Devs: PR opened, all tests pass, QA reviewed
   - Marketing: copy approved by creative director, brand guidelines met
   - Real estate: listing complete, photos verified, pricing confirmed
   - Whatever fits this team

5. How does the team handle requirements?
   - One sprint at a time (recommended): one agreed scope completed before
     next is accepted
   - Continuous flow: new requirements can come in any time
   (One-sprint-at-a-time is strongly recommended for teams that need
   focused execution. Continuous flow is appropriate for teams handling
   high-volume small tasks.)

6. Escalation thresholds:
   - How long should an agent be stuck on the same problem before stopping
     and surfacing to a human? (Default: 24 hours of active work)
   - How many times can an agent re-escalate the same issue before stopping?
     (Default: 2 escalations to the feasibility-reviewer)
   - How long with no client response before involving the operator?
     (Default: 48 hours)

7. Does this team produce or consume any visual / media assets?
   - Yes: describe (mockups, photos, video, audio, diagrams)
   - No
   (If yes: assets will be stored as task-manager attachments primarily,
   with a fallback location in the project workspace.)

8. Anything else specific to this team that other agents would need to know?
   (Free-form — house style, client communication preferences, specific
   tools/platforms, compliance requirements, etc.)
```

Record all answers. Confirm back before moving on.

---

## Step 4 — Pass 3: AI-Drafted Team Plan for Review

This is the most important step. Take everything from Pass 1 and Pass 2 and produce a **comprehensive, operational team plan** — not a transcription of the user's answers, but an AI-rewritten, gap-filled version that any agent could read and immediately know how to operate.

The plan must include:

- **Team identity:** project name, ID, purpose, kind
- **Roster:** every agent, their role on this project, what they own, what they do not own
- **Task manager configuration:** which one, the column structure with each column's meaning
- **Shared working medium:** what it is, how agents access it, conventions for using it
- **Workflow phases:** every phase from intake through close, with who owns each, what triggers transitions
- **Escalation rules:** thresholds, who escalates to whom, when work stops
- **Communication protocol:** queue files between agents, who reads which queue
- **Visual/media handling:** if applicable, how assets are stored and referenced
- **What "done" means** at each phase
- **Anything specific** the user mentioned

Write this plan in clear, complete prose. Fill gaps the user didn't address explicitly — for example, if the user said "we have a designer" but didn't say what triggers the designer's involvement, infer reasonable defaults based on team type and write them in. Mark inferred items clearly so the user can correct them.

Present the plan to the user:

```
I've turned your answers into a full team plan. Read through it carefully —
this is what will go into PROJECT.md, which is what every agent on the team
reads to understand how to operate.

Items I inferred (not directly asked) are marked with [INFERRED].
Anything that doesn't match what you want, tell me and I'll revise.

[FULL PLAN HERE]

Does this match what you want? Anything to change before we build?
```

**Do not move to Step 5 until the user explicitly approves the plan.** This is the gate that prevents vague PROJECT.md files. Iterate as many times as needed.

---

## Step 5 — Capability Check

Before building, look at the approved plan and check whether the assigned agents can actually do what the plan asks of them.

Using openclaw-administrator, fetch each agent's configured model. Cross-reference against the plan:

- **Vision required?** If the plan involves the agent reviewing mockups, photos, screenshots, or any visual asset, check that the agent's model has vision capability. If not, flag it.
- **Long context required?** If the agent needs to read large documents (long specs, full codebases, large research corpora), check the model's context window. If under 200k and the work seems heavy, flag it.
- **Code-heavy work?** If the agent is doing software development, check the model has reasonable coding benchmarks. (If the user picked something obviously weak, mention it.)
- **Heartbeat model available?** Check whether the agent has OpenRouter configured (for `minimax-m2.7`) or at least one cheap model available for heartbeat use. If the agent's only model is a high-cost primary and there's no OpenRouter or cheap fallback, flag it — heartbeat on a primary model every 30 minutes is a significant credit burn.

**Output format:**

```
Capability check on the assigned agents:

✅ [agent-id] (role: PM) — model [model-name]
   No concerns.

⚠️  [agent-id] (role: FE Designer) — model [model-name]
   Concern: This role will review visual mockups, but [model-name] does not
   support vision. Consider using a vision-capable model for tasks that
   involve images, or assigning that work to a different agent.

⚠️  [agent-id] (role: QA) — model [model-name]
   Concern: This model has a [X]% hallucination rate per public benchmarks,
   which is high for QA work that needs precise pass/fail judgment.
   This is advice — not a blocker.

These are advisory only. You can proceed as-is, change agent models in
your OpenClaw config, or reassign work to different agents.
Proceed? (yes / make changes first)
```

Wait for the user. If they want to change agent models, that's their job — point them at openclaw-administrator. This skill does not set models.

---

## Step 6 — Task Manager Setup

Based on the user's choice in Pass 2:

### If task manager board does NOT exist yet

```
Create the task manager board manually:

1. Log into [Asana / ClickUp]
2. Create a new project / space named: [project_display_name]
3. Set up the columns in this exact order:
   [column list from the approved plan]
4. Invite all agent accounts as members
5. Copy the project ID / GID from the board URL
6. Share the ID here when ready
```

### Once the project ID is confirmed

Using the task manager dependency skill (via the client-facing agent, since they own task creation), add a project description / pinned note with:

```
Project: [project_display_name]
Project ID: [project-id]
Client-facing agent: [agent-id]
Feasibility reviewer: [agent-id]
QA: [agent-id]
Operator: [operator-alias or N/A]
Shared workspace: [path or description]
Task manager column meanings: [brief column legend]
```

Record the task manager project ID — it goes in `project.json`.

---

## Step 7 — Create Project Folder Structure

This creates the entire project at `~/.openclaw/projects/[project-id]/`. Read `references/project-files.md` for the full specification of each file.

### Folder layout

```
~/.openclaw/projects/[project-id]/
├── PROJECT.md                    ← Team rulebook from the approved plan
├── project.json                  ← Machine-readable config
├── project-lock.json             ← Phase tracker (initialized to "idle")
├── STATE.md                      ← Human-readable status
├── SHARED_MEMORY.md              ← Cross-agent knowledge store
├── DECISIONS.md                  ← Append-only decision log
├── KNOWN_ISSUES.md               ← Accepted limitations / debt
├── RUNBOOK.md                    ← Project operating guide (stub initially)
├── workspace/
│   ├── [shared medium]           ← Repo, folder, files, depending on team
│   ├── [media-folder/]           ← Only if team uses visual/media assets
│   ├── SPEC-CURRENT.md           ← Current accepted spec / brief
│   └── DELIVERABLES_GUIDE.md     ← Feasibility-reviewer's task plan (was IMPLEMENTATION_GUIDE.md)
└── queues/
    ├── to-[client-facing-role].md
    ├── to-[feasibility-reviewer-role].md
    ├── to-[feasibility-reviewer-role]-feasibility.md
    ├── to-[qa-role].md
    ├── to-[operator].md          ← Only if operator was specified
    └── to-[other-role].md         ← One per other role on the team
```

### Building each file

**PROJECT.md** — generate from the PROJECT.md template in `references/templates.md`, filling every placeholder with the approved plan content from Step 4. This is the single most important file — it must be complete and operational. Use the placeholder reference table at the bottom of `references/templates.md` to map each placeholder to its source.

**project.json** — generate from the project.json template in `references/templates.md`. Validate the result is valid JSON before writing. Fill in:
- `id` and `name` from Pass 1
- `task_manager` block — type (asana / clickup), project ID, columns
- `participants` — every agent with their project role and OpenClaw workspace path
- `client_facing_role`, `feasibility_reviewer_role`, `qa_role`, `operator` — pointers to the right roles
- `shared_workspace` and `shared_medium` — type and path/URL
- `visual_assets` block — only if the team uses media (Pass 2 #7)
- `queues` — file paths for each role's queue
- `escalation_rules` — values from Pass 2 #6

**project-lock.json** — initialize:
```json
{
  "phase": "idle",
  "sprint_id": null,
  "sprint_opened": null,
  "waiting_on": null,
  "last_updated": "[today]",
  "last_updated_by": "operator",
  "context": "Project initialized. Ready to receive first work.",
  "blocked_tasks": []
}
```

**STATE.md** — initialize:
```markdown
# [project_display_name] — Current State
**Phase:** Idle — Ready for first work
**Last updated:** [today] by operator
```

**Queue files** — initialize each one with header:
```
# Queue: to-[role]
# Format: [YYYY-MM-DD HH:MM] [FROM: agent-id] [TO: agent-id] [TASK: task-id or N/A]
# Append-only. Never delete entries. Mark processed with [READ].
```

**SHARED_MEMORY.md, DECISIONS.md, KNOWN_ISSUES.md** — each gets a header and an empty body.

**RUNBOOK.md** — generate a stub with section headers appropriate for the team type, plus a note:
```
This is a starting stub. The feasibility-reviewer should expand each section
as they learn the project. Devs / contributors read this before starting work.
```

**Shared medium initialization:**
- Git repo: `cd ~/.openclaw/projects/[project-id]/workspace && git clone [ssh-url] [repo-name]`
- Folder/Drive: create `workspace/[folder-name]/` and add a `LINKS.md` file with the external URL if not local
- CRM/external: skip — write a `workspace/EXTERNAL_SYSTEM.md` describing where work happens
- None: skip

**Media folder** — only if Pass 2 #7 was yes:
```bash
mkdir -p ~/.openclaw/projects/[project-id]/workspace/[media-folder-name]
```

---

## Step 8 — Update Agent Workspaces

For each participating agent, write two files: update their `AGENTS.md` with the project reference, and write their `HEARTBEAT.md` with direct queue lookup instructions.

### AGENTS.md — append Active Projects entry

Append (or update) an Active Projects section in each agent's `AGENTS.md`:

```markdown
## Active Projects
- **[project_display_name]** — I am the [role] on this project.
  - Full rules: ~/.openclaw/projects/[project-id]/PROJECT.md
  - My queue: ~/.openclaw/projects/[project-id]/queues/to-[my-role].md
  - Shared workspace: ~/.openclaw/projects/[project-id]/workspace/
  - Check my queue at the start of every session before doing anything else.
  - Check ~/.openclaw/projects/[project-id]/project-lock.json to know what
    phase we are in before acting.
```

If the agent is already on other projects, **append** — do not overwrite. The agent should see all their active projects.

### HEARTBEAT.md — write per agent

Write (or update) `HEARTBEAT.md` for each agent. The heartbeat model is:
- `openrouter/minimax/minimax-m2.7` if OpenRouter is configured on this agent
- Otherwise: the cheapest model in this agent's config (identify it now and fill it in below)

Get the task manager section/column GID for each agent's queue from the task manager board confirmed in Step 6. If unavailable at setup time, leave the GID blank — the agent will discover it on first heartbeat and write it in.

```markdown
/think:minimal

# HEARTBEAT

## Task Manager Queue (read this, do not rediscover)
- Project: [project_display_name]
- Project ID / GID: [task_manager_project_id]
- My Queue / Section: [Agent Role] Queue
- Queue / Section GID: [section_gid_if_known]
- Heartbeat model: [minimax-m2.7 via OpenRouter OR cheapest-available-model-id]

## On each heartbeat
1. Read the project ID and queue/section above — do not browse the task manager to find your queue.
2. Query only that exact project + section.
3. Filter for tasks assigned to you only.
4. If no actionable task is assigned → reply HEARTBEAT_OK and stop.
5. If a task is assigned → report it and proceed per your role workflow in PROJECT.md.
6. If queue metadata above is missing or invalid → do one-time discovery, record the
   project ID and section GID here, then use that direct path from then on.

## Hard rules
- Never use sessions_send to message yourself.
- Never browse other projects, sections, or columns unless queue metadata is missing.
- Never reason about missed or old heartbeats.
- If this heartbeat fails for any reason (tool error, bad model config, task manager
  unreachable): log the failure and STOP. Do not retry. Do not escalate to your primary
  model. Do not troubleshoot. The next scheduled heartbeat will try again.
```

If an agent participates in multiple projects, include a queue block per project in HEARTBEAT.md — one per project — and check each queue in sequence.

---

## Step 9 — Update OpenClaw Config

Use openclaw-administrator to update each participating agent's `agent_to_agent` allow list so agents on this project can communicate. The allow list should include every other agent on the project.

Be careful: if the agent is already on other projects, they may already have entries in their allow list for those project members. **Merge, don't replace.**

Example: if agent `engineer` is on projects A and B:
- Project A members: `pm-agent-a, dev-fe, dev-be, qa`
- Project B members: `pm-agent-b, designer, copywriter, qa`
- Final allow list for `engineer`: `pm-agent-a, dev-fe, dev-be, qa, pm-agent-b, designer, copywriter`

After updating, verify:
```
openclaw agents list --verbose
Confirm each agent's allow list includes all project members.
```

---

## Step 10 — Smoke Test

```
SMOKE TEST

Step 1: Manually create a test task in the [task-manager] [first-stage column]:
  Title: [TEST] Smoke test — verify [project-id]
  Description: Test task. The [client-facing role] agent should pick this up,
  acknowledge it, and either move it forward or post to a queue.

Step 2: Wait for the [client-facing role] agent's next heartbeat (up to 30 min).
  Watch for: task gaining a comment, or moving to another column.

Step 3: Confirm the agent is reading from the project folder.
  - Check [client-facing role] agent's session log
  - Should see references to ~/.openclaw/projects/[project-id]/PROJECT.md
    and the agent's queue file

Step 4: Confirm queue files are writable.
  - Either: trigger a small interaction that produces a queue entry
  - Or: manually write a test entry to one queue file and verify the
    receiving agent picks it up next session

Heartbeat confirmed working? (yes / no — describe what happened)
```

If something fails here, do not move to Step 11. Diagnose:
- Agent didn't pick up task → check their AGENTS.md has the project reference, check their task manager skill is installed and authenticated
- Agent picked up task but didn't write to queue → check `project-lock.json` is readable and `queues/` files exist with correct permissions
- Agent-to-agent message didn't arrive → check OpenClaw config allow list from Step 9

---

## Step 11 — Post-Setup Snapshot and Handoff

### Snapshot
If openclaw-recovery-manager is installed:
```
Take post-setup snapshot.
Label: post-project-setup-[project-id]-[date]-confirmed
```

### Handoff Summary

```
PROJECT SETUP COMPLETE

Project: [project_display_name] ([project-id])
Type: [team_type]
Folder: ~/.openclaw/projects/[project-id]/

ROSTER:
[role]               | [agent-id]              | [model]
[client-facing role] | [agent-id]              | [model]
[feasibility role]   | [agent-id]              | [model]
[qa role]            | [agent-id]              | [model]
[operator]           | human

TASK MANAGER:
Type: [Asana / ClickUp]
Project ID: [id]
Stages: [column list]

SHARED WORKSPACE:
[path or description]
[Repo SSH URL if applicable]

HOW TO START WORK:
Send your first requirements / brief / intake to [client-facing-agent-id].
The team will:
  1. Validate feasibility through [feasibility-reviewer]
  2. Get your sign-off on the plan
  3. Execute through [executing-roles]
  4. Quality-review through [qa-role]
  5. Notify [operator or you] when ready for sign-off

ESCALATION:
Stuck > [X]h or [Y] re-escalations → work stops, [operator] notified
Client no response > [Z]h → [operator] gets a message

ADD ANOTHER PROJECT:
Run this skill again. Same agents can join multiple projects without conflict.

RECOVERY:
Pre-setup snapshot:  pre-project-setup-[project-id]-[date]
Post-setup snapshot: post-project-setup-[project-id]-[date]-confirmed
```

---

## If Anything Goes Wrong

```
Option 1 — Recover using openclaw-recovery-manager:
  Restore: pre-project-setup-[project-id]-[date]
  Returns config to the state before setup began.

Option 2 — Diagnose with openclaw-administrator:
  Run diagnostics, identify what failed, retry just that step.

Option 3 — Describe what step failed and what error appeared.
  I can walk through the failed step again.
```

---

## Adding Agents to an Existing Project Later

If the user runs this skill against an existing project with the same project ID:
1. Detect the existing project folder
2. Ask: "Project [id] already exists. Are you adding agents, changing the structure, or something else?"
3. If adding agents: run only Pass 1 question 4 (agent assignment), check capabilities, update participants in `project.json`, append to AGENTS.md for new agents only, update allow lists in OpenClaw config
4. If changing structure: walk through the relevant interview sections, regenerate PROJECT.md, leave history files (DECISIONS.md, SHARED_MEMORY.md) intact

Do not overwrite history files (DECISIONS.md, SHARED_MEMORY.md, queue archives) under any circumstance.
