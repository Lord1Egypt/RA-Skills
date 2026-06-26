---
name: local-coding-orchestrator
description: Use OpenClaw as a supervisor-driven orchestration scaffold for local coding CLIs such as Codex, Claude Code, and OpenCode. Supports task records, lifecycle transitions, worker launch and reconcile, retry briefs, pipeline presets, and environment-aware blocking for local coding workflows.
---

# Local Coding Orchestrator

Use this skill to run OpenClaw as a lightweight supervisor for local coding CLIs.

This skill has evolved from a routing helper into a v2 orchestration scaffold. The goal is not just to route prompts to tools. The goal is to intake coding work, assign it to the right local worker, track objective progress, coordinate review, reconcile background execution, and retry intelligently until the task reaches a clear done state or a clear blocked state.

## Mission

Use this skill when the user wants OpenClaw to act like an orchestration layer above local coding tools.

That includes cases such as:
- choosing between `codex`, `claude`, and `opencode`
- running implementation and review as separate worker roles
- comparing outputs across tools
- steering long-running local coding sessions
- supervising coding work through task files, status transitions, and review loops

This skill is for **persistent orchestration**, not just one-off prompt forwarding.

## Strict supervisor boundary

Default stance: this skill is a **supervisor, coordinator, and reviewer of work**, not the hands-on implementer.

That means OpenClaw should normally:
- define the task
- choose and launch the right worker
- reconcile worker output
- verify objective checks
- route to review / retry / hardening
- report progress and decisions back to the user

And OpenClaw should normally **not**:
- directly edit product code that belongs to the delegated task
- silently replace a failed worker by doing the implementation itself
- mix coordinator voice with implementer voice in the same phase
- report a task as complete based only on a worker saying it is done

## When direct edits are allowed

Direct edits by the supervisor are the exception, not the default.

Allowed cases:
- fixing the orchestrator skill itself
- repairing task metadata, task records, or orchestration scripts
- making tiny non-product changes required to unblock supervision
- explicit user instruction to take over implementation directly

If the supervisor makes a direct edit, it should say so clearly and distinguish:
- what was supervisor-layer work
- what was worker-layer implementation

## Worker-first policy

For coding tasks inside the target repo, prefer this order:
1. probe with a worker when environment viability is unclear
2. implement with a worker
3. review with a reviewer worker or explicit supervisor review phase
4. harden via a worker retry brief if review requests changes

Do not collapse these into one hand-wavy pass unless the user explicitly asks for speed over strict orchestration.

## Multi-worker orchestration

When the task benefits from multiple tools, the supervisor should assign distinct roles instead of letting every worker do everything.

Recommended pattern:
- one primary implementer
- one reviewer / planner
- one secondary reviewer or alternate implementer

The supervisor should then periodically check progress rather than waiting until the very end.

Periodic supervision means checking:
- whether repo changes are actually landing
- whether a worker is stalled or looping
- whether reviewers agree on the next boundary
- whether a worker-specific blocker requires rerouting or a tighter brief

The supervisor should synthesize reviewer output into a concrete next step.
Do not just forward three uncoordinated opinions to the user.

## What this skill assumes

The machine has local CLIs available for:
- `codex`
- `claude`
- `opencode`

It also assumes you can create project-specific working directories, keep artifacts on disk, and run local background processes safely.

## Execution model

Treat the orchestrator as a three-layer system.

### 1. Intake layer

The intake layer converts a user request into a structured task.

Capture at least:
- task id
- repo path (preferred) or repo identifier
- worktree / branch plan
- task type
- requested outcome
- success criteria
- preferred tool or routing mode
- sensitivity level
- whether review is required
- whether tests, build checks, screenshots, or PR creation are required

### 2. Worker layer

The worker layer runs one or more local coding CLIs.

Workers should be isolated where practical:
- separate worktree or branch per implementation task
- separate logs per worker
- separate prompt snapshot per attempt
- separate review outputs per reviewer

Workers are tool specialists, not supervisors.

### 3. Supervisor layer

The supervisor layer is the core of this skill.

It should:
- launch workers
- record status transitions
- inspect objective signals instead of trusting self-reported completion
- decide whether the task is blocked, review-ready, done, or needs retry
- rewrite prompts for semantic retries when the worker solved the wrong problem
- summarize results back to the user in coordinator voice

## Task lifecycle

Model work as a persistent state machine instead of a one-shot run.

Recommended states:
- `draft`
- `queued`
- `running`
- `awaiting-review`
- `changes-requested`
- `retrying`
- `blocked`
- `completed`
- `failed`
- `cancelled`

