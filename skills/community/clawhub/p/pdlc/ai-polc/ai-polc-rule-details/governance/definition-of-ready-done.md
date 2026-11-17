<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 8: Definition of Ready / Done

**Phase:** Governance
**Purpose:** Set the quality bar for entering development (DoR) and for accepting completed work (DoD) — the contract between PO and development team that prevents rework and scope drift.

---

## Purpose

The DoR/DoD are the governance rules that flow downstream: AI-DWG encodes them into `DEFINITION_OF_DONE.md` and `session-governance.md`; AI-GCE enforces them via hooks. Without them, developers start work on half-specified items (waste) or ship features that technically work but don't solve the user's problem (rework).

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | 3-5 items per checklist. Essential quality bar only. |
| **Standard** | 6-8 items per checklist. Context-adapted. Review cadence defined. |
| **Comprehensive** | 8-12 items per checklist. Exception process. Compliance items. Governance for changing DoR/DoD itself. |

---

## Steps

### Step 8.1: Build Definition of Ready (DoR)

DoR answers: "What must be true about a backlog item BEFORE development begins?"

**Universal items (apply to any project):**
- [ ] Clear description of WHAT (not how) is expected
- [ ] Acceptance criteria defined and testable
- [ ] Goal/epic linkage documented
- [ ] No unresolved dependencies blocking implementation
- [ ] Size estimated (story points or T-shirt)

**Context-adapted additions:**

| Context Factor | Additional DoR Items |
|---|---|
| Architecture = DDD | Bounded context identified; aggregate boundaries clear |
| Architecture = Microservices | Service ownership assigned; API contract defined |
| Compliance = Heavy | Compliance requirements listed; audit trail requirements stated |
| Scale = Multi-team | Cross-team dependencies identified and resolved |
| Data-Driven = High | Success metric defined; measurement instrumentation specified |

### Step 8.2: Build Definition of Done (DoD)

DoD answers: "What must be true about a completed increment BEFORE it ships?"

**Universal items (apply to any project):**
- [ ] Code complete and peer-reviewed
- [ ] All acceptance criteria verified (pass/fail demonstrated)
- [ ] Tests written and passing (unit + integration as applicable)
- [ ] No P1/P2 bugs open in scope
- [ ] Documentation updated (if applicable)
- [ ] PO has reviewed and accepted

**Context-adapted additions:**

| Context Factor | Additional DoD Items |
|---|---|
| Compliance = Heavy | Compliance sign-off obtained; audit log entries verified |
| Architecture = Microservices | Contract tests passing; service health check verified |
| Release Strategy = Continuous | Feature flag configured; rollback tested |
| Data-Driven = High | Analytics instrumented; baseline measurement captured |
| Security (from AP) | Security review completed; no new vulnerabilities introduced |

### Step 8.3: Define Exception Process

Not every item will cleanly meet DoR/DoD. Define the exception path:

```
Exception Process:
1. Item fails DoR/DoD check → flagged by team or AI-GCE hook
2. PO assesses: Is the gap acceptable given context?
   - YES → Record exception with rationale (POLC-D-NNN)
   - NO  → Item returns to backlog / blocked until resolved
3. Exception is time-bounded: "Accepted for this sprint; must be resolved by next"
4. Exception count tracked — pattern of exceptions = DoR/DoD needs updating
```

### Step 8.4: Define Review Cadence

DoR/DoD are living documents, not set-and-forget:

| Review Trigger | Action |
|---|---|
| End of each release | Retrospective: "Did DoR/DoD catch quality issues? Did they prevent rework?" |
| Pattern of exceptions (>3 in one sprint) | DoR/DoD may be too strict or too vague — revise |
| Architecture change (AP update) | Re-derive context-adapted items |
| Team feedback ("this check is wasteful") | Evaluate and remove/modify if justified |
| New compliance requirement | Add to DoD immediately |

### Step 8.5: Downstream Encoding Notes

Document how DoR/DoD reach the development workflow:

```
AI-DWG encodes:
├── DoR items → DEFINITION_OF_DONE.md "Readiness" section
├── DoD items → DEFINITION_OF_DONE.md "Done" section
└── Review cadence → session-governance.md "Quality review cadence"

AI-GCE enforces:
├── pre-sprint-readiness-check hook → validates items against DoR
├── pre-release-dod-check hook → validates increment against DoD
└── acceptance-criteria-format-check → validates AC format consistency
```

This is a documentation note for the user — AI-POLC doesn't control DWG/GCE directly.

### Step 8.6: Persist DoR/DoD

Write two files:

**`definition-of-ready.md`:**
- Universal items
- Context-adapted items (with which context factor triggered each)
- Exception process
- Review cadence
- Version number

**`definition-of-done.md`:**
- Universal items
- Context-adapted items
- Exception process
- Review cadence
- Version number

---

## Gate

**Gate 8 — DoR/DoD Confirmed:**

Present to user:
```
Quality bar established:
• Definition of Ready: {N} items
• Definition of Done: {N} items
• Exception process: defined
• Review cadence: {description}

These rules will flow into the development workspace via AI-DWG.
Does this quality bar match your product's needs?
Approve to proceed to Product Risk & Assumptions.
```

User must confirm before proceeding.

---

## Governance Spine Entry

Log in Decision Log:
```
POLC-D-007: DoR ({N} items) and DoD ({N} items) established.
Review cadence: {summary}. Exception process defined.
DoR version: 1.0. DoD version: 1.0.
```

Log in Change Log (for version tracking):
```
POLC-C-001: DoR v1.0 and DoD v1.0 baseline established.
Context-adapted for: {list of triggering context factors}.
```

---

## Transition

→ **Stage 9: Product Risk & Assumptions** (Governance continues)

---

*Detail file for AI-POLC Stage 8 | Phase: Governance*
