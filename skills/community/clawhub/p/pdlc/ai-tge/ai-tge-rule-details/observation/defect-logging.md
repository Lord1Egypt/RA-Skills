<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Defect Logging

## Stage: 11 of 12
## Phase: 🟢 OBSERVATION
## Execution: CONDITIONAL — when defects are reported

---

## Purpose

Capture and structure defect information when the user reports a bug, a test failure is detected, or a quality issue surfaces during development. Each defect is logged with severity, category, linked component, linked test (if applicable), and root cause (when determined). The defect log provides audit trail and feeds into debt reassessment.

AI-TGE does NOT find defects — it structures and governs defect TRACKING when defects are reported to it.

---

## Conditional Trigger

| Execute IF | Skip IF |
|-----------|---------|
| User reports a defect: "I found a bug in..." | No defects reported this session |
| Test failure detected during observation (Status = Failing) | All tests passing |
| User explicitly requests "log defect" or "record a bug" | Defect already logged (don't duplicate) |
| CI/CD reports test failures (if observable) | User says "ignore this failure" |

**If skipped:** No action needed — this stage activates on-demand only. No log entry for skipping.

---

## Depth Adaptation

| Depth | Logging Detail | Analysis |
|-------|---------------|----------|
| **Minimal** | Core fields only: ID, severity, category, description, component, status. No root cause analysis. No linked test requirement. | Simple tracking |
| **Standard** | Full fields: + linked test, linked story, root cause (when known), linked register entry. Severity assessment with impact justification. | Structured tracking with traceability |
| **Comprehensive** | All Standard fields + timeline (detection → investigation → fix → verification), regression prevention note, test register gap analysis (did missing test allow this defect?), pattern detection across defects. | Full lifecycle tracking + governance learning |

---

## MANDATORY: Stage Sub-Role — Audit Specialist

During THIS stage, ALSO adopt the mindset of an **Audit Specialist**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Record facts precisely: what broke, where, when, how it was discovered
- Link to governance: was there a register entry that should have caught this? If so, the register needs updating. If not, a new requirement may be needed.
- Classify consistently: use the same severity and category definitions every time
- Think preventively: every defect is a lesson — what test would have caught this earlier?

### Anti-Patterns for This Stage
- Do NOT assess blame — log WHAT happened, not WHO caused it
- Do NOT skip severity assessment — every defect needs a priority level
- Do NOT create a new test register entry automatically for every defect — that's a separate decision (propose, don't auto-add)
- Do NOT close a defect until it's verified fixed (Status progression matters)

### Quality Check
A good output at this stage sounds like:
- "DEF-003: High/Security — JWT token refresh endpoint returns 200 with expired refresh token (should return 401). Component: AuthService. Linked register entry: SEC-001 (test exists but doesn't cover refresh flow — gap in test assertion scope). Root cause: refresh token expiry check missing from middleware. Regression prevention: expand SEC-001 test to cover refresh token path."

---

## Step-by-Step Execution

### Step 1: Capture Defect Information

Gather defect details from user report:

