# Execution Discipline

> **The Build → Test → Document → Decide cycle for reliable autonomous operations**
> Priority: CRITICAL | Category: Core Workflow

## Overview

Autonomous agents fail when they treat tasks as one-shot attempts. This skill enforces a disciplined execution loop that ensures validation, documentation, and iterative improvement.

## The Execution Loop

```
┌─────────────────────────────────────────────────────────────┐
│                     EXECUTION CYCLE                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   BUILD ──→ TEST ──→ DOCUMENT ──→ DECIDE ──→ (repeat)       │
│     │          │           │            │                   │
│     │          │           │            └─→ ITERATE        │
│     │          │           │                UPGRADE        │
│     │          │           │                CLOSE          │
│     │          │           │                              │
│     │          │           └─→ progress-log.md            │
│     │          │                                        │
│     │          └─→ Validation Results                   │
│     │                                                 │
│     └─→ Minimal Meaningful Change                    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## Phase 1: BUILD

### Principles
- **Smallest meaningful change only**
- **No speculative additions**
- **No refactoring alongside feature work**
- **Testable units only**

### Rules
```yaml
build_rules:
  - scope: "One logical unit per change"
  - size: "Smallest that validates the approach"
  - dependencies: "Handle one at a time"
  - testing: "Must be immediately testable"
  - documentation: "Update docs before, not after"

prohibitions:
  - "Don't add 'nice-to-have' extras"
  - "Don't refactor alongside features"
  - "Don't batch multiple logical changes"
  - "Don't skip to next phase without completing build"
```

### Build Checklist
- [ ] Change is scoped to single logical unit
- [ ] Change is testable immediately
- [ ] Dependencies are identified and documented
- [ ] Success criteria are defined
- [ ] Rollback plan exists

### Example

#### ❌ Bad Build
```
"Add user authentication, update the UI, refactor the database,
add email notifications, and write tests"
```

#### ✅ Good Build
```
"Add user authentication API endpoint that accepts username/password
and returns a JWT token. Success: endpoint returns 200 with valid token.
Rollback: revert auth/ directory."
```

## Phase 2: TEST

### Principles
- **Test against expected behavior, not hopes**
- **Automated tests when possible**
- **Manual testing documented**
- **Failure is valuable information**

### Test Categories

#### 1. Unit Tests
```bash
# Run for isolated functionality
pytest tests/unit/test_feature.py
```

#### 2. Integration Tests
```bash
# Run for component interactions
pytest tests/integration/test_feature_integration.py
```

#### 3. Manual Verification
```yaml
manual_test:
  given: "Preconditions and setup"
  when: "Action taken"
  then: "Expected observable result"
  evidence: "Screenshot, log output, or measurement"
```

### Test Documentation

Always record test results in `progress-log.md`:

```markdown
## Test Result: [Feature Name]

**Date**: 2026-03-10 14:30
**Build**: JWT authentication endpoint
**Tester**: OpenClaw Agent

### Tests Run

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| Valid login | 200 + token | 200 + token | ✅ PASS |
| Invalid password | 401 | 401 | ✅ PASS |
| Missing fields | 400 | 500 | ❌ FAIL |
| SQL injection safe | No error | Crashed | ❌ FAIL |

### Evidence
```
[Log output or screenshot]
```

### Decision: Needs iteration - error handling broken
```

## Phase 3: DOCUMENT

### What to Document

Every cycle must update:

1. **progress-log.md**
   ```markdown
   ## Cycle: [Feature] - [Date]

   **Build**: [What was changed]
   **Test**: [Tests performed]
   **Result**: [Pass/Fail]
   **Learned**: [What was discovered]
   **Next**: [What happens next]
   ```

2. **Code Documentation** (if applicable)
   - Update function docstrings
   - Update API documentation
   - Update architecture diagrams

3. **lessons.md** (if failure occurred)
   ```markdown
   ## [Date]: [Failure Summary]

   **Problem**: [What went wrong]
   **Root Cause**: [Why it happened]
   **Prevention**: [How to avoid recurrence]
   ```

### Documentation Template

```markdown
# Execution Log: [Feature Name]

## Metadata
- **Date**: YYYY-MM-DD HH:MM
- **Agent**: [Agent Name]
- **Model**: [Model Used]
- **Cycle**: [N of M]

## Build Phase
- **Scope**: [Single logical unit]
- **Files Changed**: [List]
- **Success Criteria**: [Defined criteria]

