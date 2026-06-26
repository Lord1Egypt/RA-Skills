# Orchestration Control Plane V1

## Goal
Build an OpenClaw-native orchestration layer that supports:
- deep research
- builder/reviewer/fix loops
- project builder with reviewer-guided retries
- long-running work over hours
- durable run state and recovery
- mixed tasks (code, research, docs, ops), not just coding

## V1 Principles
1. **OpenClaw-native**: use sessions, cron, heartbeat, shared files.
2. **Durable state beats prompt memory**: every run must be resumable from files.
3. **Typed retries**: not blind retry, but fix-loop / partial rebuild / replan.
4. **Workflow-first**: reusable declarative workflows, not ad hoc orchestration each time.
5. **Human-visible checkpoints**: every phase produces an artifact and a state update.
6. **Cheap ops, expensive judgment**: scheduler/monitoring can be cheap; routing/review stays high-quality.

---

## Architecture Overview

### Layer 1: Orchestrator Skill (policy + routing)
Keep one primary skill:
- `skills/agent-team-orchestration/`

Responsibilities:
- choose workflow
- choose agent roles
- choose model category
- define handoff format
- define retry / escalation rules
- explain when to use each mode

This layer is the **brain**, not the runtime.

### Layer 2: Declarative Control Plane (files)
New directory:

```text
agent/orchestration/
  agents/
    planner.yaml
    researcher.yaml
    synthesizer.yaml
    architect.yaml
    builder.yaml
    reviewer.yaml
    tester.yaml
    critic.yaml
    integrator.yaml
    ops.yaml
  workflows/
    deep-research.yaml
    review-loop.yaml
    project-builder.yaml
    batch-review.yaml
    watchdog.yaml
  runs/
    <run-id>/
      state.json
      plan.md
      events.jsonl
      handoffs/
      outputs/
      reviews/
      checkpoints/
      working-memory/
  templates/
    handoff.md
    review.md
    checkpoint.md
    temporary-context.md
  COMMUNICATION.md
```

This layer is the **shared source of truth**.

### Layer 3: Local Runtime (dispatcher + monitor)
Small local helper code, e.g.:

```text
scripts/orchestration/
  run_workflow.py
  dispatch_step.py
  complete_step.py
  apply_review.py
  prepare_project_builder.py
  watchdog.py
  status.py
```

Responsibilities:
- create run ids
- materialize workflow state
- dispatch sub-agents / sessions
- update run state after each completion
- apply retry policy
- trigger escalations
- resume stalled runs from file state

This layer is the **engine**.

---

## Communication Model

The system should treat communication as 3 separate layers:

### 1. Stable shared context
This is the project-level context every agent should consult.

Canonical files:
- `README.md`
- `CLAUDE.md`

For project work, these live at the repository or worktree root.

### 2. Directed handoff
This is the explicit A -> B relay between phases or agents.

Canonical location:
- `runs/<run-id>/handoffs/`

### 3. Shared temporary context
This is richer short-lived context that survives retries, agent death, or replacement.

Canonical location:
- `runs/<run-id>/working-memory/`

Use it for:
- failed attempts
- intermediate notes
- unresolved questions
- partial decompositions
- integration gotchas

---

## Core File Schemas

### `agents/*.yaml`
Defines stable agent archetypes.

Example fields:
- `name`
- `purpose`
- `best_for`
- `avoid_for`
- `default_model_category`
- `allowed_tools`
- `input_contract`
- `output_contract`
- `reviewer_for`

Example:
```yaml
name: reviewer
purpose: verify artifacts against spec and catch gaps
best_for:
  - correctness checks
  - edge cases
  - scope drift detection
avoid_for:
  - first-pass implementation
  - writing specs it will later approve
default_model_category: brain
output_contract:
  - verdict
  - issues_by_severity
  - minimal_fix_scope
  - escalate_if_systemic
```

### `workflows/*.yaml`
Defines reusable state machines.

Example fields:
- `workflow_id`
- `goal`
- `phases`
- `entry_conditions`
- `artifacts`
- `retry_modes`
- `escalation_rules`
- `completion_conditions`

