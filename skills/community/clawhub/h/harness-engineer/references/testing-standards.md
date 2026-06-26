# TESTING STANDARDS

Testing is the primary deterministic verification layer. LLM judgment is never a
substitute for a failing test. Deterministic constraints are always checked before
LLM-based review.

---

## VERIFICATION ORDER (deterministic first)

1. Pre-commit hooks (linter, formatter, type-checker) -- must pass before ANY test run
2. Unit tests
3. Integration tests
4. E2E tests
5. Then: 3-layer recursive review cycle (agents/reviewer.md)

LLM review runs LAST, after all deterministic checks pass.
A passing LLM review does not override a failing test.

---

## PRE-COMMIT HOOKS (mandatory)

Every repo using this harness must have pre-commit hooks that:
  - Run the linter (no lint errors allowed)
  - Run the type-checker if applicable (no type errors)
  - Run a formatter check (no unformatted files)
  - Block the commit if any hook fails

Pre-commit hooks are deterministic, fast, and do not require LLM judgment.
They catch the largest class of common errors at zero extra cost.

Configure in .pre-commit-config.yaml or equivalent for the stack.

---

## REQUIRED TESTS

Unit tests:
  - Coverage >= 90% on all changed files (CONFIG.yaml testing.coverage_minimum)
  - Each test must be deterministic -- no random failures, no time-dependent assertions
  - Each test must be isolated -- no shared mutable state between tests
  - Fast: < 100ms per test

Integration tests:
  - At least one per major code path affected by the plan
  - Test the contract between components, not internals

E2E tests:
  - At least one per user-facing behavior in the plan
  - Exercises the full stack from input to output

---

## RECOMMENDED (required on critical paths)

Fuzz tests:
  - All input parsing, serialization, external data ingestion

Property-based tests:
  - Algorithms with invariants

---

## COVERAGE RULE

Minimum 90% line coverage on changed files.
Coverage alone is insufficient. Tests must assert correct behavior, not just execute lines.
A test that always passes regardless of code is worse than no test.

---

## TEST QUALITY RULES

- Tests must be meaningful -- assert the behavior described in the plan
- Tests must be maintainable -- clear test name, clear assertion message
- Tests must not suppress errors -- no bare except, no ignoring failures

---

## FAILURE PROTOCOL

When tests fail:
1. collect_logs() immediately
2. Identify the smallest failing case
3. Dispatch debugger_agent with failure log and test output
4. Identify harness gap category (runtime/observability.md)
5. Do NOT merge. Do NOT advance cycle phase.
6. Write MEMORY.md entry (EPISODIC type)

---

## TEST RESULT FORMAT (required from tester_agent)

```json
{
  "phase": "unit | integration | e2e | fuzz",
  "passed": 0,
  "failed": 0,
  "skipped": 0,
  "coverage": "0%",
  "failures": [
    {
      "test": "test_name",
      "file": "tests/path.test.ts",
      "reason": "AssertionError: expected X got Y",
      "log_ref": "CYCLE-NNN tool-log entry ID"
    }
  ]
}
```

Note: log_ref points to a tool-log entry ID -- never raw log content.

---

## THE TDD CYCLE (RED-GREEN-REFACTOR)

For any new behavior or bug fix, follow this cycle:

```
RED:    Write a test that fails (proves the behavior doesn't exist yet)
GREEN:  Write the minimum code to make it pass
REFACTOR: Clean up the implementation while tests stay green
```

A test that passes on the first run proves nothing. A test that never fails
is as useless as a test that always fails.

### The Prove-It Pattern (bug fixes)
When a bug is reported, do NOT start by fixing it:
1. Write a test that reproduces the bug (must FAIL with current code)
2. Confirm the test fails
3. Implement the fix
4. Test passes (proving the fix works)
5. Run full suite (no regressions)

Bug fixes without reproduction tests are incomplete.

---

## TEST PYRAMID

Distribute testing effort according to the pyramid:

