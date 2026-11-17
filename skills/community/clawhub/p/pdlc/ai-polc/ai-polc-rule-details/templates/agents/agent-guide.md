<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-POLC
generatedVersion: "{version}"
source: ai-polc-rules/core-workflow.md
generatedOn: "{ISO-date}"
ownership: generated
purpose: Appended to destination workspace's .governance/AGENT-GUIDE.md
---

<!-- BEGIN AI-POLC AGENT GUIDE SECTION -->

## AI-POLC — Backlog Health Agent

AI-POLC ships one governance agent that validates the health of the Product Backlog Package (PBP).

### `backlog-health-agent` (BLH__)

**Domain:** Product backlog quality — structure, prioritization, quality bar, traceability, handoff readiness
**AG-ID:** POLC-AG-01
**Tier:** 1 (always available)
**Trigger:** `BLH__`

**What it checks (19 checks, 5 categories):**

| Category | Focus | Checks |
|----------|-------|:------:|
| B — Backlog Structure & Vision | Vision/goals exist, epics trace to goals, roadmap coherence, PO charter | 4 |
| P — Prioritization Coherence | All items ranked, single model applied, rationale recorded, re-prio triggers | 4 |
| Q — Quality Bar (DoR/DoD) | DoR+DoD exist & versioned, version sync, readiness checks, review cadence | 4 |
| T — Traceability & Lineage | intent→epic→story links, derivedFrom present, no orphans, projectId | 4 |
| R — Risk, Stories & Handoff | risk currency, INVEST stories (Tier 2), state status, downstream signals | 3 |

**When to call:**
- After PBP assembly (Stage 13), before setting `polc-state.md` status = `ready`
- Before each sprint/increment refinement (Stage 14)
- After any reprioritization or DoR/DoD change
- Per-release backlog-health check

**Recovery if skipped:** Run `BLH__` at any time — it reads the current backlog artifacts and `polc-state.md`. Fix Critical findings first (broken traceability, unranked active items, missing/mis-versioned DoR/DoD), then Major (missing rationale, stale items). If the PBP was already handed off, bump the version in `polc-state.md` so AI-DWG re-derives.

**Boundary:** `BLH__` validates the backlog *artifacts*; it never re-prioritizes, writes epics, or makes product decisions — those remain the product owner's, at the workflow's gates.

<!-- END AI-POLC AGENT GUIDE SECTION -->
