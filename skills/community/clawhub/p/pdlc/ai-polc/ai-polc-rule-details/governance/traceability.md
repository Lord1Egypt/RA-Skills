<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 10: Traceability Spine

**Phase:** Governance
**Purpose:** Establish and maintain links from business intent → epic → (story) → acceptance → increment, so every backlog item justifies its existence and scope is auditable end-to-end.

---

## Purpose

Traceability answers: "Why does this item exist? What goal does it serve? What acceptance bar must it meet? Which release does it ship in?" Without traceability, scope drifts silently, features accumulate without justification, and post-mortems can't explain "why did we build X?"

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Simple Goal→Epic links only. One table. No outcome tracing. |
| **Standard** | Goal→Epic→Release links. Traceability matrix with coverage check. |
| **Comprehensive** | Full audit-grade matrix: Intent→Epic→Story→AC→Release→Outcome. Compliance evidence. Extension: Full Traceability activated. |

---

## Steps

### Step 10.1: Build the Traceability Matrix

**Minimal format (always produced):**

| Goal | Epic(s) | Release | Status |
|------|---------|---------|:------:|
| Reduce payment time to <2s | EPIC-001, EPIC-003 | R1 (MVP) | In Progress |
| Support 3 providers | EPIC-002, EPIC-004, EPIC-006 | R2 | Planned |
| Reduce onboarding drop-off | EPIC-005 | R1 (MVP) | In Progress |

**Standard format (adds release + AC linkage):**

| Goal | Epic | Epic AC Count | Release | Priority Rank | Dependencies |
|------|------|:---:|---------|:---:|---|
| Payment <2s | EPIC-001: Async Processing | 4 | R1 | 2 | Depends: EPIC-003 |
| Payment <2s | EPIC-003: Provider Abstraction | 3 | R1 | 1 | Blocks: EPIC-001, EPIC-002, EPIC-004 |
| 3 Providers | EPIC-002: Stripe | 3 | R2 | 4 | Depends: EPIC-003 |

### Step 10.2: Verify Coverage

Run a coverage check:

- [ ] **Goal coverage:** Every product goal has at least one epic serving it
- [ ] **Epic coverage:** Every epic links to at least one goal
- [ ] **Release coverage:** Every prioritized epic appears in exactly one release
- [ ] **No orphans:** No epics exist without goal linkage
- [ ] **No gaps:** No goals exist without serving epics

Flag any violations:
```
⚠️ Coverage gaps found:
• Goal "Reach 10K MAU" has no serving epic — needs decomposition
• EPIC-008 has no goal linkage — justify or remove
```

### Step 10.3: Upstream Traceability (Chain Mode)

If PIP available, extend the chain upward:

| PIP Business Objective | Product Goal | Epic(s) |
|---|---|---|
| "Increase revenue by 20%" | Payment <2s, 3 Providers | EPIC-001, EPIC-002, EPIC-003, EPIC-004 |
| "Acquire 10K users by Q4" | Reduce onboarding drop-off | EPIC-005 |

This proves: every project objective maps to product work. Stakeholders can see the path from "what we approved" to "what's being built."

### Step 10.4: Downstream Traceability (When DLC Feedback Available)

During Operations (Stage 15), extend the chain downward:

| Epic | Stories (from DLC) | Completion Status | Increment |
|------|---|:---:|---|
| EPIC-001 | Story 1.1, 1.2, 1.3 | 2/3 done | R1-Sprint3 |
| EPIC-003 | Story 3.1, 3.2 | 2/2 done ✅ | R1-Sprint2 |

This is populated as AI-DLC v1 completes work — not at initial creation.

### Step 10.5: Persist Traceability Matrix

Write `traceability-matrix.md` with:
- Core matrix (goal → epic → release → status)
- Coverage check results
- Upstream links (PIP objectives → goals) if chain mode
- Downstream placeholder (populated during Operations)
- Last verified date

---

## Extension: Full Traceability

If triggered ("full traceability" / compliance context), load `extensions/full-traceability.md` and additionally produce:
- Audit-grade matrix (Intent→Epic→Story→AC→Increment→Outcome)
- Compliance evidence mapping (which regulatory requirement maps to which AC)
- Change impact tracing (when a goal changes, which epics are affected?)
- Outcome tracking (did the delivered increment achieve the goal's metric?)

---

## Gate

**Gate 10 — Traceability Confirmed:**

Present to user:
```
Traceability established:
• Goals covered: {N}/{N} ✅ (or ⚠️ if gaps)
• Epics linked: {N}/{N} ✅ (or ⚠️ if orphans)
• Releases mapped: {N}/{N} ✅

{If gaps: list them}

Traceability will be maintained and extended as work progresses.
Approve to proceed to Phase 4 (Stakeholders), or fix gaps first.
```

User must confirm. This is also the **Phase 3 gate** — Governance complete.

---

## Governance Spine Entry

Log in Decision Log:
```
POLC-D-009: Traceability matrix established. 
{N} goals → {N} epics → {N} releases.
Coverage: {complete | gaps identified}.
```

---

## Transition

→ **Phase 4, Stage 11: Stakeholder Management** (Stakeholders & Communication begins)

---

*Detail file for AI-POLC Stage 10 | Phase: Governance*
