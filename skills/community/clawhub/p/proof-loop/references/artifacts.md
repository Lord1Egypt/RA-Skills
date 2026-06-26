# Artifact Schemas

All artifacts live in the repository under `.agent/tasks/<TASK_ID>/`.

---

## spec.md

Plain Markdown. Written by Spec-Freezer before build starts. Never modified after freeze.

```markdown
# Task: [TASK_ID]

## Task Statement
[Original task description]

## Acceptance Criteria

**AC1:** [testable condition]
- Verify: [how to check]

**AC2:** [testable condition]
- Verify: [how to check]

## Constraints
- [what must not break]

## Non-Goals
- [what is out of scope]

## Verification Approach
[Overall approach to verifying this task]
```

---

## verdict.json

Written by Verifier. Updated after each fix loop iteration.

```json
{
  "task_id": "sprint-4c",
  "phase": "verify",
  "agent": "verifier",
  "timestamp": "2026-03-30T14:00:00Z",
  "overall": "FAIL",
  "criteria": [
    {
      "id": "AC1",
      "status": "PASS",
      "note": "All nav labels confirmed German in browser test"
    },
    {
      "id": "AC2",
      "status": "FAIL",
      "note": "Form field labels still in English — formSchemaTranslated is null in DB"
    },
    {
      "id": "AC3",
      "status": "PASS",
      "note": "pnpm test:e2e — all sprint 1-4c specs green"
    }
  ]
}
```

**overall** is PASS only when every AC status is PASS.
**status values:** PASS | FAIL | UNKNOWN

---

## problems.md

Written by Verifier when overall is not PASS. Specific, actionable.

```markdown
# Problems — [TASK_ID]

## AC2: Form field labels in English

**File:** `packages/llm/src/translation.ts`
**Function:** `translatePrompts()`
**Issue:** All prompt chunks translated in parallel via `Promise.all()`. Under slow local
models, all calls time out simultaneously and fall back to English silently.
**Evidence:** DB query shows `formSchemaTranslated IS NULL` for all 50 rows.
**Fix needed:** Change parallel chunk processing to sequential — one prompt at a time.
```

---

## evidence.md (optional)

Prose summary written by Builder in evidence mode. Supplements verdict.json.

```markdown
# Evidence — [TASK_ID]

## Build Summary
[What was changed and why]

## AC1 — PASS
[How it was verified, what was checked]

## AC2 — FAIL
[What was attempted, what failed, why]
```