### `runs/<run-id>/state.json`
Durable run state.

Example fields:
```json
{
  "run_id": "prj-2026-04-20-001",
  "workflow": "project-builder",
  "status": "in_progress",
  "phase": "review",
  "iteration": 2,
  "active_agents": ["builder-backend", "reviewer-main"],
  "canonical_artifacts": {
    "spec": "shared/specs/foo.md",
    "implementation": "shared/artifacts/foo/",
    "review": "shared/reviews/foo-round2.md"
  },
  "last_decision": "Fix loop on backend module only",
  "next_action": "dispatch partial rebuild",
  "blockers": [],
  "history": []
}
```

### `events.jsonl`
Append-only event log.
Each event contains:
- timestamp
- actor
- phase
- event_type
- artifact path
- summary

This is crucial for recovery and observability.

---

## V1 Workflows

### 1. `deep-research`
Use for broad investigation.

Flow:
1. planner creates question decomposition
2. 3-6 researchers run in parallel on non-overlapping angles
3. synthesizer merges findings
4. critic reviews for gaps / weak evidence
5. optional second pass if critic finds major gaps
6. final synthesis

Artifacts:
- `shared/specs/<topic>-plan.md`
- `shared/artifacts/<topic>/research-*.md`
- `shared/reviews/<topic>-critic.md`
- `shared/specs/<topic>-final.md`

Retry modes:
- `targeted-research-pass`
- `re-synthesis`

### 2. `review-loop`
Use for a bounded build + review cycle.

Flow:
1. builder creates artifact
2. reviewer evaluates
3. if pass -> done
4. if fail -> builder fix loop
5. max 3 iterations before escalation

Reviewer output must be structured:
- verdict: pass/fail
- issue list
- severity
- minimal fix scope
- whether issue is local or systemic

### 3. `project-builder`
Use for end-to-end project work.

Flow:
1. interview/spec
2. architecture
3. parallel builders by module
4. integration
5. review
6. typed retry:
   - local fix loop
   - partial rebuild
   - replan
7. integration review
8. ship

This is the main answer to the “Ralph loop for project building” requirement.

#### Git-backed execution requirement
For `project-builder`, execution should happen inside a git-backed repository or worktree, not only inside orchestration state files.

Requirements:
- repository/worktree root exists
- `README.md` and `CLAUDE.md` live there and are treated as stable shared context
- parallel builders should use isolated worktrees/branches when practical
- GitHub remote should exist for durable sync on GitHub-backed projects
- worktree prep should be reproducible via a helper (V1: `prepare_project_builder.py`)
- worktrees should live outside the repo working tree (V1 target: `<worktree-root>/...`)

The orchestration layer should therefore manage both:
- run-local state (`runs/<run-id>/...`)
- project state (repo/worktree + git history)

#### Typed retry policy
When review fails, classify the failure:

**A. Local defect**
- example: bug in one module
- action: builder fix loop
- owner: same builder if possible
- max: 2-3 rounds

**B. Cross-module mismatch**
- example: API contract drift between frontend/backend
- action: partial rebuild + reintegration
- owner: affected builders + integrator

**C. Architectural/spec issue**
- example: reviewer says the implementation follows a bad plan
- action: replan loop
- owner: planner/architect

Do not restart the whole project by default.

### 4. `batch-review`
Use for many similar items.

Flow:
1. split batch
2. dispatch M parallel reviewers/builders
3. aggregate results
4. optional second batch for failed items only

### 5. `watchdog`
Health monitoring workflow.

Flow:
1. inspect active runs
2. detect stale state / missing events / excessive retries
3. mark run as healthy, stalled, or escalated
4. optionally trigger wake / summary / recovery step

---

## Handoff Contract (mandatory)
Every inter-agent handoff must contain:
1. what was done
2. canonical artifact paths
3. how to verify
4. known issues
5. exact next action
6. whether retry should be local / partial / replan

