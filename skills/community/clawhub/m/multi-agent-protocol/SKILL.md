---
name: multi-agent-protocol
description: >
  OpenClaw-native v2 protocol for spec-first multi-agent delivery. Use when you need
  2+ agents with explicit phase control, dual review gates, bounded retry/circuit
  breaker behavior, Lobster approval/recovery for side effects, OpenProse orchestration,
  typed plugin tools backed by SQLite/event log for task state, and ACP integration for
  external coding harnesses such as Codex. Avoid when a single agent or prompt-only
  delegation is enough.
---

# Multi-Agent Protocol v2

OpenClaw-native multi-agent protocol. Keep the good parts from v1:

- spec-first
- review gates
- retry with circuit breaker

Replace the brittle parts from v1:

- no fixed `sessionKey` memory contract
- no `shared/blackboard.json`
- no undeclared `beads` or `git` dependency
- no prompt-only state machine
- no LangGraph

## Architecture

Use the stack below and do not silently swap layers:

1. `SKILL.md`
   Defines protocol, roles, dependency expectations, and non-negotiable rules.
2. `OpenProse`
   Owns orchestration flow and agent dispatch.
3. `Lobster`
   Owns approval, pause/resume, and side-effect recovery templates.
4. `task-store` plugin
   Owns authoritative task state via typed tools + SQLite event log.
5. `ACP`
   Connects external coding harnesses such as Codex.

## Source Of Truth

The source of truth is the `task-store` plugin, not prompts and not reviewer output.

- Canonical task phase lives in SQLite.
- Every phase change is an event.
- Reviewers append findings and verdicts.
- Reviewers do **not** finalize phase transitions.
- The orchestrator is the only actor that decides phase movement.

## Required Dependencies

Declare these dependencies explicitly in the skill or the workflow setup:

- OpenClaw runtime with `OpenProse`
- `Lobster` runtime for approval/resume
- `task-store` plugin enabled
- local SQLite availability
- ACP bridge when external harnesses are involved

Optional, but explicit when used:

- `git`
- browser/runtime plugins
- language-specific build tools

Do not assume:

- `beads`
- `bd`
- `shared/blackboard.json`
- persistent role memory through fixed sessions
- `git worktree`

## Core Rules

### 1. Spec-first

No execution phase starts before a spec record exists in `task-store`.

Minimum spec payload:

- `goal`
- `scope_in`
- `scope_out`
- `inputs`
- `outputs`
- `acceptance_criteria[]`
- `risks[]`

If acceptance criteria are weak or missing, the orchestrator keeps the task in `spec_draft`.

### 2. Phase transitions are explicit

Use a stored phase enum. Recommended baseline:

```text
spec_draft
spec_review
execution_ready
executing
spec_gate
quality_gate
awaiting_approval
ready_to_resume
completed
failed
circuit_open
```

All transitions must be written through `task_transition`.

### 3. Reviewers are evidence producers

Reviewer output is evidence, not authority.

- Spec reviewer answers: "Does the artifact satisfy the spec?"
- Quality reviewer answers: "Is the implementation acceptable for maintainability and risk?"
- Reviewers write findings via `task_append_review`.
- The orchestrator reads review state and decides the next phase.

### 4. Retry and circuit breaker are stored state

Retries are not tracked in free text.

- attempt counters live in SQLite
- retry reasons are evented
- circuit state is explicit

Recommended policy:

- `attempt 1-2`: retry same phase with bounded backoff
- `attempt 3`: optional stronger model/runtime
- `attempt >= 4`: `circuit_open`

### 5. Side effects require Lobster gates

Any real-world effect should pass through Lobster:

- writing to external systems
- approvals
- irreversible file mutations outside the declared sandbox
- deployments
- notifications
- merges

Lobster pauses, requests approval, and resumes from persisted state.

### 6. ACP is the bridge for external harnesses

When using Codex or another external coding harness:

- launch work through ACP, not prompt-only relays
- pass `task_id`, `attempt_id`, `workspace`, and allowed capabilities
- capture external session metadata as non-authoritative references

Practical note inferred from the local OpenClaw installation: parent streaming features such
as `streamTo` are tied to `runtime=acp`, not generic subagent runtime. Design the workflow
accordingly.

## Role Model

### Orchestrator

The orchestrator:

- creates the task record
- validates spec completeness
- dispatches agents
- reads stored findings
- decides phase transitions
- triggers Lobster when approval or recovery is needed
- opens the circuit when retries are exhausted

The orchestrator does **not** become a passive message relay or free-form blackboard parser.

### Executor

The executor may be:

- a local OpenClaw worker
- an ACP-backed external harness such as Codex
- a read-only research agent

Executor responsibilities:

- produce artifacts
- record attempt heartbeat/checkpoints through typed tools
- report structured outputs and evidence

Executor cannot finalize `completed`, `failed`, or gate transitions on its own.

