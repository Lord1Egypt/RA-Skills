<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 15: Acceptance & Feedback Loop

**Phase:** Operations (repeating)
**Purpose:** Accept or reject completed increments against the DoD, process execution feedback from AI-DLC v1, and translate learnings into backlog/priority adjustments.

---

## Purpose

This is the PO's acceptance authority in action. AI-DLC v1 builds; AI-POLC judges whether what was built meets the product bar. This stage also processes blockers, velocity data, and runtime feedback to inform the next prioritization cycle.

---

## Behavior by Mode

| Mode | Stage 15 Behavior |
|------|------------------|
| **Standalone** | PO reviews manually delivered work against DoD. |
| **Chain with DLC** | PO reads `aidlc-docs/` for DLC completion records and judges against DoD. |

---

## Steps

### Step 15.1: Scan DLC Output (Chain Mode)

Read `aidlc-docs/` for changes since last POLC session:

| Signal | What It Means | PO Action |
|--------|--------------|-----------|
| Bolt completed (story done) | Story implemented, tested, deployed | Verify against DoD → Accept/Reject |
| Epic fully done (all stories complete) | Epic delivered | Verify against epic AC → mark epic complete |
| Blocker reported | Story can't proceed | Assess → reprioritize or escalate |
| Velocity data | Team throughput for this period | Update release plan forecasts |

### Step 15.2: Accept/Reject Increments

For each completed epic or story (if Tier 2 active):

**Acceptance checklist (from DoD):**
- [ ] All acceptance criteria verified (pass/fail)
- [ ] No P1/P2 bugs in scope
- [ ] Tests passing
- [ ] PO judgment: "Does this solve the user's problem?"

**Decision:**

| Verdict | Action |
|---------|--------|
| **Accept** | Mark epic/story as DONE in traceability matrix. Update release progress. |
| **Reject** | Document what's missing. Item returns to backlog with specific gap description. |
| **Accept with conditions** | Accept for now; create follow-up epic for gaps. |

Log each acceptance decision: `POLC-D-NNN: Accepted EPIC-XXX — all {N} AC met.` or `POLC-D-NNN: Rejected EPIC-XXX — AC {N} not met: {reason}.`

### Step 15.3: Process Blockers

For each blocker reported by DLC:

1. **Assess impact:** Which epics are affected? Which releases?
2. **Decision options:**
   - Remove the blocker (PO can resolve — e.g., clarify requirement)
   - Escalate (per PO Charter escalation path)
   - Reprioritize around it (move blocked epic down, pull alternative forward)
   - Accept delay (update release plan timeline)
3. **Log:** `POLC-I-NNN: Blocker on EPIC-XXX — {description}. Resolution: {action taken}.`

### Step 15.4: Update Traceability

After acceptance/rejection:
- Update `traceability-matrix.md` status column
- Update epic completion percentage
- Update release progress (e.g., "R1: 4/6 epics done")

### Step 15.5: Reprioritize Based on Learnings

If acceptance/feedback reveals new information:
- Feature shipped but adoption is low → investigate; maybe next epic should address adoption
- Blocker reveals dependency not previously identified → add to risk register
- Velocity data shows team is faster/slower than expected → adjust release plan

Trigger Stage 14 (Backlog Ops) if significant reprioritization needed.

### Step 15.6: Persist State

Update:
- `polc-state.md` (upstream read timestamps, backlog summary)
- `traceability-matrix.md` (completion status)
- `release-plan.md` (progress tracking)
- `management_framework/` (decisions, issues, changes)

---

## Gate

**Gate 15 — Acceptance Complete:**

Present to user:
```
Acceptance & feedback processed:
• Accepted: {N} epics/stories
• Rejected: {N} (returned to backlog with gap description)
• Blockers: {N} (resolution: {summary})
• Release progress: R{N}: {X}/{Y} epics done

Reprioritization needed? {yes/no}
Continue to Value & Metrics (Stage 16), or end session?
```

---

## Transition

→ **Stage 16: Value & Metrics** (if extension active and user continues)
→ **Stage 14: Backlog Operations** (if reprioritization needed)
→ **Session end** (state persisted)

---

## The Exchange — What AI-POLC Sends to / Receives from AI-DLC v1

> **Critical constraint:** AI-DLC v1 is NOT our product. We do not integrate directly. We prepare the workspace so that any AI operating within it encounters our governance decisions as rules.

### Direct (via files AI-DLC v1's user points to)

| What | How | What DLC Does |
|------|-----|---------------|
| Prioritized Epics | Epic files ranked in `prioritization-register.md` | DLC Inception takes top epic, elaborates into stories |
| Priority Order | Ordering in register | DLC picks the top item when ready for new work |
| Reprioritization Signals | Updated register + `POLC-C-NNN` in spine | DLC stops deferred epic at bolt boundary, picks new top |

### Indirect (via AI-DWG workspace steering)

| Rule POLC Defines | How It Reaches DLC | DLC Behavior |
|---|---|---|
| DoR checklist | AI-DWG encodes into `DEFINITION_OF_DONE.md` | DLC self-checks stories against readiness bar |
| DoD checklist | AI-DWG encodes into `DEFINITION_OF_DONE.md` | DLC verifies bolt against product acceptance bar |
| AC format (Given/When/Then) | AI-DWG encodes into `testing-strategy.md` | DLC uses this format when writing AC |
| Refinement cadence | AI-DWG encodes into `session-governance.md` | DLC knows operational rhythm |

### What DLC Returns to POLC (user brings to POLC session)

| What | What POLC Does |
|------|----------------|
| Bolt completed (story done) | Updates traceability, checks increment completeness |
| Blocker encountered | Reprioritizes around it, escalates if needed |
| Velocity/throughput data | Adjusts release slicing |
| Runtime feedback (if instrumented) | Feeds into Value & Metrics extension |

---

*Detail file for AI-POLC Stage 15 | Phase: Operations*
