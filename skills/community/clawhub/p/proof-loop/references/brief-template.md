# Agent Brief Template

Use this template when briefing any coding agent on a non-trivial task.

---

## Sprint/Task Brief: [TASK_ID]

### Task Statement
[One paragraph describing what needs to be built and why]

### Acceptance Criteria

```
AC1: [specific, testable condition]
     Verify: [how to check this — command, visual check, API call]

AC2: [specific, testable condition]
     Verify: [how to check this]

AC3: [specific, testable condition]
     Verify: [how to check this]
```

**Good AC examples:**
- "AC1: A user with locale=de sees all navigation labels in German after saving language preference"
- "AC2: POST /api/v1/prompts/translate/de returns 200 with translated titles for all 50 prompts"
- "AC3: `pnpm test:e2e` passes all sprint spec files with no failures"

**Bad AC examples:**
- "AC1: Translate the UI" (not testable)
- "AC1: Make it work in German" (vague)
- "AC1: Fix the translation bugs" (not specific)

### Constraints
[What must not break — existing features, performance, API contracts]

### Non-Goals
[What is explicitly OUT of scope for this task]

### Verification Approach
[How each AC will be verified — automated tests, manual browser check, API call, etc.]

---

## Brief Checklist (orchestrator — run before firing agents)

- [ ] ACs are explicit, testable, and frozen
- [ ] Each AC has a verification approach
- [ ] Constraints are listed
- [ ] Non-goals are listed
- [ ] Builder role is clear (who builds)
- [ ] Verifier role is clear (different agent, fresh session)
- [ ] Fixer role is clear (if needed)
- [ ] Artifact path is set: `.agent/tasks/[TASK_ID]/`

---

## Prompts by Role

### Spec-Freezer prompt
```
You are the spec freezer for task [TASK_ID].

Read the brief above. Write spec.md to .agent/tasks/[TASK_ID]/spec.md with:
- Original task statement
- Acceptance Criteria (AC1, AC2, AC3...) — copy from brief, do not modify
- Constraints
- Non-goals
- Verification approach per AC

Do not edit any production code. Do not start building.
```

### Builder prompt
```
You are the builder for task [TASK_ID].

Read .agent/tasks/[TASK_ID]/spec.md. Implement the task against the frozen ACs.
Make the smallest safe change set that satisfies all ACs.
Do not verify your own work. When done, hand off to the evidence phase.
```

### Verifier prompt
```
You are the verifier for task [TASK_ID]. This is a fresh session.

Read:
- .agent/tasks/[TASK_ID]/spec.md (the frozen ACs)
- .agent/tasks/[TASK_ID]/verdict.json (current verdicts)
- .agent/tasks/[TASK_ID]/problems.md (known problems)

Run independent checks. For each AC, write your verdict: PASS / FAIL / UNKNOWN.
Update verdict.json. If any AC is not PASS, update problems.md with specific file/line references.

Do not edit production code. Do not sign off on completion.
```

### Fixer prompt
```
You are the fixer for task [TASK_ID].

Read:
- .agent/tasks/[TASK_ID]/spec.md
- .agent/tasks/[TASK_ID]/verdict.json
- .agent/tasks/[TASK_ID]/problems.md

Fix only what the verifier identified. Apply the minimal diff. Regenerate evidence.
Do not write final sign-off. A fresh verifier will re-run after your fix.
```
