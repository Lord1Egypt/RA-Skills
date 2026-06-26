# Triage Boundary Contracts

Defines the exact handoff behavior between Triage and the systems that consume
its signals. Every consumer reads `.triage/signals.jsonl` and writes an
acknowledgment. No consumer receives pushed notifications — all pickup is
pull-based polling.

---

## Triage vs Dispatch

**Dispatch's role:** normalizes inbound communications, classifies message
intent, tracks threads, detects commitments and follow-up needs.

**Handoff to Triage:** when Dispatch produces an actionable item (a reply
needed, a commitment to fulfill, a follow-up required), it creates a Triage
task by writing to `.triage/queue.jsonl` with `origin: dispatch`.

**Pickup from Triage:** Dispatch polls `.triage/signals.jsonl` for
`task_ready` signals with `routing_hint: dispatch`. On pickup, it writes
`task_acknowledged` with `acknowledged_by: dispatch`.

**Hard boundary:**
- Triage never reads raw messages or email threads
- Dispatch never sets task priority or modifies queue order

---

## Triage vs Mentor

**Mentor's role:** manages task ordering and execution within an active
project. Decomposes goals into task graphs, supervises skills, handles failure
repair.

**Pickup from Triage:** Mentor polls `.triage/signals.jsonl` on each heartbeat
pass. It picks up unacknowledged `task_ready` signals with
`routing_hint: mentor`. On pickup, it writes `task_acknowledged` with
`acknowledged_by: mentor`, then creates or extends a project.

**Priority surfacing:** when a Mentor project is active, Mentor surfaces the
project's current priority score to Triage via a task record update. Triage
uses this score for preemption decisions. Mentor does not implement urgency
scoring or queue aging independently.

**Hard boundary:**
- Mentor never modifies `.triage/queue.jsonl` task order
- Triage never reaches into a Mentor project's internal task graph
- Triage does not invoke execution systems — Mentor decides how to execute
  code tasks, including whether to use a code execution tool

---

## Triage vs Base Agent

**Base agent's role:** handles short-path tasks that do not require project
orchestration or a dedicated skill invocation.

**Pickup from Triage:** the base agent polls `.triage/signals.jsonl` on every
activation. It picks up unacknowledged `task_ready` signals with
`routing_hint: direct` or `routing_hint: null`. On pickup, it writes
`task_acknowledged` with `acknowledged_by: agent`.

**Audit requirement:** short-path tasks handled directly by the agent must
still be registered in `.triage/queue.jsonl` before execution with
`routing_hint: direct`. This preserves a complete audit log even for tasks
that never require a skill.

---

## Signal Acknowledgment Protocol

Prevents double-pickup when multiple consumers run across overlapping heartbeat
cycles.

**Rule:** a `task_ready` signal with no corresponding `task_acknowledged` in
`.triage/signals.jsonl` within the same heartbeat window is eligible for
pickup. A signal with an `acknowledged` record is not.

**Consumers must:** write `task_acknowledged` as the first act of pickup,
before beginning execution.

**Triage must:** on each scoring cycle, check for `task_ready` signals older
than one heartbeat interval with no `task_acknowledged`. Re-emit if none found.

---

## What Triage Never Does

- Selects which skill executes a task
- Routes tasks to skills directly
- Decomposes tasks into subtasks
- Interprets domain intent (travel, finance, communication, etc.)
- Invokes any execution system
- Reads from any other skill's storage directory
- Writes to any path outside `.triage/`