### Spec Reviewer

Reads the actual artifact and records one of:

- `approved`
- `changes_requested`
- `blocked`

Plus findings with file references or artifact references.

### Quality Reviewer

Reads the actual artifact after spec gate passes and records:

- maintainability concerns
- test gaps
- safety or regression risk
- approval/rework recommendation

### Lobster Approver / Recovery Actor

Lobster manages:

- approval prompts
- pause/resume after interruption
- resuming idempotent or compensating side-effect steps

Lobster does not own the business workflow phase. It only writes approval state and recovery
evidence back to `task-store`.

## Minimal Lifecycle

```text
task_create
  -> spec_review
  -> execution_ready
  -> executing
  -> spec_gate
  -> quality_gate
  -> awaiting_approval (only if side effects exist)
  -> ready_to_resume
  -> completed
```

Failure branches:

```text
executing -> retrying -> executing
executing -> circuit_open
spec_gate -> execution_ready
quality_gate -> execution_ready
awaiting_approval -> failed
```

## Protocol By Phase

### `spec_draft`

- Create task in `task-store`.
- Persist full spec content or spec reference.
- Do not spawn builders yet.

### `spec_review`

- Reviewer checks the spec itself for ambiguity and testability.
- Orchestrator either:
  - fixes the spec and stays in `spec_draft`, or
  - transitions to `execution_ready`

### `execution_ready`

- Orchestrator chooses runtime:
  - local worker for low-side-effect or local tasks
  - ACP for Codex/external harness
- Orchestrator creates a new attempt record.

### `executing`

- Executor works only against declared inputs/outputs.
- Checkpoints go through typed tools.
- Side effects are declared ahead of time as planned actions.

### `spec_gate`

- Spec reviewer inspects produced artifact.
- Reviewer writes findings only.
- Orchestrator decides:
  - pass to `quality_gate`
  - rework back to `execution_ready`
  - open circuit if repeated mismatch indicates spec or implementation collapse

### `quality_gate`

- Quality reviewer records findings only.
- Orchestrator decides:
  - `completed`
  - `execution_ready`
  - `awaiting_approval`

### `awaiting_approval`

- Lobster requests human approval with structured context.
- Approved result becomes evidence in store.
- Orchestrator transitions to `ready_to_resume`.

### `ready_to_resume`

- Lobster or orchestrator resumes the exact side-effect step using persisted idempotency data.

### `circuit_open`

- Stop automatic retries.
- Surface:
  - failure summary
  - attempts
  - last known good artifact
  - unblock options

## What Goes In Storage

The `task-store` plugin should persist at least:

- task header
- current phase
- spec payload or reference
- review records
- attempt records
- artifact records
- approval records
- event log
- optional external session references

The plugin storage is authoritative. Prompt text is not.

## OpenProse Guidance

The `.prose` workflow should be minimal and boring:

- read state
- branch on typed state
- dispatch one actor
- store result
- decide next phase

Do not encode business state only in the prose graph. The graph coordinates. The plugin stores.

Read [workflows/openclaw-native-v2.prose](workflows/openclaw-native-v2.prose) when wiring the
workflow.

## Lobster Guidance

Use Lobster only where it adds hard guarantees:

- approval request with resumable context
- idempotent recovery after interruption
- controlled side-effect replay

Read [lobster/approval-recovery.template.yaml](lobster/approval-recovery.template.yaml) when a
task contains side effects or human approval.

## Plugin Guidance

Use the `task-store` plugin as the only write path for protocol state.

Read [references/task-store-plugin.md](references/task-store-plugin.md) when:

- implementing the plugin
- validating tool shapes
- deciding schema changes

## Permissions

Use least privilege. The matrix lives in
[references/agent-permissions.md](references/agent-permissions.md).

Key rule:

- executors can write artifacts and attempts
- reviewers can write findings
- only orchestrator can move the phase

## Migration Rules From v1

Read [references/migration.md](references/migration.md) before replacing an existing v1 setup.

Summary:

- replace fixed session identity with run-scoped `attempt_id` and optional `external_session_ref`
- replace blackboard with typed storage
- replace beads/git buses with plugin tools
- replace reviewer-led state changes with orchestrator-led transitions

## Quick Start

1. Enable `task-store`.
2. Create a task with a full spec.
3. Run the OpenProse workflow.
4. Route external coding work through ACP.
5. Use Lobster only for approval/recovery steps.
6. Let orchestrator decide every phase transition from stored evidence.

## Anti-Patterns

Do not do any of the following:

- use fixed role `sessionKey` as the memory backbone
- store canonical state in `shared/blackboard.json`
- let reviewer verdict directly close the task
- let executor mutate final phase
- assume `git` or `beads` exists without declaring it
- recover from interruption by guessing from prompt history
- add LangGraph just to simulate a state machine already held in SQLite
