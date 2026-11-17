<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Brownfield Assessment

## Stage: 4 of 12
## Phase: 🔵 STRATEGY
## Execution: CONDITIONAL — if existing tests detected

---

## Purpose

Scan existing test directories, map found tests to register entries, and classify every register entry as Covered (matching test exists), Uncovered (no matching test), or Orphaned (test exists but no matching commitment). Produce a **Brownfield Gap Map** that shows the team exactly where they stand.

This stage is first-class — existing projects with existing tests get proper assessment, not dismissal.

---

## Conditional Trigger

| Execute IF | Skip IF |
|-----------|---------|
| Existing test directories detected in Stage 1 (`.governance/test/tge-state.md` shows test paths) | Greenfield project with zero existing test files |
| Mode is Brownfield (no AP, just existing code + tests) | Mode is Architecture Only AND no test directories exist |
| Mode is Full Chain AND test directories exist | User explicitly says "skip brownfield — we're starting fresh" |

**If skipped:** Log in state file: `Stage 4: Skipped (greenfield — no existing tests detected)`. Proceed to Stage 5.

---

## Depth Adaptation

| Depth | Assessment Scope | Gap Map Detail |
|-------|-----------------|---------------|
| **Minimal** | Count test files per directory. Match by filename pattern only. Produce summary: estimated coverage by component. | Counts + high-level gaps (component-level) |
| **Standard** | Read test file names + first-level content (describe blocks, test function names). Match to register entries by name similarity + component mapping. Produce detailed gap map with specific unmatched tests. | Per-entry matching + orphan identification + coverage % |
| **Comprehensive** | Read test file content (assertions, imports). Map test assertions to specific commitments. Identify partial coverage (test exists but doesn't cover all aspects). Produce full traceability matrix. | Assertion-level mapping + partial-coverage flags + quality assessment |

---

## MANDATORY: Stage Sub-Role — Audit Specialist

During THIS stage, ALSO adopt the mindset of an **Audit Specialist**. This does NOT replace your primary role (Senior QA Engineer / Test Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Map without modifying — your job is to OBSERVE and REPORT, not to change anything
- Be rigorous about evidence: "test exists" means a file is found AND it appears to test the right thing — a file named `user.test.js` doesn't automatically cover all user commitments
- Distinguish between coverage EXISTENCE (test file present) and coverage QUALITY (test actually verifies the commitment) — at Standard depth, focus on existence; at Comprehensive, assess quality
- Identify orphans without judgment — orphaned tests aren't "wrong," they may test things outside the current architecture scope

### Anti-Patterns for This Stage
- Do NOT modify or delete any existing test files — assessment is read-only
- Do NOT assume a test covers a commitment just because the filename matches — verify at Standard+ depth
- Do NOT report 100% coverage without checking that tests actually pass (if runtime data is available)
- Do NOT dismiss orphaned tests — they may indicate architecture documentation gaps

### Quality Check
A good output at this stage sounds like:
- "Scanned 142 test files across 4 directories. Mapped 67 to register entries (48% coverage). Found 31 orphaned tests (test things not in current register — may indicate undocumented architecture). 45 register entries have no matching test (Missing). Top uncovered area: integration tests for PaymentService (0 of 6 required tests exist)."

---

## Step-by-Step Execution

### Step 1: Identify Test Directories

From Stage 1 detection, locate all test-containing paths:

| Pattern | Framework Association |
|---------|---------------------|
| `tests/`, `test/` | Generic (Python, PHP, Go) |
| `__tests__/` | Jest (JavaScript/TypeScript) |
| `spec/` | RSpec (Ruby), Jasmine |
| `*.test.ts`, `*.test.js` | Jest, Vitest (co-located) |
| `*.spec.ts`, `*.spec.js` | Angular, Jasmine (co-located) |
| `*_test.go` | Go (co-located) |
| `*_test.py`, `test_*.py` | Pytest (co-located or in tests/) |
| `*Test.java`, `*Spec.java` | JUnit, Spock |
| `cypress/`, `e2e/`, `playwright/` | E2E test frameworks |
| `integration/` | Integration test directory |

**Record for state file:**
```markdown
## Test Directories Found
- {path}: {n} test files ({framework} pattern detected)
- {path}: {n} test files ({framework} pattern detected)
- Total: {N} test files across {n} directories
```

---

### Step 2: Catalog Existing Tests

Build an inventory of existing tests by reading file names and (at Standard+ depth) test block names:

**Minimal depth:**
```markdown
| File Path | Estimated Scope | Test Count |
|-----------|----------------|:----------:|
| tests/user.test.js | UserService | ~12 tests |
| tests/order.test.js | OrderService | ~8 tests |
```

**Standard/Comprehensive depth:**
```markdown
| File Path | Test Name / Describe Block | Component | Estimated Coverage |
|-----------|---------------------------|-----------|-------------------|
| tests/user.test.js | "POST /users creates user" | UserService, API-001 | Contract test (happy path) |
| tests/user.test.js | "POST /users rejects invalid email" | UserService, API-001 | Validation error test |
| tests/auth.test.js | "JWT token validation" | AuthService, SEC-001 | Auth valid test |
```

---

### Step 3: Match Tests to Register Entries

For each register entry (from Stage 3), attempt to find a matching existing test:

**Matching criteria (in priority order):**

| Match Type | Confidence | Example |
|-----------|:----------:|---------|
| **Exact name match** | High | Register: "POST /users returns 201" → Test: `it("POST /users returns 201")` |
| **Semantic match** | Medium | Register: "User creation contract test" → Test: `describe("user creation")` with POST assertion |
| **Component + type match** | Low | Register: "UserService unit test" → File: `user.test.js` (assumes component coverage) |
| **No match found** | — | Register entry has no corresponding test → Status: Missing |

**Update register entries:**
- Match found (High/Medium confidence) → Status: `Exists`, Verification: `{file_path}:{line or block}`
- Match found (Low confidence) → Status: `Exists (unverified)`, Note: `Confidence: Low — verify manually`
- No match → Status: `Missing`

---

### Step 4: Identify Orphaned Tests

Tests that exist but don't match any register entry:

```markdown
## Orphaned Tests

Tests found in codebase with no matching register commitment:

| File | Test Name | Possible Reason |
|------|-----------|----------------|
| tests/legacy-feature.test.js | "Legacy widget renders" | Deprecated feature? Component not in current AP |
| tests/utils.test.js | "formatDate handles timezone" | Utility — may not map to architectural commitment |
| e2e/smoke.spec.ts | "Homepage loads" | Smoke test — broader than specific commitment |
```

**Orphan analysis (Comprehensive depth):**
- Could indicate undocumented architecture (AP is incomplete)
- Could indicate deprecated tests (test code but no matching code)
- Could indicate utility/helper tests (valid but outside governance scope)
- Recommendation: Review orphans — some may need new register entries; others may be candidates for cleanup

---

### Step 5: Compile Brownfield Gap Map

```markdown
## Brownfield Gap Map

**Project:** {project_name}
**Scan Date:** {ISO timestamp}
**Test Files Scanned:** {N}
**Register Entries Assessed:** {N}

### Coverage Summary

| Metric | Count | Percentage |
|--------|:-----:|:----------:|
| Register entries with matching test (Covered) | {n} | {n}% |
| Register entries with no matching test (Uncovered) | {n} | {n}% |
| Tests with no matching register entry (Orphaned) | {n} | — |

### Coverage by Category

| Category | Total Required | Covered | Uncovered | Coverage % |
|----------|:-------------:|:-------:|:---------:|:----------:|
| API | {n} | {n} | {n} | {n}% |
| Security | {n} | {n} | {n} | {n}% |
| Business Logic | {n} | {n} | {n} | {n}% |
| Integration | {n} | {n} | {n} | {n}% |
| Data | {n} | {n} | {n} | {n}% |
| Performance | {n} | {n} | {n} | {n}% |
| Workflow | {n} | {n} | {n} | {n}% |

### Top Gaps (Highest-Risk Uncovered Areas)

| # | Area | Missing Tests | Impact |
|---|------|:-------------:|--------|
| 1 | {component/category} | {n} tests | {why this gap matters} |
| 2 |... |... |... |
| 3 |... |... |... |

### Orphan Analysis

| Disposition | Count | Action |
|-------------|:-----:|--------|
| Potentially valid (needs register entry) | {n} | Consider adding to register |
| Deprecated (no matching code) | {n} | Consider cleanup |
| Utility/helper (outside governance scope) | {n} | Leave as-is |
| Unknown (needs manual review) | {n} | Flag for team review |
```

---

### Step 6: Present for Review

```markdown
## Review: Brownfield Gap Map

I've scanned your existing test suite against the derived test register.

**Headline:** {n}% of required tests already exist — {n} gaps to address.

**Key findings:**
- **Covered:** {n} register entries have matching tests ({n}%)
- **Uncovered:** {n} register entries have NO matching tests ({n}%)
- **Orphaned:** {n} tests exist with no matching register commitment

**Top 3 gap areas:**
1. {Category}: {n} missing tests — {brief impact}
2. {Category}: {n} missing tests — {brief impact}
3. {Category}: {n} missing tests — {brief impact}

**Orphan highlight:** {n} tests may indicate architecture documentation gaps — recommend reviewing

**Full gap map saved to:** `.governance/test/brownfield-gap-map.md` (working document)

---

**Your response:**
- (a) **Approve** — assessment looks accurate; proceed to strategy generation
- (b) **Dispute mappings** — some tests are incorrectly matched/unmatched
- (c) **Add context** — I can explain some orphans (provide info)
- (d) **Rescan** — test directories have changed since detection (rescan)
```

---

## Gate

**This stage has a GATE.** The brownfield assessment represents the current reality of test coverage. If the user disputes mappings, resolve before proceeding — incorrect baseline coverage leads to wrong debt calculations.

---

## Output Artifacts

| Artifact | Location | Purpose |
|----------|----------|---------|
| Brownfield Gap Map | `.governance/test/brownfield-gap-map.md` | Working document — current coverage reality |
| Updated Test Register | `.governance/test/test-register.md` | Status field updated (Required → Exists / Missing) |
| Updated state file | `.governance/test/tge-state.md` | Stage 4 complete; coverage stats populated |

---

## Stage Completion Criteria

| Check | Pass Criteria |
|-------|---------------|
| All test directories scanned | Every path from Stage 1 detection assessed |
| Register entries updated | Each entry has Status = Exists or Missing |
| Orphans identified | Tests without register match cataloged |
| Coverage calculated correctly | Exists / (Total - Deprecated - Overridden) = Coverage % |
| No false positives | Low-confidence matches flagged for verification |
| Gap map produced | Summary + category breakdown + top gaps documented |
| User approved | Assessment accuracy confirmed |
| State file updated | Stage 4 = complete; coverage stats in state |
