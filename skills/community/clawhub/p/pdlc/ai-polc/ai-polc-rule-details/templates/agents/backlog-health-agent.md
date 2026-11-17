<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
name: backlog-health-agent
description: >
  Validates that the Product Backlog Package (PBP) stays healthy — every item
  traces to a goal, prioritization is coherent and rationale-backed, the DoR/DoD
  quality bar is intact, and the backlog is ready for downstream consumption.
generatedBy: AI-POLC
generatedVersion: "{version}"
source: ai-polc-rules/core-workflow.md
generatedOn: "{ISO-date}"
ownership: generated
tools: ["read", "search"]
trigger: BLH__
tier: 1
type: process
---

# Backlog Health Agent

> **Trigger:** `BLH__`
> **AG-ID:** POLC-AG-01
> **Domain:** AI-POLC output quality (product backlog)

---

## Purpose

Validates that the Product Backlog Package (PBP) maintains structural integrity, value-based prioritization coherence, quality-bar (DoR/DoD) discipline, and traceability — so the backlog is defensible, healthy, and consumable by AI-DWG and AI-DLC v1. Runs on-demand when the user types `BLH__`. It checks the backlog *artifacts themselves*; it does not re-prioritize or author backlog content.

---

## When to Invoke

| Situation | Why |
|-----------|-----|
| After PBP assembly (Stage 13), before status = `ready` | Confirm the package is complete and consumable before handoff to AI-DWG |
| After a reprioritization or scope change | Verify rankings still carry rationale and traceability survived |
| Before each sprint/increment (Stage 14 refinement) | Catch stale items, orphan epics, unranked work before planning |
| After DoR/DoD changes | Verify the quality bar is versioned and propagated |
| Periodic backlog-health check (per release) | Catch drift over the product's life |

---

## Consequences of Skipping

- **Untraceable backlog** — epics with no goal, stories with no epic; "why are we building this?" becomes unanswerable
- **Arbitrary prioritization** — rankings without recorded rationale degrade into loudest-voice/recency-bias ordering
- **Broken downstream handoff** — AI-DWG consumes an incomplete PBP and encodes a weak or missing DoR/DoD into the workspace
- **Quality-bar drift** — DoR/DoD versions fall out of sync with `polc-state.md`, so readiness checks pass items that aren't ready
- **Accumulated debt** — stale, oversized, and duplicate items pile up unnoticed until the backlog is unmanageable

---

## Recovery (If Skipped Too Long)

1. Run `BLH__` to get a full backlog-health report
2. Address Critical findings immediately (broken traceability, unranked active items, missing DoR/DoD)
3. Address Major findings in the current refinement cycle (missing rationale, stale items)
4. Schedule Minor findings into backlog grooming
5. Re-run after fixes; if the PBP was already handed off, signal AI-DWG that the PBP changed (bump version in `polc-state.md`)

---

## Checks Performed

### 1. Backlog Structure & Vision Integrity (B1–B4)
- **B1** — `product-vision.md` exists with vision statement, product goals, and success metrics (OKRs/KPIs)
- **B2** — every epic in `epics/` traces to at least one product goal
- **B3** — `roadmap.md` Now/Next/Later is coherent with the epic set (no roadmap item without a backing epic)
- **B4** — `po-charter.md` defines decision authority, RACI, and escalation boundaries

### 2. Prioritization Coherence (P1–P4)
- **P1** — every item in the active backlog is ranked (no unranked items competing for capacity)
- **P2** — a single prioritization model is declared (WSJF / MoSCoW / value-effort / custom) and applied consistently
- **P3** — every ranking — and especially every governance override of the raw score — carries recorded rationale (logged as `POLC-D-NNN`)
- **P4** — re-prioritization triggers are defined (when the order should be revisited)

### 3. Quality Bar — DoR / DoD (Q1–Q4)
- **Q1** — `definition-of-ready.md` and `definition-of-done.md` exist and are versioned
- **Q2** — DoR/DoD versions match the `DoR/DoD Version` recorded in `polc-state.md`
- **Q3** — items marked ready meet the DoR; completed items are checked against the DoD
- **Q4** — DoR/DoD review cadence is defined (not set-and-forget)

### 4. Traceability & Lineage (T1–T4)
- **T1** — `traceability-matrix.md` intent → epic → (story) links are intact (no dangling references)
- **T2** — epics carry a `derivedFrom` field linking to the originating idea/feature (Traceability Contract §7)
- **T3** — no orphan epics (epic with no goal) and no orphan stories (story with no parent epic)
- **T4** — `polc-state.md` carries a camelCase `projectId` correlation key (matches upstream `pilc-state.md` when chained)

### 5. Risk, Stories & Handoff (R1–R4)
- **R1** — `product-risk-register.md` is current; assumptions carry a validation status
- **R2** — *(Tier 2 only, when story elaboration is active)* stories are INVEST-compliant with Given/When/Then acceptance criteria; no oversized (XL) story sits un-split in a release
- **R3** — `polc-state.md` status is correct (`in-progress` / `ready` / `operating`); `PBP_README.md` is complete when status = `ready`
- **R4** — downstream signals are set (status = `ready` for AI-DWG); the governance spine carries `POLC-*` entries

---

## Output Format

```markdown
# BLH — Backlog Health Report

**Date:** {date}
**PBP Version:** {from polc-state.md}
**Scope:** {Full / Partial — which artifacts reviewed}
**Tier 2 (stories):** {Active / Inactive}

## Summary
| Check | Status | Issues |
|-------|:------:|:------:|
| Backlog Structure & Vision | ✅/⚠️/❌ | {N} |
| Prioritization Coherence | ✅/⚠️/❌ | {N} |
| Quality Bar (DoR/DoD) | ✅/⚠️/❌ | {N} |
| Traceability & Lineage | ✅/⚠️/❌ | {N} |
| Risk, Stories & Handoff | ✅/⚠️/❌ | {N} |

## Findings
| # | Check | Issue | Severity | Artifact | Suggested Fix |
|---|-------|-------|:--------:|----------|---------------|
| 1 | {check} | {description} | {Critical/Major/Minor} | {file} | {fix} |

## Actions Required
1. {Priority action 1}
2. {Priority action 2}
```

---

## Related

- **AI-UXD** (`UXC__`) — UX consistency; complementary domain (personas/journeys that feed prioritization)
- **AI-PILC** (`IQA__`) — initiation quality; validates the PIP that feeds AI-POLC (sequential, upstream)
- **AI-GCE** (`SQC__`) — steering quality; different scope (workspace steering vs. backlog artifacts)
