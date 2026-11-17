# OpenClaw Dashboard — Internal Engineering Review

> Audience: internal engineering / ops team  
> Purpose: summarize rationale, architecture decisions, execution path, and follow-up work

---

## 1. Problem Statement

Before refactor, we had rising complexity in three dimensions:
- feature delivery became slower (cross-file coupling)
- reliability fixes were hard to isolate
- agent-assisted coding had low patch precision on large monolithic contexts

We needed an architecture that supports:
1) faster incremental change
2) lower blast radius
3) higher machine-readability for agent workflows

---

## 2. Design Principles Adopted

### 2.1 Provider-as-boundary
Each backend provider owns one data contract and one domain:
- sessions
- ledger
- cron
- watchdog
- system
- spark
- tasks
- config

### 2.2 Frontend as composable tabs
Each tab owns UI logic and data transformations for one operational concern.

### 2.3 Ground Truth over scattered constants
Model/channel/cron metadata should come from an authoritative source to reduce drift.

### 2.4 Compatibility-first migration
Legacy surface retained during migration to avoid hard cutovers.

---

## 3. Execution Process (What we changed)

### Phase A — Modularization
- split backend into provider modules
- split frontend into tab/shared modules
- created cleaner API namespace while preserving compatibility paths

### Phase B — Visibility Enhancements
- redesigned top decision cards
- introduced stronger cost/model mix observability
- improved cron/watchdog operational signals

### Phase C — Data correctness and schema hardening
- fixed `/ops/ledger/today` field mismatch (`rows` vs `by_model`)
- canonicalized local model variants for consistent aggregation
- added deterministic color fallback for unknown models

### Phase D — Status bar/API reliability
- host status bar: improved fallback behavior and API coverage
- spark status: merged multiple data sources for runtime context
- added/extended API fields for versions and runtime task visibility

---

## 4. Key Technical Insights

1. **Schema drift is the silent killer**  
Frontend assuming a field that backend no longer serves causes false “no data” states.

2. **Compatibility layer is not optional**  
In live systems, migration must support old and new paths simultaneously.

3. **Agent-readable code is an architectural requirement**  
Small modules + explicit contracts significantly improve autonomous patch quality.

4. **Top-level UI should be intervention-oriented**  
First screen should answer “do I need to act now?”, not “show every metric”.

---

## 5. What Worked Well

- provider split reduced debugging scope
- card-level redesign improved operational decision speed
- iterative rollout in production-like environment avoided major regressions

---

## 6. What Didn’t Work / Friction Points

- dual runtime paths (`backend/server.js` vs legacy process) caused confusion
- endpoint shape inconsistency required repeated fallback logic
- status-bar data contracts were not explicit enough early on

---

## 7. Open Risks

- legacy and modular paths still coexist; ownership boundaries can blur
- if Ground Truth is not kept current, dashboard confidence degrades
- Spark endpoint variation across environments still requires defensive parsing

---

## 8. Next Actions

1. finalize runtime ownership (single default path)
2. formalize API contract docs (per provider)
3. add contract tests for critical endpoints (`/ops/system`, `/ops/dgx-status`, `/ops/ledger/today`)
4. continue reducing legacy dependency surface

---

## 9. TL;DR

This refactor is not just a UI update.  
It is a shift to **plug-in, agent-readable, operations-first architecture**.

That shift increases delivery speed, reduces operational risk, and sets the system up for sustained human+agent co-maintenance.
