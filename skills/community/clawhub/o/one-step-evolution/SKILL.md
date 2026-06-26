---
name: one-step-evolution
description: "Use when you need to stand up or standardize a fresh OpenClaw setup as the Fire Dragon Fruit Architecture: one strong main, one isolated rescue, layered file memory, project truth docs, heartbeat, isolated cron, official Feishu integration, Ollama memory embeddings, and a durable long-running operating model. Search intents include OpenClaw architecture, OpenClaw memory, OpenClaw heartbeat, OpenClaw cron, OpenClaw Feishu, OpenClaw Ollama, OpenClaw rescue, Fire Dragon Fruit Architecture, 火龙果架构, 持续进化, 分层记忆, 调度任务, 长期记忆, 自动调度, 飞书机器人, 个人经营系统, 主脑架构, and personal operating system."
---

# One Step Evolution

## Overview

This skill installs the Fire Dragon Fruit Architecture, or `火龙果架构`, onto a fresh OpenClaw setup and makes the resulting system durable for long-running work. It is optimized for a single strong `main`, one minimal `rescue`, layered memory on disk, an explicit evolution loop, project truth files, low-noise heartbeat, precise cron, and official integrations only.

Read [fire-dragon-fruit-architecture.md](references/fire-dragon-fruit-architecture.md) for the positioning and distinguishing traits. Read [architecture.md](references/architecture.md) for the target design. Read [checklist.md](references/checklist.md) for the implementation runbook and acceptance criteria.

## When To Use

Use this skill when the user wants any of the following:

- Stand up a new OpenClaw directly in the Fire Dragon Fruit Architecture
- Rebuild around `main` first and remove `lab`
- Add durable memory that survives sessions and supports ongoing work
- Add heartbeat and cron so the system can keep working without babysitting
- Rework agent topology so fallback and rescue do not pollute the main brain
- Standardize Feishu, runtime paths, and project structure using official mechanisms
- Normalize an older OpenClaw install into the same architecture if needed

Do not use this skill for a tiny one-file tweak or a single prompt improvement. This skill is for system-level OpenClaw refactors.

## Target State

The desired end state is the Fire Dragon Fruit Architecture:

- One strong `main` agent as the primary brain
- One minimal `rescue` agent for emergency continuity only
- No `lab` in the steady-state production topology
- One gateway per machine
- Hosted frontier model as the main reasoning engine
- Ollama only for `memorySearch.provider = "ollama"` embeddings unless the user explicitly wants more local inference
- Layered memory on disk:
  - `MEMORY.md`
  - `memory/YYYY-MM-DD.md`
  - `memory/topics/*.md`
- Project truth kept in files, not chat history:
  - `projects/INDEX.md`
  - `projects/<project>/PRD.md`
  - `projects/<project>/PROGRESS.md`
  - `projects/<project>/EXECUTION_PLAN.md`
- Role behavior implemented as skills or explicit modes, not as many long-lived business agents
- `heartbeat` for low-noise maintenance and `isolated cron` for scheduled work
- Official `@openclaw/feishu` only
- Fixed runtime paths instead of fragile version-manager-only service entrypoints

## Core Capabilities

Every successful implementation of this skill must leave these three capabilities clearly present in files and runtime behavior.

### 1. Memory Capability

The system must have durable memory that survives sessions and can be searched, maintained, and promoted over time.

Required structure:

- `MEMORY.md` for stable, curated truths
- `memory/YYYY-MM-DD.md` for daily factual logs
- `memory/topics/*.md` for evergreen knowledge
- `projects/INDEX.md` plus project truth files so work context is not trapped in chat history

Required behavior:

- daily facts go into date-stamped logs
- reusable patterns get promoted into topic files
- only high-signal truths stay in `MEMORY.md`
- active projects are always recoverable from files without depending on chat transcripts

### 2. Evolution Capability

The system must be able to improve itself through file updates and workflow hardening, not by vague claims that the model "learns automatically".

Required behavior:

- a `reflect-mode` or equivalent routine reviews recent daily logs, project progress, and failures
- successful patterns are promoted into `memory/topics/*.md`, `MEMORY.md`, or private skills
- failed instructions, dead prompts, and obsolete workflow branches are removed
- useful repeated behaviors are upgraded into explicit skills or documented operating rules
- improvement is judged by business or operating outcomes, not by how busy the agent looks

### 3. Scheduling Capability

The system must be able to keep working when the user is away.

Required behavior:

- `heartbeat` handles low-noise health checks, stalled work detection, approval queues, and memory hygiene
- regular `cron` handles timed visible outputs such as progress updates or morning focus
- `isolated cron` handles heavier reflection, synthesis, document cleanup, and memory promotion tasks
- every scheduled task must point at real files and a real purpose
- side effects must stay behind approval gates or deterministic workflows

## Template Kit

This skill includes a copy-ready starter workspace under `assets/templates/workspace/`.

Use it like this:

- copy missing root files from `assets/templates/workspace/`
- seed `memory/topics/` from the provided topic templates
- seed `skills/*-mode/` from the provided role skill skeletons
- copy `projects/example-project/` and rename it to the real project name
- adapt `AUTOMATION.md` into the target machine's real heartbeat and cron configuration
- if `rescue` is missing, seed a separate minimal rescue workspace from `assets/templates/rescue/`

Important:

- for a fresh OpenClaw, treat these templates as the default starting point
- if the workspace already contains valuable project truth, merge carefully
- do not overwrite real project history with template placeholders
- use the templates to make the system explicit, then customize them to the machine and user

