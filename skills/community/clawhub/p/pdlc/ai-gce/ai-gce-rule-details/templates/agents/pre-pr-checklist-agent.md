<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Pre-PR Checklist Agent — Template

## Purpose

A process agent that verifies PR readiness before creating a pull request. Checks governance, tests, naming, API contracts, segregation, and Definition of Done — producing a pass/warn/block report.

**Replaces:** `periodic-audit.json` hook (userTriggered) — per, process milestone checks are agents, not hooks.

---

## When to Invoke

- **Before creating any pull request** — verifies all quality gates are met
- **Shortcut:** `PRC__` (typed anywhere in a prompt)
- **Tier:** 2+ (Construction phase onward)
- **Consequence of skipping:** PR may fail review, compliance score drops, CODEOWNER review wasted on avoidable issues

---

## Recovery (If Skipped)

If a PR was created without running this check:
1. Run `PRC__` against the current branch state
2. If ❌ blockers found → fix before merge
3. If ⚠️ warnings only → address in follow-up commit or accept with justification
4. Log a `GOV-SKIP` event to compliance log

---

## Checks Performed (12)

### Step 1: Context Load
- Read `.compliance-state.json` → confirm tier ≥ 2 and phase ≥ Construction
- If tier < 2: respond "This agent activates at Tier 2 — your workspace is currently at Tier {current}."

### Step 2: Tests Pass
- Confirm all tests in affected modules pass
- Source: test runner output / `testing-strategy.md` test commands

### Step 3: Coverage Met
- Coverage meets threshold from `testing-strategy.md`
- Compare against configured minimum (default: 80%)

### Step 4: API Contract Aligned
- If endpoints were created/modified → verify they match the OpenAPI contract
- Source: `api-standards.md`, contract files

### Step 5: Naming Correct
- All new files follow `naming-conventions.md`
- Check: file names, class names, method names, folder placement

### Step 6: No Cross-Module Violations
- No direct imports across module boundaries
- Source: `module-structure.md` boundary rules

### Step 7: Commit Convention
- Commits follow the format from `git-workflow.md`
- Pattern: `{type}({scope}): {description}`

### Step 8: Branch Naming
- Branch follows the pattern from `git-workflow.md`
- Pattern: `{type}/{ticket-id}-{description}`

### Step 9: One Module Per Branch
- Commits only touch one module's files
- If multiple modules touched → warn (may indicate scope creep)

### Step 10: CODEOWNER Assigned
- The PR will be reviewed by the CODEOWNER (not the author)
- Source: `CODEOWNERS` file + `role-isolation.md` (author ≠ approver)

### Step 11: Security Review (Conditional)
- IF auth/security code was modified → flag for security role review
- IF financial calculations modified → flag for zero-trust review

### Step 12: Definition of Done
- All applicable DoD criteria checked
- Source: `DEFINITION_OF_DONE.md`

---

## Output

Report format:
```
## PR Readiness Report — {branch_name}

| # | Check | Result | Notes |
|---|-------|:------:|-------|
| 1 | Tests pass | ✅/⚠️/❌ | {details} |
| 2 | Coverage met | ✅/⚠️/❌ | {actual}% vs {threshold}% |
|... |... |... |... |

**Verdict:** {✅ Ready to PR / ⚠️ Proceed with caution / ❌ Fix before PR}
**Blockers:** {count}
**Warnings:** {count}
```

---

## Compliance Logging

After completing all checks, append to `compliance-log/events/{today-date}.jsonl`:

```json
{"timestamp": "{ISO-8601-UTC}", "type": "check", "id": "chk-{date}-{time}-{seq}", "agent": "pre-pr-checklist-agent", "trigger": "user/PRC__", "ruleId": "{primary-rule-checked}", "ruleSeverity": "{severity}", "result": "{pass|fail|warn}", "message": "{finding}"}
```

Log ONE event per check performed.

---

## Related

| Item | Location |
|------|----------|
| Agent Guide | `.governance/AGENT-GUIDE.md` |
| Agent Registry | `.governance/AGENT_REGISTRY.md` |
| Shortcut | `PRC__` |
| Git workflow rules | `rules/git-workflow.md` |
| Testing strategy | `rules/testing-strategy.md` |
| Naming conventions | `rules/naming-conventions.md` |

---

*Template Version: 1.0.0 | Replaces: pre-pr-checklist.json (userTriggered hook) | Per *