```
        ╱╲
       ╱  ╲  E2E Tests (~5%)
      ╱    ╲  Full user flows, real browser
     ╱──────╲
    ╱        ╲  Integration Tests (~15%)
   ╱          ╲  Component interactions, API boundaries
  ╱────────────╲
 ╱              ╲  Unit Tests (~80%)
╱                ╲  Pure logic, isolated, milliseconds each
╱──────────────────╲
```

### Decision Guide
```
Is it pure logic with no side effects?
  → Unit test (small)
Does it cross a boundary (API, database, file system)?
  → Integration test (medium)
Is it a critical user flow that must work end-to-end?
  → E2E test (large) -- limit these to critical paths
```

### Test Sizes (Resource Model)
| Size | Constraints | Speed | Example |
|------|------------|-------|---------|
| **Small** | Single process, no I/O, no network, no database | Milliseconds | Pure function tests, data transforms |
| **Medium** | Multi-process OK, localhost only, no external services | Seconds | API tests with test DB, component tests |
| **Large** | Multi-machine OK, external services allowed | Minutes | E2E tests, performance benchmarks |

Small tests should make up the vast majority of the suite.

---

## WRITING GOOD TESTS

### Test State, Not Interactions
Assert on the **outcome** of an operation, not on which methods were called internally.
Tests that verify method call sequences break when you refactor.

### DAMP Over DRY in Tests
In production code, DRY is right. In tests, **DAMP** (Descriptive And Meaningful Phrases)
is better. Each test should tell a complete story without requiring the reader to
trace through shared helpers. Duplication in tests is acceptable when it makes each
test independently understandable.

### Prefer Real Implementations Over Mocks
Preference order (most to least preferred):
1. Real implementation → Highest confidence, catches real bugs
2. Fake → In-memory version of a dependency (e.g., fake DB)
3. Stub → Returns canned data, no behavior
4. Mock (interaction) → Verifies method calls — use sparingly

Use mocks only when: the real implementation is too slow, non-deterministic, or has
uncontrollable side effects. Over-mocking creates tests that pass while production breaks.

### Mock at Boundaries Only
Mock these:
- Database calls, HTTP requests, file system operations, external APIs, time/date
Do NOT mock these:
- Internal utility functions, business logic, data transformations, pure functions

### One Assertion Per Concept
Each test verifies one behavior. Don't bundle "rejects empty", "trims whitespace",
and "enforces max length" into a single test.

### Name Tests Descriptively
```
Good:  'sets status to completed and records timestamp'
Good:  'throws NotFoundError for non-existent task'
Good:  'is idempotent -- completing an already-completed task is a no-op'
Bad:   'works'
Bad:   'handles errors'
Bad:   'test 3'
```

---

## TEST ANTI-PATTERNS

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Testing implementation details | Tests break on refactor even if behavior unchanged | Test inputs/outputs, not internal structure |
| Flaky tests (timing, order-dependent) | Erode trust in the test suite | Use deterministic assertions, isolate test state |
| Testing framework code | Wastes time testing third-party behavior | Only test YOUR code |
| Snapshot abuse | Large snapshots nobody reviews, break on any change | Use snapshots sparingly and review every change |
| No test isolation | Tests pass individually but fail together | Each test sets up and tears down its own state |
| Mocking everything | Tests pass but production breaks | Prefer real > fakes > stubs > mocks. Mock only at boundaries |
| Skipping tests to pass CI | Hides real bugs | Fix or delete the test |
| Overly broad assertions | Doesn't catch regressions | Be specific |

---

## MECHANICAL ENFORCEMENT

In addition to test coverage, quality is enforced via custom linters that run in
pre-commit hooks. See references/mechanical-enforcement.md for the full list.

Linter rules encode architectural constraints (dependency directions, file size limits,
naming conventions, structured logging). When a linter violation occurs, the error
message includes remediation instructions that go directly into agent context.

"Documentation falls short? Promote the rule into code."