## Workflow

### 1. Inspect The Current System

Before editing anything, inspect the real installation and summarize:

- Agent list and routing
- Current gateway mode and runtime paths
- Model strategy
- Memory layout
- Existing skills
- Feishu bindings
- Heartbeat and cron jobs
- Project directories that already contain useful truth

Pay special attention to duplicated agents, half-removed experiments, custom sidecars, and anything that can silently override the intended topology.

If the installation is fresh, keep this step short and use it to confirm the baseline before applying the templates.

### 2. Reshape The Agent Topology

Refactor toward:

- `main` as the only daily operating brain
- `rescue` as a separate emergency agent with minimal memory and minimal skills
- No `lab` unless the user explicitly requests a research sandbox

Rules:

- `main` and `rescue` must not depend on each other's memory files
- `rescue` should not run routine business planning or learning loops
- If a second external account exists, route it to `rescue` only if that protects continuity without creating cross-talk

### 3. Rebuild The Memory Layer

Create or repair the file-based memory system:

- `MEMORY.md` for curated durable truths
- `memory/YYYY-MM-DD.md` for daily factual logs
- `memory/topics/*.md` for evergreen knowledge such as users, offers, workflows, channels, and operating rules

Keep `MEMORY.md` small and high-signal. Do not turn it into a dumping ground.

Build a promotion path, not just storage:

- raw facts land in daily logs
- repeated truths move into `memory/topics/*.md`
- only durable operating truths move into `MEMORY.md`
- archived project conclusions move into the relevant project files

If projects exist, establish a file-based source of truth:

- `projects/INDEX.md` declares active projects
- Each active project has `PRD.md`, `PROGRESS.md`, and `EXECUTION_PLAN.md`
- Heartbeat and cron instructions must explicitly reference these project files

If these files are missing, seed them from `assets/templates/workspace/projects/example-project/` and then replace placeholders with the real project data.

### 4. Convert Behavior Into Skills And Modes

Prefer a single `main` plus role skills such as:

- `scout-mode`
- `closer-mode`
- `ops-mode`
- `reflect-mode`

Do not split these into separate long-lived agents unless there is a hard routing or permissions reason.

When implementing, move durable operating logic into:

- `skills/`
- `AGENTS.md`
- `HEARTBEAT.md`
- project truth files

Do not bury core operating rules inside transient chats.

If role skills are missing, seed them from `assets/templates/workspace/skills/`.

### 5. Rebuild Automation The Stable Way

Use:

- `heartbeat` for low-noise checks, stalled work detection, approval queues, and memory hygiene
- regular `cron` for user-facing timed updates
- `isolated cron` for higher-noise reflection, cleanup, and document maintenance

Automation rules:

- Keep heartbeat small and cheap
- Use project files as the source of truth
- Prefer isolated sessions for heavy scheduled work
- Keep external side effects behind explicit approval or deterministic workflow controls

If the current install has no useful cadence, establish a default blueprint:

- `heartbeat`: every 30 minutes during active hours for health, stalled work, and pending approvals
- main `cron`: timed operational updates such as hourly progress or morning focus
- `isolated cron`: nightly reflection and memory maintenance

Make sure scheduled tasks reference the actual project files they should read and update.

If the install has no scheduling docs at all, start from `assets/templates/workspace/AUTOMATION.md`.

### 6. Install An Explicit Evolution Loop

Add a recurring improvement loop so the system can get better instead of just accumulate clutter.

Minimum loop:

- read recent `memory/YYYY-MM-DD.md` logs
- inspect current project truth files
- identify repeated wins, failures, and stale instructions
- promote stable rules into `memory/topics/*.md` or `MEMORY.md`
- convert repeated work into skills or durable SOP files
- delete or rewrite prompt clutter that no longer helps

The evolution loop should be visible in files. If another operator opens the workspace, they should be able to see how the system learns.

### 7. Standardize Integrations And Runtime

Use official pieces wherever possible:

- official `@openclaw/feishu`
- official Ollama embeddings path for memory search
- fixed runtime paths for gateway or service scripts

Avoid:

- unofficial Feishu forks when the official package covers the need
- ad hoc embeddings sidecars when official Ollama embeddings are available
- brittle service wrappers that only work under one shell or version-manager session
- adding a small local text model by default when the hosted primary model is already stable and budget allows it

### 8. Validate, Clean Up, And Finish

After edits:

- verify the topology matches the target state
- verify the memory layout exists on disk
- verify heartbeat and cron point at real files and real tasks
- verify memory promotion and reflection paths are explicit
- verify Feishu routing is intentional
- verify model settings reflect the desired primary and embedding strategy
- remove obsolete agents, dead directories, and misleading docs
- run the relevant validation commands
- commit the result if the repo exists and the user expects versioned changes

## Guardrails

- Do not reintroduce `lab` by default
- Do not create many agents when skills are enough
- Do not store project truth only in chat transcripts
- Do not make `rescue` a shadow copy of `main`
- Do not install extra local text models unless there is a clear reliability or cost reason
- Do not leave heartbeat or cron without file references and success criteria
- Do not claim "continuous learning" unless the evolution loop is visible in files and schedules

## Deliverable

When this skill is used well, the final output should leave the system in a state where:

- `main` can keep operating day to day
- `rescue` exists but stays isolated and quiet
- important facts survive across sessions because they live on disk
- projects have explicit truth files
- heartbeat and cron keep work moving
- the setup is easy for another operator or another Codex to replicate
