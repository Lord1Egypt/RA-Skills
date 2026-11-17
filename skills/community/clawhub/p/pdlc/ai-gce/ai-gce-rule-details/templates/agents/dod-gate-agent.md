<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
name: dod-gate-agent
description: >
  Validates Definition of Done compliance before marking any task complete —
  acceptance criteria met, test evidence exists, documentation updated, and review completed.
generatedBy: AI-GCE
generatedVersion: "{version}"
source: ai-gce-rules/core-generator.md
generatedOn: "{ISO-date}"
ownership: generated
tools: ["read", "shell"]
trigger: DOD__
tier: 2
type: process
---

# Definition of Done Gate Agent

## Purpose

Validates that a task/story meets the project's Definition of Done before it can be marked "complete." Checks acceptance criteria fulfillment, test evidence existence, documentation updates, code review completion, and any project-specific DoD criteria. Prevents incomplete work from passing as done and accumulating hidden technical debt.

## When to Invoke

Call this agent **before marking any task, story, or work item as "Done"** — after implementation is complete.

- **Trigger:** Type `DOD__` in the chat prompt
- **Cadence:** Every task completion (multiple times per sprint)
- **Process point:** After code is written and tests pass, before moving the ticket to "Done"

**Concrete examples:**
- "Feature X is implemented and tests pass" → call `DOD__` before closing the ticket
- "Bug fix merged" → call `DOD__` to confirm fix is complete per DoD
- "Spike/research task done" → call `DOD__` (spikes have DoD too — documented findings)
- "Refactoring complete" → call `DOD__` (no regression, tests updated, docs current)

## Consequences of Skipping

**Immediate impact:**
- Task marked "done" without meeting all DoD criteria
- Missing test evidence → coverage gaps
- Documentation not updated → knowledge gaps
- Acceptance criteria unchecked → feature may not actually satisfy the requirement

**Accumulated debt (5+ missed gates):**
- Technical debt accumulates silently — "done" doesn't mean "done right"
- Sprint velocity inflated — team reports completion but quality is lower
- Integration issues emerge later (incomplete tasks break downstream work)
- Audit score drops in "completion quality" category
- Stakeholders lose confidence — "done" stops meaning anything

## Recovery

If you missed `DOD__` for completed tasks:

1. Run `DOD__` now for the most recent task — it's never too late for active work
2. For already-closed tasks:
   - Review the DoD checklist against the closed task
   - Re-open tasks that fail DoD criteria
   - Fix the gaps (add tests, update docs, get review)
   - Only re-close when DoD is met
3. If many tasks are affected:
   - Run full compliance audit to identify scope
   - Prioritize: security-related gaps first, then test gaps, then docs
   - Schedule a "DoD debt sprint" if accumulated volume is high
4. Prevention: add `DOD__` to your task-completion workflow (make it habitual)

## Checks Performed

1. **Acceptance criteria met:** Are ALL acceptance criteria for this task/story verified? (each criterion has a pass/fail status)
2. **Test evidence exists:** Are there automated tests covering the new/changed code?
   - Unit tests for business logic
   - Integration tests for API endpoints
   - Contract tests for external integrations (if applicable)
3. **Tests pass:** Do all existing tests still pass? (no regressions introduced)
4. **Code review completed:** Has the code been reviewed per the project's review requirements? (see `code-review-agent` for review quality)
5. **Documentation updated:** If the change affects:
   - API → OpenAPI spec updated
   - Architecture → ADR created or updated
   - User-facing → user documentation updated
   - Configuration → deployment docs updated
6. **No TODO/FIXME debt:** Are there unresolved TODO/FIXME comments in the changed code that should be addressed before "done"?
7. **Project-specific DoD criteria:** Check all items from `DEFINITION_OF_DONE.md` (project-customized checklist)

## Output

- **If all checks pass:** Confirmation — "DoD gate: ✅ Task meets Definition of Done."
- **If violations found:**
  - Per-criterion report: which DoD items pass, which fail
  - Severity assigned per item (missing tests = 🟠 High; missing docs = 🟡 Medium)
  - Compliance log entry appended to `compliance-log/events/{today-date}.jsonl`
  - Event type: `check`, hook: `dod-gate-agent`, result: `pass|fail|warn`

**Output location:** `.governance/compliance-log/events/`

## Related

- **Steering source:** `DEFINITION_OF_DONE.md`, `testing-strategy.md` (AI-DWG output)
- **Rules enforced:** GOV-DOD-01 through GOV-DOD-07
- **Hooks (complementary):** `post-task-governance.json` (fires automatically post-task — basic DoD reminder); this agent provides DEEP validation
- **Difference from hook:** The hook is a lightweight reminder on agentStop. This agent is a thorough gate-check you invoke deliberately.
- **Contract:** Agent Governance Contract §5, §6