Use explicit transitions. Do not silently treat “process exited” as “task completed”.

## Task record

Keep a JSON task file for each orchestration unit.

Recommended directory structure:

```text
local-orchestrator/
  tasks/
  logs/
  prompts/
  reviews/
  state/
```

Recommended task record shape:

```json
{
  "id": "feat-custom-templates",
  "repo": "my-repo",
  "worktree": "../worktrees/feat-custom-templates",
  "branch": "feat/custom-templates",
  "taskType": "feature",
  "role": "implementer",
  "agent": "codex",
  "status": "running",
  "attempt": 1,
  "maxAttempts": 3,
  "createdAt": 1772958600000,
  "updatedAt": 1772959200000,
  "successCriteria": [
    "build passes",
    "tests pass",
    "review complete"
  ],
  "artifacts": {
    "logPath": "local-orchestrator/logs/feat-custom-templates.log",
    "promptPath": "local-orchestrator/prompts/feat-custom-templates-attempt-1.md",
    "reviewPath": "local-orchestrator/reviews/feat-custom-templates.md",
    "prUrl": null
  }
}
```

The exact schema can evolve, but the orchestrator should always leave a durable audit trail.
For the fuller current schema shape, prefer `docs/task-schema.v1.json` and `docs/task-schema.example.json` over this abbreviated inline example.

## Routing and role guidance

Tool choice should reflect the worker role, not just the raw user wording.

### Default role mapping

- **Codex**
  - implementation lead
  - backend logic
  - complex fixes
  - multi-file refactors
  - direct code production

- **Claude Code**
  - architecture review
  - risk analysis
  - code review
  - requirements clarification
  - maintainability critique

- **OpenCode**
  - session continuation
  - alternative implementation plan
  - exploratory or agent-style follow-up work

### Intent model

When routing automatically, first classify the request into a supervisor mode.

- **continue**
  - signals: continue, session, resume, agent
  - default tool: `opencode`

- **review**
  - signals: analyze, explain, review, compare, risk, audit, architecture
  - default tool: `claude`

- **implement**
  - signals: implement, build, create, modify, refactor, fix, generate, develop
  - default tool: `codex`

- **prototype**
  - signals: demo, prototype, quick, lightweight, MVP, browser toy
  - default tool: `codex`, optionally followed by `claude` review

- **maintainable-project**
  - signals: production, maintainable, scalable, long-term, structured
  - default tool: `claude` first for stack and risk validation, then `codex` for implementation

If the task is ambiguous between rapid delivery and long-term maintainability, decide explicitly and state that bias in the user-facing summary.

## Pipelines

Do not treat multi-tool orchestration as “run everything and compare”. Prefer explicit worker roles.

### 1. `implement_and_review`

Use when the user wants a reliable default delivery flow.

- Codex: implement
- Claude Code: architecture / review / risk check
- OpenCode: optional alternative plan or follow-up patch strategy

### 2. `design_then_build`

Use when UI, UX, or solution framing needs a first pass before coding.

- planning / design worker: Claude Code or another design-capable tool if available
- Codex: implementation
- Claude Code: post-implementation review

### 3. `investigate_then_fix`

Use when the failure mode is unclear.

- Claude Code or OpenCode: isolate cause, inspect risks, propose strategy
- Codex: implement fix
- reviewer: verify regression coverage and edge cases

### 4. `parallel_compare`

Use only when the user explicitly wants comparison, diversity of solutions, or tool benchmarking.

- run multiple tools against the same scoped task
- compare outputs by correctness, maintainability, risk, and delivery speed

### 5. `pr_hardening`

Use after an implementation worker has produced a candidate result.

- reviewers run in parallel or sequence
- collect blocking vs non-blocking issues
- if needed, hand a repair brief back to the implementation worker

## Done policies

Completion must be defined by objective signals, not worker self-report.

### Feature task

Recommended checks:
- intended files changed
- build passes
- tests pass
- review completed or explicitly waived
- PR created when requested
- screenshot attached when UI changed and a screenshot requirement exists

### Bugfix task

Recommended checks:
- defect scope identified
- fix applied in intended area
- relevant tests pass or regression coverage added
- no new lint / type failures introduced

### Review-only task

Recommended checks:
- review artifact produced
- issues classified into blocking / non-blocking
- recommendation clearly stated

### Prototype task

Recommended checks:
- runnable artifact exists
- usage or launch instructions exist
- result is demonstrable even if production hardening is deferred

Always report:
- checks passed
- checks still pending
- checks failed
- whether the result is actionable now

## Retry policy

Not all retries are the same.

### Mechanical retry