| Field | Required | Source |
|-------|:--------:|--------|
| Description | ✅ | User provides (what's wrong) |
| Where discovered | ✅ | User provides (which component/endpoint/flow) |
| How discovered | ✅ | Testing / manual use / CI / user report |
| Expected behavior | ✅ | What SHOULD happen |
| Actual behavior | ✅ | What ACTUALLY happens |
| Reproducibility | For Standard+ | Always / intermittent / one-time |
| Environment | For Standard+ | Local / staging / production |

**If user report is vague**, ask structured questions:
```markdown
To log this defect properly, I need:
1. **What component/feature is affected?** (e.g., "user registration", "payment processing")
2. **What did you expect to happen?**
3. **What actually happened?**
4. **How was it discovered?** (during testing / manual exploration / user report / CI failure)
```

---

### Step 2: Assign Defect ID

Sequential: `DEF-{NNN}` (check existing defect log for next number)

If no defect log exists yet, start at DEF-001.

---

### Step 3: Assess Severity

| Severity | Definition | Impact |
|:--------:|-----------|--------|
| **Critical** | System unusable; data loss or corruption; security breach; complete feature broken | Blocks release; immediate fix required |
| **High** | Major feature broken; no workaround; significant user impact | Fix before next release; may block sprint completion |
| **Medium** | Feature partially broken; workaround exists; moderate user impact | Fix within next 2 sprints |
| **Low** | Cosmetic; minor inconvenience; edge case; workaround trivial | Fix when convenient; backlog |

**Assessment criteria:**
- How many users are affected? (all → Critical/High; subset → Medium; edge case → Low)
- Is there a workaround? (none → +1 severity; exists → -1 severity)
- Is data at risk? (yes → minimum High)
- Is security at risk? (yes → minimum High, likely Critical)

---

### Step 4: Assign Category

| Category | What It Covers |
|----------|---------------|
| **Functional** | Feature doesn't work correctly; wrong behavior; logic error |
| **Performance** | Slow response; timeout; resource exhaustion |
| **Security** | Auth bypass; data exposure; injection vulnerability |
| **Data** | Corruption; inconsistency; loss; wrong data returned |
| **Integration** | External system communication failure; wrong data exchange |
| **UI/UX** | Display issue; accessibility failure; confusing interface |
| **Configuration** | Bad config causes failure; env-specific issue |
| **Infrastructure** | Deployment failure; environment issue; connectivity |

---

### Step 5: Link to Register and Architecture

Connect the defect to test governance:

| Link Type | How to Find | Significance |
|-----------|------------|-------------|
| **Linked Component** | Which AP component does this defect affect? | Identifies blast radius |
| **Linked Test** | Which test caught it (if any)? | If none → missed by testing |
| **Linked Register Entry** | Is there a register entry that SHOULD have caught this? | If yes → entry needs stronger assertions. If no → new entry may be needed. |
| **Linked Story** | Which user story does this defect violate? | Traces to business impact |

**Governance insight (Standard+ depth):**
```markdown
### Governance Analysis
- **Was this defect coverable?** {Yes — register entry exists / No — gap in register}
- **If coverable, why was it missed?** {Test doesn't cover this path / Test exists but insufficient assertion / Test not yet written (Missing status)}
- **Proposed register action:** {Expand existing entry / Add new entry / No change needed}
```

---

### Step 6: Compile Defect Entry

```markdown
## DEF-{NNN}

| Field | Value |
|-------|-------|
| **ID** | DEF-{NNN} |
| **Severity** | {Critical / High / Medium / Low} |
| **Category** | {Functional / Performance / Security / Data / Integration / UI-UX / Configuration / Infrastructure} |
| **Description** | {Clear description of what's wrong} |
| **Expected** | {What should happen} |
| **Actual** | {What actually happens} |
| **Component** | {Architectural component affected} |
| **Discovered By** | {Testing / Manual / CI / User report} |
| **Linked Test** | {Test that caught it, OR "None — discovered outside testing"} |
| **Linked Register Entry** | {Entry ID, OR "None — gap in register"} |
| **Linked Story** | {Story ID, OR "N/A"} |
| **Root Cause** | {When determined: brief technical cause. Until then: "_[Investigating]_"} |
| **Status** | {Open / Investigating / Fixed / Verified / Closed} |
| **Opened** | {ISO timestamp} |
| **Last Updated** | {ISO timestamp} |

### Regression Prevention (Standard+ depth)
{What test should be added or expanded to prevent recurrence?}
```

---

### Step 7: Update Defect Log

Append entry to `.governance/test/defect-log.md`:

```markdown
# Defect Log

**Type:** Defect Log
**Generated:** {initial creation date}
**Engine:** AI-TGE v1.0.0
**Last Updated:** {ISO timestamp}

## Summary

| Severity | Open | Fixed | Verified | Closed | Total |
|----------|:----:|:-----:|:--------:|:------:|:-----:|
| Critical | {n} | {n} | {n} | {n} | {n} |
| High | {n} | {n} | {n} | {n} | {n} |
| Medium | {n} | {n} | {n} | {n} | {n} |
| Low | {n} | {n} | {n} | {n} | {n} |

## Active Defects (Open + Investigating)

{Table of active defects — most recent first}

## Resolved Defects

{Table of Fixed/Verified/Closed — collapsed or summarized}
```

---

### Step 8: Propose Register Updates (If Applicable)

If the defect reveals a governance gap:

```markdown
## Register Update Proposal

Based on DEF-{NNN}, I recommend:

{Option A: Existing entry needs stronger assertions}
- Entry {ID}: Add assertion for {specific path/condition} that this defect exposed

{Option B: New entry needed}
- Proposed: {New test requirement} covering {the gap this defect revealed}
- Level: {level} | Type: {type} | Source: Manual (defect-driven)

{Option C: No register change needed}
- Existing entry {ID} covers this — the test just wasn't written yet (Status: Missing)
- Priority may need adjustment (defect confirms real risk)

Would you like me to update the register?
```

---

### Step 9: Confirm and Report

```markdown
## 🟢 Defect Logged: DEF-{NNN}

**Severity:** {severity} | **Category:** {category}
**Component:** {component}
**Summary:** {one-line description}

{IF register gap found:}
⚠️ This defect was not coverable by current register entries — register update proposed.

{IF existing test should have caught it:}
⚠️ Entry {ID} exists but its assertions don't cover this path — expansion recommended.

**Defect log saved to:** `.governance/test/defect-log.md`
```

**No gate.** Defect logging is continuous — log and inform. Register update proposals are presented but don't block.

---

## Status Lifecycle

```
Open → Investigating → Fixed → Verified → Closed
                 ↓                    ↓
            (Won't Fix)          (Reopened → Open)
```

| Status | Meaning | Who Transitions |
|--------|---------|----------------|
| **Open** | Defect reported, not yet investigated | Auto on creation |
| **Investigating** | Someone is looking into root cause | Developer/QA |
| **Fixed** | Code fix applied, not yet verified | Developer |
| **Verified** | Fix confirmed working; no regression | QA (tester) |
| **Closed** | Defect fully resolved; regression prevention in place | QA/PM |
| **Won't Fix** | Accepted risk; documented rationale | PM/Architect decision |
| **Reopened** | Fix didn't work; defect recurred | QA on verification failure |

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Defect Log | `.governance/test/defect-log.md` | Structured defect tracking (append-only) |
| Register update (if approved) | `.governance/test/test-register.md` | New entry or expanded assertion |
| Updated state file | `.governance/test/tge-state.md` | Defect count updated |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| Defect ID unique | Sequential, no gaps, no duplicates |
| Severity assessed | One of: Critical / High / Medium / Low |
| Category assigned | Valid category from the defined list |
| Component linked | Architectural component identified |
| Status valid | One of the lifecycle states |
| Governance connection made | Register entry linked (existing or gap noted) |
| Root cause tracked | Present OR marked "_[Investigating]_" |
| Defect log updated | Entry appended to `.governance/test/defect-log.md` |
| Non-blocking | No gate — log and inform |
