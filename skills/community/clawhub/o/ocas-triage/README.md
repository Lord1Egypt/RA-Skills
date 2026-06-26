# 🔀 Triage

System scheduler and priority queue manager. Determines what gets attention next across all pending work. Maintains a durable priority queue, scores work deterministically, emits pickup signals, injects heartbeat cadence into Mentor handoffs, and handles interrupts. One active task at a time. Deterministic scoring. Durable queue.

---

## 📖 Overview

Triage is a core OCAS component. Its only job is to determine what gets attention next. It maintains a durable priority queue, scores work deterministically, emits pickup signals, injects heartbeat cadence into Mentor handoffs, and handles interrupts.

---

## 🔧 Tool Surface

- `triage.task.add` — add work to the queue
- `triage.task.remove` — remove work from queue
- `triage.queue.list` — list all pending tasks with scores
- `triage.queue.status` — current queue state and active task
- `triage.interrupt` — preempt active work
- `triage.pause` / `triage.resume` — pause/resume queue processing
- Meta commands (bypass queue): `status`, `stop`, `pause`, `resume`

---

## 📊 Output & Journals

Maintains task queue (`queue.jsonl`), signal emissions with heartbeat assignments, and decision logs (`decisions.jsonl`). Every task logged with score breakdown and routing decision.

---

## ⏱️ Heartbeat & Background Tasks

**Heartbeat Injection** (CRITICAL in 1.2.0): When Triage scores a task with `routing_hint: mentor`, it MUST inject a `heartbeat_interval_seconds` into the `task_ready` signal before emission. This is not optional. Heartbeat intervals are priority-linked:

- **70–100 (high priority)** → 60 seconds
- **40–69 (medium priority)** → 10 minutes
- **0–39 (low priority)** → 1–6 hours (1 hour default)

`heartbeat_assigned` is recorded as a DecisionRecord `decision_type` for audit trail.

---

## 🛠️ Features

- **Deterministic priority scoring** — urgency + deadline proximity + consequence + interruption intent + completion bonus + queue aging
- **Task state lifecycle** — queued → active → completed/cancelled (with blocked, waiting_external states)
- **Durable queue** — persistent `queue.jsonl` for resume across sessions
- **Heartbeat governance** — priority-linked cadence prevents stalls (root cause fix: tasks no longer go idle overnight)
- **Signal schema versioning** — `task_ready` now has two variants: standard (non-Mentor) and Mentor handoff (with heartbeat fields)

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

See `references/` for detailed specifications and examples.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