Template:
```markdown
## What was done
...

## Canonical artifacts
- ...

## Verification
- ...

## Known issues
- ...

## Retry classification
- local-fix | partial-rebuild | replan | none

## Next action
- ...
```

---

## Reviewer Contract (mandatory)
Reviewer outputs must be machine-usable.

Template:
```markdown
## Verdict
pass | fail

## Severity
low | medium | high | critical

## Issues
- [id] description

## Minimal fix scope
- exact modules / files / artifacts affected

## Classification
local-defect | cross-module | architecture-spec

## Recommended next step
fix-loop | partial-rebuild | replan | escalate
```

Without this structure, retries become noisy and wasteful.

---

## Retry and Escalation Policy

### Retry rules
- same builder retries local fixes when feasible
- max 3 retries for same failure class
- if same failure repeats twice with no delta -> escalate
- if reviewer flags systemic problem -> no local retry, go to partial rebuild or replan

### Escalation triggers
- same failure repeated twice
- run exceeds expected scope by 2x
- no event/checkpoint for threshold duration
- missing canonical artifact
- contradictory reviews

### Escalation targets
- stronger reviewer
- planner/architect
- human

---

## Observability V1
We do not need a full dashboard yet, but we do need:
- `state.json` as the source of truth
- `events.jsonl` append-only log
- `plan.md` human-readable summary
- periodic summaries via cron / heartbeat

Minimal statuses:
- `queued`
- `assigned`
- `in_progress`
- `review`
- `fix_loop`
- `partial_rebuild`
- `replan`
- `blocked`
- `done`
- `failed`
- `escalated`

---

## OpenClaw Integration

### Sessions
- use `sessions_spawn` for specialized workers
- use persistent sessions only when role continuity matters
- otherwise prefer one-shot runs plus durable file state

### Heartbeat
Heartbeat should not merely say “still running”. It should:
- advance active runs
- inspect stalled ones
- recover the next step from `state.json`
- notify only on meaningful progress, blockers, or decision requests

### Cron
Use cron for:
- watchdog checks
- stale run detection
- daily/periodic summaries
- wake-up of long-running orchestration runs

### Shared directories
Canonical artifact routing:
- `shared/specs/`
- `shared/artifacts/`
- `shared/reviews/`
- `shared/decisions/`
- `shared/learnings/`

---

## What stays out of V1
Do **not** build yet:
- full UI/dashboard
- automatic model optimization engine
- 20+ agent zoo
- complex external scheduler
- merge queue like Gastown refinery
- mailbox simulation between agents
- autonomous indefinite loops with weak stop conditions

V1 should stay small, legible, and robust.

---

## Recommended Initial Agent Set (10)
1. planner
2. researcher
3. synthesizer
4. critic
5. architect
6. builder
7. reviewer
8. tester
9. integrator
10. ops

This is enough to cover research + project work.

---

## Recommended Implementation Order

### Phase 1: Foundations
- create `agent/orchestration/agents/`
- create `agent/orchestration/workflows/`
- define YAML schemas
- create run directory structure
- define handoff/review templates

### Phase 2: Runtime core
- implement run creation
- implement state transitions
- implement event logging
- implement dispatch of first workflow step
- implement retry classification

### Phase 3: First workflows
- `review-loop`
- `deep-research`
- `project-builder`

### Phase 4: Recovery + ops
- watchdog script
- stale-run detection
- heartbeat integration
- cron summaries

### Phase 5: Hardening
- better summaries
- replay/resume helpers
- reviewer conflict handling
- richer run analytics

---

## Success Criteria for V1
V1 is successful when we can run:
1. one deep research task end-to-end
2. one builder/reviewer/fix loop with structured retries
3. one project-builder run with at least one reviewer-guided relaunch
4. one interrupted run that resumes from files without manual reconstruction

---

## Short Positioning
- **OMC inspiration**: named workflows, clean UX, staged execution
- **Gastown inspiration**: durable state, recovery, watchdog mindset
- **Our version**: lighter, file-native, OpenClaw-native, cross-domain