Use when the failure is environmental or operational.

Examples:
- CLI startup glitch
- transient shell error
- workdir mismatch
- temporary tool availability issue
- one-off install or permission hiccup

In this case, retry the same task with corrected execution conditions.

### Semantic retry

Use when the worker moved in the wrong direction.

Examples:
- solved Y instead of X
- ignored required file or type definition
- produced an overbuilt design when a narrow fix was needed
- skipped tests or changed the wrong surface

In this case, do **not** just rerun the same prompt.

Generate a retry brief that includes:
- what the previous attempt did
- evidence of failure or mismatch
- what to preserve
- what to change
- extra context to inject
- the new acceptance focus

Example structure:

```text
Retry reason:
- Worker implemented a net-new creation flow.
- Required outcome is editing and reusing existing configuration.

Adjustments:
- Focus on reuse/edit flows, not greenfield creation.
- Reuse src/types/template.ts.
- Add tests for mutation of existing configuration objects.
- Do not spend time polishing unrelated UI.
```

## Progress reporting

Report objective state changes, not chatter.

### Include

- worker status per tool: queued / running / completed / failed
- current task lifecycle state
- whether work landed in the intended directory
- key artifact created
- done criteria met / unmet
- blocking issue if one exists
- recommended next action

### Report on

- major state change
- worker completion
- worker failure
- transition into review
- transition into retry
- final completion or terminal failure

### Stay concise when

- nothing material changed
- only timestamps changed
- the user did not request detailed check-ins

## Resource scheduling

The likely bottleneck is often local machine capacity, not model intelligence.

Supervise concurrency intentionally.

### Suggested weighting

- review-only task = weight 1
- implementation task = weight 2
- build/test-heavy task = weight 3

### Suggested policy

- keep a configurable max total weight in flight
- queue additional tasks instead of launching everything at once
- avoid overlapping heavy installs/builds unless the machine can handle them
- isolate implementation tasks into separate worktrees

If RAM, CPU, or disk pressure becomes the real limit, treat that as a scheduler concern rather than a worker failure.

## Bundled scripts

Read and use these files from the skill assets when they exist:
- `assets/scripts/run-codex.ps1`
- `assets/scripts/run-claude-code.ps1`
- `assets/scripts/run-opencode.ps1`
- `assets/scripts/route-task.ps1`
- `assets/scripts/multi-orchestrate.ps1`
- `assets/scripts/task-state.ps1`
- `assets/scripts/evaluate-done.ps1`
- `assets/scripts/generate-retry-brief.ps1`
- `assets/scripts/start-pipeline.ps1`
- `assets/scripts/supervise-task.ps1`
- `assets/scripts/launch-worker.ps1`
- `assets/scripts/reconcile-worker.ps1`

The scripts are worker adapters. The orchestration logic should live at the supervisor level.

## Operator controls

The orchestrator should support intervention.

Useful controls include:
- steer a running worker
- pause or stop a task
- cancel a task
- relaunch from a corrected workdir
- reassign the task to another tool
- trigger review-only follow-up
- promote a failed implementation into an investigate-first pipeline

## Known issues and mitigation

### 1. Path drift across mounted workspaces

Problem:
A tool may not see the intended OpenClaw workspace path and may silently continue in another mounted path.

Mitigation:
- inspect the actual reachable workdir before delegating
- verify output landed in the intended project directory
- if drift is detected, stop and relaunch with a corrected directory

### 2. Noisy wrapper output

Problem:
Wrapper output can still include startup banners, MCP warnings, and shell-specific error framing.

Mitigation:
- treat cleaned summaries as best-effort
- inspect raw excerpts when results look suspicious
- tighten cleaning rules over time based on real outputs

### 3. False completion

Problem:
A worker process can exit even though the real task is not review-ready or done.

Mitigation:
- use done policies tied to objective checks
- separate worker exit from task completion state
- require explicit supervisor transition to `completed`
- if a worker only produces analysis or a patch plan, do not mark implementation complete unless repo changes actually landed

### 4. Adapter-layer execution failure

Problem:
A worker adapter or wrapper may fail even when the underlying worker logic is still usable.
Examples include PowerShell wrapper framing, stdout/stderr capture quirks, or PTY / shell integration issues.

Mitigation:
- classify wrapper failures separately from task failures
- distinguish adapter failure from implementation failure in supervisor summaries
- if needed, relaunch the same worker brief through a simpler execution path while preserving supervisor-only boundaries
- do not silently rewrite task history to make an adapter failure look like product progress

### 5. Static retries

Problem:
Blindly rerunning the same prompt wastes time and tokens when the first attempt misunderstood the task.