## Test Phase
| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| [Test 1] | [Expected] | [Actual] | [Pass/Fail] |
| [Test 2] | [Expected] | [Actual] | [Pass/Fail] |

## Decision
- **Outcome**: [PASS/FAIL/NEEDS_ITERATION]
- **Reasoning**: [Why this decision]
- **Next Action**: [What happens in next cycle]

## Evidence
[Logs, screenshots, measurements]
```

## Phase 4: DECIDE

### Decision Options

#### 1. ITERATE
**When**: Tests failed but approach is sound
**Action**: Fix the issue, run test cycle again
**Limit**: Maximum 3 iterations before re-planning

```yaml
iterate:
  condition: "Tests failed but approach valid"
  action: "Fix and retest"
  max_attempts: 3
  after_max: "Re-plan from scratch"
```

#### 2. ESCALATE
**When**: Blocked by external factors or missing context
**Action**: Pause execution, notify user, wait for input

```yaml
escalate_triggers:
  - "Missing credentials or access"
  - "External service failure"
  - "Requirements ambiguity"
  - "Third iteration on same issue"
  - "Security concern identified"

escalate_message: |
  ESCALATION REQUIRED: [Brief summary]

  What I was doing: [Task description]
  What happened: [Issue description]
  What I need: [Specific requirement]
  Context: [Relevant logs/evidence]
```

#### 3. CLOSE
**When**: All tests pass, success criteria met
**Action**: Mark complete, update Todo.md, summarize

```yaml
close:
  condition: "All tests pass, success criteria met"
  requirements:
    - "All defined tests pass"
    - "No regressions introduced"
    - "Documentation updated"
    - "Progress logged"
  actions:
    - "Mark task complete in Todo.md"
    - "Write completion summary"
    - "Update any affected documentation"
```

#### 4. RE-PLAN
**When**: Approach is fundamentally flawed
**Action**: Stop execution, analyze failure, create new plan

```yaml
re_plan:
  condition: "Three iterations failed OR approach invalid"
  actions:
    - "Stop current implementation"
    - "Analyze root cause"
    - "Research alternatives"
    - "Create new plan"
    - "Get approval before proceeding"
```

## Anti-Patterns to Avoid

### ❌ The "One-Shot" Fallacy
```yaml
pattern: "Make all changes at once, test at end"
problem: "Impossible to debug, massive rollback"
fix: "Break into smallest testable units"
```

### ❌ The "Hope-Based" Test
```yaml
pattern: "Test that 'it works' without specific criteria"
problem: "Subjective, unrepeatable"
fix: "Define specific, observable success criteria"
```

### ❌ The "Silent" Failure
```yaml
pattern: "Tests fail but proceed anyway"
problem: "Compounds errors, creates technical debt"
fix: "Never proceed without test validation"
```

### ❌ The "Memory-less" Cycle
```yaml
pattern: "Don't document lessons learned"
problem: "Repeat same mistakes"
fix: "Always update lessons.md on failure"
```

## Execution Example

### Task: Add user authentication

#### Cycle 1
```
BUILD: Add login endpoint with JWT return
TEST: Valid login works ✅ | Invalid login fails ❌ (returns 500 not 401)
DECISION: ITERATE - Error handling needs work
```

#### Cycle 2
```
BUILD: Fix error handling for invalid credentials
TEST: Invalid login returns 401 ✅ | SQL injection crashes ❌
DECISION: ITERATE - Security issue
```

#### Cycle 3
```
BUILD: Add input sanitization
TEST: SQL injection handled ✅ | All tests pass ✅
DECISION: CLOSE - Ready for deployment
```

## Verification Checklist

After enabling this skill, your agent should:

- [ ] Never make changes without testing
- [ ] Always document test results
- [ ] Never proceed after test failure without explicit decision
- [ ] Always update progress-log.md
- [ ] Never iterate more than 3 times on same issue
- [ ] Always escalate when blocked

## Key Metrics

Track these to verify compliance:

```bash
# Average cycles per task (target: 2-3)
openclaw metrics cycles-per-task

# Test pass rate (target: >80%)
openclaw metrics test-pass-rate

# Documentation coverage (target: 100%)
openclaw metrics docs-coverage

# Escalation rate (target: <20%)
openclaw metrics escalation-rate
```

## Key Takeaway

**Reliable autonomous operations require disciplined iteration.** One perfect attempt is rare; three documented iterations with learning are valuable.

---

**Next Skills**: Combine with `docs-first.md` for research-before-build discipline.
