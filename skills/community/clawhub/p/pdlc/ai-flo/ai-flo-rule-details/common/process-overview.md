<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-FLO — Process Overview

**Purpose:** High-level map of the entire AI-FLO engine. Reference this to understand how routing works, where you are, and how the pieces connect.

---

## Engine at a Glance

```
Phase 1: CONFIGURE           Phase 2: ROUTE              Phase 3: MONITOR
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│ 1. Workspace    │         │ 4. Dispatch     │         │ 8. Position     │
│    Detection    │         │    (Down)       │         │    Tracking     │
│ 2. Routing     │────────▶│ 5. Fan-Out /    │────────▶│ 9. Roll-Up      │
│    Table Build  │         │    Fan-In       │         │    Relay        │
│ 3. Flow State  │         │ 6. Handoff      │         │10. Health,      │
│    Init        │         │    Execution    │         │    Conflicts    │
│                 │         │ 7. Exceptions   │         │    & Alerts     │
│                 │         │    & Overrides  │         │                 │
└─────────────────┘         └─────────────────┘         └─────────────────┘

         ONE-TIME                  ON DEMAND              CONTINUOUS
     (first session)          (each routing event)     (background awareness)
```

---

## Phase Summary

| Phase | Name | Purpose | Stages | Execution |
|-------|------|---------|--------|-----------|
| 1 | **Configure** | Detect topology, build routing table, initialize state | 1–3 | Once (then resume) |
| 2 | **Route** | Dispatch, coordinate fan-out/fan-in, execute handoffs, handle exceptions | 4–7 | On demand (each routing event) |
| 3 | **Monitor** | Track positions, relay roll-up, detect conflicts/stalls | 8–10 | Continuous |

---

## Stage Detail

| # | Stage | Always/Conditional | Primary Deliverable | Gate? |
|---|-------|-------------------|---------------------|:-----:|
| 1 | Workspace Detection | Always | Topology mode + package inventory | ✅ |
| 2 | Routing Table Build | Always | `routing-table.md` | ✅ |
| 3 | Flow State Init | Always | `flo-state.md` + configuration | ✅ |
| 4 | Dispatch (Down) | Always (when dispatch exists) | Dispatch records | ✅ |
| 5 | Fan-Out / Fan-In | Conditional (graph topology) | Readiness checks | ✅ |
| 6 | Handoff Execution | Always | Handoff instructions + routing log | ✅ |
| 7 | Exceptions & Overrides | Conditional (exception triggered) | Updated state + spine entry | ✅ |
| 8 | Position Tracking | Always (continuous) | Updated `flo-state.md` | ❌ |
| 9 | Roll-Up Relay | Always (on request/schedule) | Roll-up report | ✅ |
| 10 | Health, Conflicts & Alerts | Always (continuous) | Conflict alerts, stall warnings | ❌ |

---

## Interaction Model

AI-FLO operates in three modes depending on context:

| Mode | Triggered By | Behavior |
|------|-------------|----------|
| **Dashboard** | `status`, `route map`, `where is...` | Shows state — read-only |
| **Command** | `dispatch`, `override`, `toggle`, `cancel` | Executes actions — confirmation required |
| **Alert** | Automatic (conflict, stall, readiness) | Surfaces proactively — operator decides |

---

## Workspace Topology Modes

| Mode | Setup | FLO Behavior |
|------|-------|-------------|
| **1 — Co-located** | Portfolio + Project in one workspace | All scans local |
| **2 — Hub-and-Spoke** | Portfolio + local project + remote projects | Local scans + remote references |
| **3 — Fully Distributed** | Portfolio workspace only; all projects remote | Remote references + operator-reported status |

Topology is detected at Stage 1 and stored in `flo-state.md`.

---

## Routing Model

```
Canonical Family Chain (default):

  AI-ILC ⇢ AI-PILC ──────────────────────────────────────┐
                │                                          │
              AI-PPM (portfolio decisions)                 │
                │                                          │
             AI-FLO (dispatch down)                        │
                │                                          │
                └──► AI-POLC ──► AI-UXD ──► AI-ADLC ──► AI-DWG ──► AI-DLC v1
                                                AI-GCE + AI-TGE (alongside)
                                                      │
                                                   AI-FLO (roll-up up)
                                                      │
                                                   AI-PPM (portfolio view)
```

- **Down:** PPM → FLO → AI-POLC (sequential chain starts)
- **Up:** Project layer → FLO → PPM (roll-up)
- **Same-layer:** Direct marker detection (no FLO needed)
- **Sequence:** POLC → UXD → ADLC → DWG (each feeds the next)

---

## Conflict Management

| Severity | Meaning | FLO Action |
|----------|---------|------------|
| **Critical** | Cannot proceed safely | HOLD + alert + timeout-with-fallback |
| **Warning** | Proceed with risk | Alert + recommend; don't hold |
| **Info** | Noted | Log only |

**Anti-deadlock guarantee:** No hold lasts forever. Configurable timeouts + deterministic fallback rules + operator force-through always available.

---

## Key Principles

1. **Advisory, not autonomous** — records decisions for human action
2. **Carry, don't decide** — PPM decides; operator overrides; FLO routes
3. **Log everything** — every hop, override, toggle, conflict recorded
4. **Flag, never suppress** — conflicts always surface
5. **Canonical default, governed deviation** — family chain is default; deviations are explicit
6. **Topology-aware** — adapts to Mode 1/2/3
7. **Additive, not blocking** — without FLO, family still works via direct markers

---

*Part of AI-FLO v1.0.0 | Reference: core-engine.md for full orchestration logic*