Mitigation:
- classify retries as mechanical vs semantic
- generate retry briefs for semantic failures
- preserve evidence from the failed attempt

### 6. Lightweight prototype bias

Problem:
The orchestrator may prefer a lightweight prototype path when the task is ambiguous, even if the user would benefit from a more structured stack.

Mitigation:
- ask or decide explicitly between rapid prototype and maintainable project modes
- use review output to validate stack choice before implementation

### 7. Write-blocked worker runtimes

Problem:
A worker may be able to inspect and reason about the target repo but still be unable to apply edits because the runtime is read-only or policy-blocked.

Mitigation:
- classify this as an environment or policy blocker, not a semantic task failure
- preserve the worker's exact patch plan as an artifact
- mark implementation checks as pending when no repo changes landed
- let the supervisor report that the task is blocked-by-runtime-write-capability rather than blocked-by-unclear-requirements

## Practical patterns learned

### Implementation + audit split

A strong default for real coding work is:
- **Codex**: implementation lead
- **Claude Code**: architecture / audit / review
- **OpenCode**: alternative plan or session-style supplement

### Reviewers are role-based, not democratic

The point of multiple workers is not equal voting. The point is specialized pressure from different angles.

Prefer:
- one implementation lead
- one architecture/risk reviewer
- one optional alternative-plan or repair worker

### Objective completion beats conversational completion

Do not ask a worker “are you done?” when you can inspect:
- process state
- files created
- git diff
- test results
- review artifact existence
- PR existence

### Start narrow, then automate discovery

Before adding proactive task discovery from meeting notes, bug trackers, or logs, first make sure the orchestrator can:
- persist tasks
- supervise retries
- enforce done policies
- schedule safely

## Output contract

When reporting back to the user, prefer this shape:
- current lifecycle state
- what each worker contributed
- objective checks passed / failed / pending
- consensus
- differences
- recommendation
- next action
- blocker classification when relevant
- whether implementation actually landed in the repo or only an analysis/patch artifact was produced

## Blocker classification

When a task cannot advance, classify the blocker explicitly.
Do not collapse all failures into a generic blocked state.

Recommended blocker types:
- `environment`
  - runtime missing required capability
  - repo path unavailable
  - missing dependencies in allowed environment
- `policy`
  - write commands blocked
  - execution path denied by sandbox or policy gate
- `adapter`
  - wrapper script failure
  - PTY or stdout/stderr integration failure
  - orchestration-layer execution bug
- `implementation`
  - worker found a real product/code issue that still needs changes
- `semantic`
  - worker misunderstood the task or changed the wrong scope
- `mixed`
  - multiple blocker classes materially apply

Supervisor reporting should name:
- blocker type
- evidence
- whether retrying unchanged would help
- recommended next action

## Terminal and near-terminal supervisor outcomes

Use explicit end-state wording in summaries even when the internal task state machine remains simple.

Recommended outcome labels:
- `completed`
- `completed-with-analysis-only`
- `blocked-by-environment`
- `blocked-by-policy`
- `blocked-by-adapter`
- `changes-requested`
- `ready-for-hardening`
- `retry-with-semantic-brief`
- `awaiting-writable-runtime`

Notes:
- `completed-with-analysis-only` is useful when the worker produced a valid artifact, review, or patch plan, but did not land repo changes.
- `awaiting-writable-runtime` is useful when implementation scope is clear and bounded, but no writable worker runtime is available.
- `blocked-by-adapter` should be used when the worker path failed in the orchestration wrapper layer and the product task itself may still be viable.

## Operator quick start

For the current v2 scaffold, the practical operator flow is:
1. initialize a task record
2. move it to `queued`
3. run `supervise-task.ps1` with `-AutoLaunch` for safe automatic worker launch
4. add `-AutoProbe` when you want a lightweight repo/runtime probe before deeper execution
5. run `reconcile-worker.ps1` or `supervise-task.ps1` again to fold background worker state back in
6. only use retry generation when the problem is semantic rather than environmental

See also:
- `docs/README.md`
- `docs/usage-guide.md`
- `docs/operator-playbook.md`
- `docs/status.md`
- `docs/v2-summary.md`
- `docs/CHANGELOG.md`
- `docs/capability-map.md`
- `docs/script-interface.md`
- `docs/environment-failures.md`
- `docs/review-output-format.md`

## Publishing workflow

After stabilizing the local skill:
1. update `SKILL.md` and bundled scripts
2. verify local folder structure and task artifact paths
3. publish with `clawhub publish`
4. install/sync and validate in the local OpenClaw environment
