# Audit — Orchestration V1 vs OMC + Gastown

## Scope
Audit of the current OpenClaw-native orchestration V1 against the essential ideas that looked most valuable in:
- Oh My Claude Code (workflow UX, staged loops, named modes)
- Gastown (durable runtime, work tracking, watchdog/recovery, git-backed execution)

## Summary verdict
The V1 now covers the main structural essentials, but not all the automation depth.

### Covered well
- reusable named workflows
- durable run state outside chat memory
- explicit handoffs
- shared temporary context
- structured review + typed retry routing
- watchdog / stale detection
- project-builder as git/worktree-backed execution
- stable shared context via `README.md` + `CLAUDE.md`

### Covered partially
- agent identity continuity
- recovery automation after failure
- escalation system
- observability / dashboarding
- GitHub durability beyond remote detection
- automatic dispatch of real subagents from the runtime itself

### Not in V1 on purpose
- heavy autonomous daemon layer
- merge queue / refinery equivalent
- full mailbox system
- large-scale scheduler
- GitHub push automation without explicit human decision

---

## Coverage matrix

### 1. Named reusable workflows
**Why it matters:** both external systems rely on named modes / repeatable workflow units.

Status: **YES**

Implemented as:
- `agent/orchestration/workflows/review-loop.yaml`
- `deep-research.yaml`
- `project-builder.yaml`
- `batch-review.yaml`
- `watchdog.yaml`

### 2. Durable run state outside session memory
**Why it matters:** this is the core thing both systems do better than prompt-only orchestration.

Status: **YES**

Implemented as:
- `runs/<run-id>/state.json`
- `plan.md`
- `events.jsonl`
- `working-memory/`
- `handoffs/`
- `reviews/`

### 3. Agent role registry
**Why it matters:** both systems depend on stable agent roles.

Status: **YES / PARTIAL**

Implemented as:
- agent archetypes in `agent/orchestration/agents/*.yaml`

Missing depth:
- no long-lived per-agent persona/history beyond role + slot

### 4. Explicit A -> B communication
**Why it matters:** handoffs / routing packets are essential in both.

Status: **YES**

Implemented as:
- `handoffs/`
- template `handoff.md`
- `dispatch_step.py`

### 5. Shared stable context
**Why it matters:** you explicitly asked for this, and it matches the best part of Claude Code style workflows.

Status: **YES**

Implemented as:
- `README.md`
- `CLAUDE.md`
- detection in `run_workflow.py`
- propagation into dispatch prompts

### 6. Shared temporary context
**Why it matters:** crucial when an agent dies or a retry needs more than the final handoff.

Status: **YES**

Implemented as:
- `runs/<run-id>/working-memory/`
- `temporary-context.md`
- documented in `COMMUNICATION.md`

### 7. Structured review and fix loops
**Why it matters:** OMC-style verify/fix loops are one of the strongest ideas.

Status: **YES**

Implemented as:
- `review.md`
- `apply_review.py`
- typed routing: `fix-loop`, `partial-rebuild`, `replan`

### 8. Recovery / restart friendliness
**Why it matters:** Gastown's big strength is surviving interruption.

Status: **PARTIAL**

Implemented as:
- durable state
- event log
- working memory
- worktree protocol
- resume order documented in `PROJECT_BUILDER_WORKTREE.md`

Missing depth:
- no automatic replacement-agent relaunch yet
- no automatic resume planner yet

### 9. Watchdog / stale detection
**Why it matters:** both systems care about not leaving work silently stuck.

Status: **YES**

Implemented as:
- `watchdog.py`
- `watchdog.yaml`
- stale/block/escalate status transitions

### 10. Observability / status surface
**Why it matters:** users need to see what is running and where it is blocked.

Status: **PARTIAL**

Implemented as:
- `status.py`
- `state.json`
- `events.jsonl`
- `plan.md`

Missing depth:
- no dashboard / TUI / rich summary view yet

### 11. Git-backed project execution
**Why it matters:** this is a key Gastown-like property and important for real project work.

Status: **YES**

Implemented as:
- `prepare_project_builder.py`
- `PROJECT_BUILDER_WORKTREE.md`
- `project-builder.yaml` requirements
- worktree root outside repo: `<worktree-root>/...`

### 12. GitHub durability awareness
**Why it matters:** project-builder should know if the repo is actually GitHub-backed.

Status: **PARTIAL**

Implemented as:
- GitHub remote detection in `prepare_project_builder.py`

Missing depth:
- no push / PR workflow yet
- no branch publish helper yet

### 13. Parallel work decomposition
**Why it matters:** both systems assume parallel sub-work when useful.

Status: **YES / PARTIAL**

Implemented as:
- `dispatch_step.py --count N`
- `dispatch_step.py --targets a,b,c`
- `deep-research` parallel branches
- `project-builder` by-module slots

Missing depth:
- no automatic aggregator / join controller yet

### 14. Escalation path
**Why it matters:** both systems avoid silent flailing.

Status: **YES / PARTIAL**

Implemented as:
- `escalated` status
- retry caps
- watchdog transitions
- `templates/escalation.md`
- `scripts/orchestration/escalate_run.py`
- escalation artifacts under `runs/<run-id>/escalations/`

Missing depth:
- no notifier / auto-routing yet

### 15. Runtime-native spawning of subagents
**Why it matters:** this is where OMC feels magical.

Status: **PARTIAL**

Current behavior:
- runtime generates canonical handoffs/prompts
- runtime now also generates launch manifests under `runs/<run-id>/launch/`
- `OPENCLAW_LAUNCHER.md` defines the bridge to actual `sessions_spawn`
- `list_pending_launches.py` + `mark_launch.py` add the receipt-side mechanics
- actual spawning remains orchestrator-side in OpenClaw

Remaining gap:
- no automatic manifest consumer wired directly into tool calls yet

---

## Bottom line
What felt essential from the two external systems is now mostly present in V1, especially the things that matter most structurally:
- workflows
- state
- communication
- retries
- watchdog
- recovery substrate
- git/worktree project execution

What is still missing is mostly **automation depth**, not **architecture**.

The biggest remaining gaps are:
1. launcher that actually spawns/reattaches OpenClaw subagents from the workflow runtime
2. richer observability
3. explicit escalation artifacts / notifications
4. GitHub publish / PR helpers for project-builder
