# Proof Loop Workflow

## Phase 0: Spec Freeze

**Who:** Orchestrator (project lead, or whoever is briefing)

Before a single line of code is written:
1. Write `spec.md` with explicit acceptance criteria (AC1, AC2, AC3...)
2. Each AC must be testable by a third party who didn't build it
3. Include: constraints, non-goals, verification approach
4. Freeze the spec — ACs cannot change during build

**spec.md must include:**
- Original task statement
- Acceptance Criteria (AC1, AC2, ...)
- Constraints (what must not break)
- Non-goals (what is explicitly out of scope)
- Verification approach (how each AC will be checked)

---

## Phase 1: Build

**Who:** Builder agent (fresh session)

- Reads spec.md — implements against frozen ACs only
- Makes the smallest safe change set that satisfies all ACs
- Does not verify own work
- Hands off to evidence phase when implementation is complete

---

## Phase 2: Evidence

**Who:** Builder (same session, switched to evidence mode) or a fresh evidence agent

- Does not change production code
- Runs checks and records results
- Writes `evidence.md` (prose) and updates `verdict.json` (structured)
- Verdict per AC: PASS / FAIL / UNKNOWN
- If FAIL or UNKNOWN: writes `problems.md` with specific file/line references

**Builder hard constraints in evidence mode:**
- Must not patch evidence to make it look better
- Must not change production code
- UNKNOWN is valid — it means "could not verify"

---

## Phase 3: Fresh Verify

**Who:** Verifier — always a NEW session, never the same agent that built

- Reads `spec.md`, `verdict.json`, `problems.md`
- Runs independent checks against the current codebase
- Updates `verdict.json` with verifier's findings
- Updates `problems.md` if issues found
- **Must not edit production code**
- **Must not sign off on completion**

---

## Phase 4: Fix (if needed)

**Who:** Fixer — fresh session

- Reads `spec.md` + `verdict.json` + `problems.md`
- Reconfirms each problem before editing
- Applies minimal fix — only what the verifier identified
- Regenerates evidence
- **Does not write final sign-off** — goes back to Phase 3

---

## The Fix Loop

```
fix -> fresh verify -> fix -> fresh verify
```

Continues until verifier writes PASS for every AC.

A single successful PASS does not end the loop — ALL ACs must be PASS.

---

## Done Criteria

A task is complete when:
- Every AC in `spec.md` has status PASS in `verdict.json`
- `problems.md` is empty or does not exist
- Any regression suite required by the spec passes

---

## Common Failure Modes (and how this prevents them)

| Failure | Prevention |
|---------|-----------|
| Agent claims done without checking | Verifier is separate, required |
| ACs drift during build | Spec is frozen before build starts |
| Later sessions can't tell what was verified | Verdict artifacts stay in repo |
| Builder judges own work | Fresh verifier is a hard rule |
| Fix introduces new regression | Verifier reruns after every fix |
