# Checklist

This checklist assumes a fresh OpenClaw by default. If the target machine already has an older setup, use the same checklist to normalize it into the Fire Dragon Fruit Architecture without carrying forward unnecessary noise.

## Inspection

Confirm and write down:

- current agents and routing
- gateway runtime mode
- model providers and profiles
- memory directories and actual files
- installed skills
- heartbeat status
- cron jobs
- Feishu bindings
- existing project docs with real business value

## Restructure

Target result:

- keep `main`
- create or refine `rescue`
- remove `lab` from normal production topology
- make sure `main` and `rescue` do not share noisy working memory

Check:

- `main` is the only daily operating brain
- `rescue` can survive independently for emergency continuity
- no old agent remains as dead configuration noise

## Memory

Required files:

- `MEMORY.md`
- `memory/YYYY-MM-DD.md`
- `memory/topics/`

Minimum topic files:

- `memory/topics/user-prefs.md`
- `memory/topics/workflows.md`

Check:

- `MEMORY.md` is concise
- daily memory exists for today
- topic files hold evergreen knowledge
- there is a visible promotion path from daily logs to topics to `MEMORY.md`

## Project Truth

Required structure:

- `projects/INDEX.md`
- `projects/<project>/PRD.md`
- `projects/<project>/PROGRESS.md`
- `projects/<project>/EXECUTION_PLAN.md`

Check:

- active projects are listed in `projects/INDEX.md`
- heartbeat and cron instructions point to these files explicitly
- important project knowledge is not stranded only in chat history

## Skills

Prefer skill-based roles, not many agents.

Recommended roles:

- `scout-mode`
- `closer-mode`
- `ops-mode`
- `reflect-mode`

Check:

- operating logic is written in files
- role switching does not require new long-lived agents

## Automation

Required pattern:

- heartbeat for low-noise checks
- regular cron for timed visible updates
- isolated cron for reflection and maintenance

Check:

- heartbeat instructions are small and concrete
- each cron has a clear purpose
- isolated cron is used for noisy synthesis work
- every scheduled task points at real project or memory files

## Evolution

Required pattern:

- recurring reflection on recent daily logs and project files
- promotion of stable lessons into memory topics or `MEMORY.md`
- upgrade of repeated work into skills or SOP files
- removal of stale prompts, dead docs, and obsolete branches

Check:

- the improvement loop is visible in files, not just promised in prose
- there is a clear place where wins, failures, and lessons are captured
- the system can get cleaner over time instead of only growing

## Integrations

Check:

- official `@openclaw/feishu` is used
- primary Feishu routing goes to `main`
- any secondary Feishu route goes to `rescue` only if justified
- Ollama is used for memory embeddings if local memory search is needed

## Runtime

Check:

- runtime paths are explicit and durable
- no brittle version-manager-only start path remains
- no unofficial helper service remains unless it is clearly necessary

## Acceptance Criteria

The work is complete when all of the following are true:

- the system has one strong `main`
- `rescue` is present and isolated
- `lab` is absent from the normal topology
- file memory exists and is usable
- project truth files exist for the active project set
- heartbeat is configured for maintenance, not noise
- cron structure is intentional
- official integrations are in place
- memory, evolution, and scheduling are all explicit rather than implied
- another operator could inspect the filesystem and understand how the system runs
