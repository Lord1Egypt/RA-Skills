# 火龙果架构

This reference describes the Fire Dragon Fruit Architecture, a fresh-install-first OpenClaw operating model built around one strong `main`, one isolated `rescue`, durable file memory, explicit project truth, and sustainable automation.

## Core Shape

The stable target is:

- one strong `main`
- one minimal isolated `rescue`
- no `lab`
- one gateway per machine

This pattern keeps decision-making centralized while preserving an emergency lane. `main` handles normal work, learning loops, planning, daily execution, and user-visible continuity. `rescue` exists only so the system can still communicate or perform narrow fallback duties if `main` is unhealthy.

This architecture is designed to be the default starting point for a new OpenClaw, not just a cleanup plan for a broken one.

## Agent Roles

### `main`

Use `main` as the only daily operating brain.

`main` should own:

- user context
- long-running project context
- memory curation
- heartbeat
- most routine cron-triggered tasks
- the skill library that shapes behavior

### `rescue`

Use `rescue` as a narrow continuity mechanism.

`rescue` should be:

- isolated from `main` memory
- smaller in scope
- lighter in skills
- excluded from normal planning and self-improvement loops

Good rescue duties:

- emergency replies
- backup channel continuity
- narrow operational notifications

Bad rescue duties:

- becoming a second main brain
- sharing the same noisy workspace as `main`
- learning from or editing `main`'s daily memory by default

## Model Strategy

Use the strongest hosted model available as the primary reasoning engine when budget is not the constraint.

Recommended strategy:

- hosted frontier model for `main`
- no small local text model by default
- Ollama only for memory embeddings unless there is a proven need for local inference

Why:

- the biggest gain usually comes from the primary model quality
- a weak local text model often adds operational complexity without improving the system
- memory embeddings are a much cleaner local use case

## Memory Strategy

Memory should live in files, not in wishful thinking about the model remembering things.

Use:

- `MEMORY.md` for curated durable truths
- `memory/YYYY-MM-DD.md` for daily factual logs
- `memory/topics/*.md` for evergreen knowledge

Recommended topic files:

- `memory/topics/user-prefs.md`
- `memory/topics/workflows.md`
- `memory/topics/offers.md`
- `memory/topics/channels.md`
- `memory/topics/integrations.md`

Rules:

- keep `MEMORY.md` short
- treat daily logs as raw operating evidence
- promote only stable patterns into topic files or `MEMORY.md`

This should behave like a memory engine, not a file pile:

- today and yesterday are the fast-moving operating surface
- topic files are the evergreen retrieval layer
- `MEMORY.md` is the compact always-worth-reading layer
- project truth files are the execution layer

Promotion path:

- raw fact -> daily log
- repeated fact -> topic file
- durable operating truth -> `MEMORY.md`
- project-specific decision -> project file

## Project Truth Files

Project truth must be stored explicitly so heartbeat, cron, and new sessions can find it.

Use:

- `projects/INDEX.md`
- `projects/<project>/PRD.md`
- `projects/<project>/PROGRESS.md`
- `projects/<project>/EXECUTION_PLAN.md`

Optional project files:

- `DECISIONS.md`
- `RISKS.md`
- `RETRO.md`

The project file tree is the durable source of truth. Chat history is not.

## Skill Strategy

Prefer one main agent with role skills over many business agents.

Useful roles:

- `scout-mode`
- `closer-mode`
- `ops-mode`
- `reflect-mode`

This keeps:

- memory centralized
- routing simple
- behavior modular
- maintenance cost lower

Split into separate agents only when you need true routing separation, permission isolation, or a dedicated long-lived context that must not mix with the main one.

## Automation Strategy

### Heartbeat

Use heartbeat for low-noise maintenance:

- stalled-task checks
- approval queue checks
- failure detection
- memory hygiene reminders
- project progress nudges

Keep it short and cheap.

### Regular Cron

Use normal cron for scheduled user-facing outputs:

- timed progress updates
- morning focus summaries
- business reports

### Isolated Cron

Use isolated cron for heavier or noisier tasks:

- nightly reflection
- document cleanup
- project synthesis
- memory promotion work

This prevents scheduled noise from polluting the main conversational thread.

## Scheduling Blueprint

If no better schedule already exists, use a default blueprint like this:

- heartbeat every 30 minutes during working hours
- one or more main cron jobs for visible progress delivery
- one nightly isolated cron for reflection and memory maintenance

Good default jobs:

- hourly progress update
- morning focus or priority sync
- nightly reflect and cleanup

Each scheduled job should have:

- a file source of truth
- a clear output
- a clear failure mode
- a reason to exist

If a job cannot name its source files and output files or destination, it is too vague.

## Evolution Loop

OpenClaw does not become stronger because someone says "self-evolve". It becomes stronger because a repeatable improvement loop is in place.

A practical evolution loop is:

1. capture daily facts in `memory/YYYY-MM-DD.md`
2. inspect project progress and execution gaps
3. run reflection on recent wins, misses, and friction
4. promote stable lessons into topic files or `MEMORY.md`
5. convert repeated work into skills, SOPs, or automation
6. prune obsolete prompts, stale docs, and dead branches

This loop should run continuously, but it should leave visible artifacts on disk so another operator can audit what changed and why.

## Feishu Strategy

Use official `@openclaw/feishu` only.

Recommended routing:

- primary account or main production traffic goes to `main`
- secondary emergency account can route to `rescue`

Do not use a second Feishu-connected agent as a permanent planning brain unless you truly want multi-agent complexity.

## Runtime Hardening

Avoid service entrypoints that depend on a particular interactive shell or version-manager session.

Prefer:

- fixed Node binary paths
- fixed OpenClaw runtime paths
- explicit service scripts

This matters most for scheduled work, boot-time starts, and long-running gateways.

## Final Standard

A good final system has:

- one clearly dominant `main`
- one clearly isolated `rescue`
- durable file memory
- explicit project truth files
- cheap heartbeat
- precise cron
- official integrations
- low operator confusion
