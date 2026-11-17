<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Dispatch Authorization: DA-{Project-ID}

---
generatedBy: AI-PPM
generatedVersion: {version}
source: portfolio-governance
generatedOn: {ISO-date}
ownership: generated
---

## Authorization Summary

| Field | Value |
|-------|-------|
| **Project ID** | {PRJ-XXX-YYYY-NNN} |
| **Project Name** | {name} |
| **Priority Rank** | #{rank} of {total} |
| **Authorization Type** | {Admit / Resume} |
| **Governance Decision** | PGD-{NNN} |
| **Authorized On** | {ISO-date} |
| **Authorized By** | {user role/name} |

---

## Execution Scope

| Aspect | Value |
|--------|-------|
| **Scope** | {Full Execution / Design Phase Only / Custom} |
| **Required Packages** | {ADLC, POLC, UXD, DWG, GCE, TGE — as applicable} |
| **Execution Pattern** | {ADLC + POLC + UXD parallel → DWG → GCE + TGE + DLC} |

---

## Constraints

| Constraint | Value | Enforcement |
|---|---|---|
| **Budget Ceiling** | ${amount} | Re-authorize if exceeded |
| **Timeline Deadline** | {date or "N months from dispatch"} | Escalate if at risk |
| **Team Allocation** | {max FTE / specific teams} | No reallocation without PPM approval |
| **Dependencies** | {list of cross-project dependencies to satisfy first} | Block until resolved |

---

## Source Artifacts

| Artifact | Location |
|----------|----------|
| Project Initiation Package (PIP) | {path to pilc-state.md} |
| ILC Brief (if applicable) | {path to ilc-state.md or "N/A"} |
| Portfolio Register Entry | {path to portfolio-register.md} |
| Governance Decision | {path to PGD-{NNN}.md} |

---

## Roll-Up Requirement

This project MUST provide portfolio roll-up data via AI-FLO at the governance cadence:

| Cadence | Minimum Fields Required |
|---------|------------------------|
| Biweekly (Portfolio Sync) | progress_pct, rag_status, top_blocker |
| Monthly (Health Review) | + budget_actual, velocity_trend, open_issues |
| On-demand (if anomaly) | Full snapshot as available |

---

## Revocation Conditions

This authorization is **automatically revoked** if:

1. Budget ceiling exceeded without re-authorization from PPM
2. Timeline deadline passes without delivery or formal extension
3. Portfolio rebalancing changes this project's priority below the active cut line
4. Governance gate decision (Stage 5) explicitly pauses or retires this project
5. Conditions in PGD-{NNN} are no longer met

**On revocation:** Project-layer packages should halt at next natural gate and await further instruction.

---

## FLO Routing Instructions

> *This section is read by AI-FLO to determine how to activate the Project layer.*

| Instruction | Value |
|-------------|-------|
| **Activate packages** | {list — e.g., "AI-ADLC, AI-POLC, AI-UXD"} |
| **Parallel/Sequential** | {parallel: ADLC+POLC+UXD; then sequential: DWG after all three} |
| **Point packages at** | {PIP location path} |
| **Project ID to propagate** | {PRJ-XXX-YYYY-NNN} |
| **Priority for scheduling** | #{rank} |

---

*This document is self-contained. AI-FLO reads only this file to activate the Project layer — no additional portfolio context needed.*
