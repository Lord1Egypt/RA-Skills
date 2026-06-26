---
name: post-dev-verification
description: >-
  Post-development full-stack verification skill. Automatically triggered after Agent completes a development task.
  Executes production-level validation (unit + integration + E2E) with real-execution-first philosophy.
  Use when: (1) Development task is complete and needs verification, (2) User says "run tests", "verify",
  "validate", "quality check", (3) User says "交付", "验证", "跑测试", "质量检查", "验收",
  (4) Before creating PRs or merging code, (5) After implementing features, bug fixes, or refactoring,
  (6) User asks "does this work?", "can we ship this?", "is this ready?".
  Covers: test design (MFT/INV/DIR taxonomy), quality metrics (4 layers, 15 metrics), feedback-driven fix loop,
  anti-pattern detection, visible/hidden test separation, reusable test script generation.
metadata:
  requires: "docker (optional), npm/pip/mvn/go (auto-detected), database client (optional)"
  capabilities: "read_project_files, run_tests, start_stop_services, network_access"
  safety_isolation: "Always run in a test/sandbox environment. Never use production credentials or production data."
  safety_credentials: "Uses only test accounts, test API keys, and environment-variable-sourced tokens. Never prompts for production secrets."
  safety_side_effects: "Starts/stops services, runs DB migrations, seeds test data, deletes test artifacts. All scoped to test environment."
  safety_recommendation: "Run Phase 0 (environment analysis) first to review what will be accessed before proceeding to execution phases."
---

# Post-Development Verification

Automated full-stack quality verification after development. **Real execution by default** -- mock is the last resort. **Deliverability is judged by external calls** (HTTP requests, CLI invocations, browser interactions), not by internal function calls passing in isolation.

## Core Philosophy: Real Execution First

Default realism level is **L2**: internal services run for real, only uncontrollable external dependencies (third-party APIs, paid services) may be mocked.

**Downgrade signals** (auto-detected from user intent):
- "快速验证" / "只测逻辑" / "mock就行" -> L0
- Pure function / utility library with no I/O -> L0
- Local environment cannot start service -> L1 (report reason)
- "生产级别" / "全面测试" / "验收测试" -> L3

**Realism level definitions:**
| Level | Description | Mock Ratio |
|-------|-------------|------------|
| L0 | All dependencies mocked | 100% |
| L1 | Core service real, databases mocked | <=50% |
| L2 | Internal services real, external deps mocked | <=30% |
| L3 | All services real (sandbox/test accounts) | 0% |

## Workflow

Execute phases sequentially. Each phase produces required artifacts for the next.

```
Phase 0: Environment Awareness
  v
Phase 1: Test Design (with anti-pattern scan)
  v
Phase 2: Execution & Evaluation
  v
Phase 3: Feedback & Fix Loop (if gates fail)
  v
Phase 4: Validation & Output
```

---

## Safety Requirements

This skill starts services, runs migrations, and makes network calls. Before execution:

1. **Run in isolation** -- use a test/sandbox environment, never production systems
2. **Use test credentials only** -- test accounts, test API keys, environment-variable tokens; never supply production secrets
3. **Phase 0 first** -- review the Environment Report before allowing execution phases (Phase 2+) to understand what will be accessed
4. **Scoped side effects** -- all service starts, DB migrations, test data seeding, and cleanup are limited to the test environment
5. **User control** -- the user can downgrade realism level (e.g., "快速验证" for L0) to reduce scope at any time

---

## Phase 0: Environment Awareness

Gather project context and determine feasibility before designing tests.

### 0.1 Project Analysis

Identify:
- **Language & Framework**: from config files (package.json, pyproject.toml, go.mod, etc.)
- **Project type**: monorepo / microservice / full-stack / library / CLI tool
- **Monorepo scope** (if applicable): identify which packages/services are affected by the current change
- **Test runner**: detect existing test framework (pytest, vitest, jest, go test, etc.)
- **Coverage tool**: detect coverage support (pytest-cov, vitest --coverage, nyc, etc.)
- **Build/start commands**: from scripts, Docker configs, Makefiles

### 0.2 Dependency Mapping

For each dependency service, classify:
- **Controllable** (self-hosted, has test env) -> must run real at L2+
- **Uncontrollable** (third-party, paid, no sandbox) -> acceptable to mock

### 0.3 Realism Level Decision

1. Check user intent signals -> override default if found
2. Check test target type -> pure functions auto-downgrade to L0
3. Assess local environment feasibility -> downgrade if services can't start
4. Record decision with rationale in the environment report

### 0.4 Environment Feasibility Check

Verify:
- Required tools installed (runtime, package manager, Docker if needed)
- Dependency services available (databases, caches, message queues)
- Target service can start locally
- **Environment consistency**: Docker/config matches production; environment variables and config files are complete; dependency service versions align with deployment target

Output: **Environment Report** -- language, framework, test runner, realism level, service availability, any blockers, consistency gaps.

---

## Phase 1: Test Design

Design test scenarios systematically using the test taxonomy. **Do NOT write test code before completing analysis.**

### 1.1 Pre-Analysis (Anti Leap-to-Code)

Before writing any test code, complete:
- **Code structure analysis**: control flow, function signatures, module dependencies
- **Dependency analysis**: external services, databases, API contracts involved
- **Constraint analysis**: business rules, data invariants, input/output contracts

>  If test code references modules/imports not in the actual codebase -> hallucinated dependency. Remove and use actual project references.

### 1.2 Scenario Identification

Map each requirement to test scenarios:
- Functional scenarios (one per acceptance criterion minimum)
- Integration scenarios (cross-module, data flow, API contract)
- Error/exception scenarios (all error handling branches)
- **End-to-end business flows** (complete user journeys that traverse multiple steps/services -- e.g., "register -> verify email -> login -> place order -> pay -> receive confirmation"; "admin creates user -> assigns role -> user logs in with correct permissions"). Each identified critical business flow MUST have at least one E2E test validated through external calls.

**Anti-pattern check**: If >80% of scenarios are happy path -> **Happy Path Obsession detected**. Add error, boundary, and exception scenarios until >=30% target error scenarios.

### 1.3 Apply Test Taxonomy

For each scenario, apply the appropriate taxonomy category. Load detailed guidance from `references/test-taxonomy.md` when needed.

| Category | Purpose | Example |
|----------|---------|---------|
| **MFT** (Minimum Functionality) | Verify each decision branch/leaf node works | Each code path returns correct result |
| **INV** (Invariance) | Same logical request -> same result, different phrasings | "show data" = "display info" = "list records" |
| **DIR** (Directional Expectation) | Vary one input -> predict output direction | Larger input -> larger output (monotonic) |

**Coverage rule**: Each of the 3 categories MUST have >=1 test. Taxonomy coverage = 100% is a **hard gate**.

### 1.4 Boundary Value Coverage

For every input parameter, identify and cover:
- **Numeric**: min-1, min, min+1, typical, max-1, max, max+1
- **String/Collection**: empty, single item, typical, max, exceeds max, special chars, Unicode
- **Optional**: not provided (default), explicit null/undefined, explicit empty

### 1.5 Real vs Mock Classification

Classify each scenario based on realism level:
- L2+: Internal service interactions -> **must run real**
- Any level: Uncontrollable external deps -> **acceptable to mock** (use realistic stubs)
- Track: test realism ratio = real tests / total tests >= 70% (hard gate at L2)

### 1.6 Visible/Hidden Test Separation

After designing all scenarios:
- Select **30-40%** as **hidden tests** (prioritize edge cases, adversarial inputs, error scenarios)
- Hidden tests are NOT exposed during fix loop -- reserved for Phase 4 validation
- Record the split in the test plan

### 1.7 Anti-Pattern Scan

Run the pre-execution checklist. Load detailed guidance from `references/anti-patterns.md` when needed.

| Anti-Pattern | Check | Action |
|-------------|-------|--------|
| Happy Path Obsession | >80% scenarios are normal flow | Add error/boundary tests |
| Weak Assertions | `assert(result != null)`, `assert(status == 200)` without body | Replace with specific value checks |
| Leap-to-Code | Test code written before structure analysis | Redo analysis first |
| Hallucinated Dependencies | References non-existent modules/imports | Replace with actual references |
| Missing Traceability | Generic test names (`test_1`, `test_func`) | Rename to describe specific behavior |

**Rule**: Each test name MUST describe the specific behavior being tested (e.g., `test_submit_empty_form_returns_422`). Each test MUST link to the requirement it validates.

**Fix all detected anti-patterns before proceeding to Phase 2.**

### Phase 1 Output

- Test plan with all scenarios (tagged: MFT/INV/DIR, real/mock, visible/hidden)
- Boundary value coverage matrix
- Anti-pattern scan results (all clear)

---

## Phase 2: Execution & Evaluation

### 2.1 Environment Preparation

Start services in dependency order with health checks:
```
for each service in dependency_order:
    start service
    wait_for_health_check (port/ping/readiness endpoint)
    if health_check fails:
        report blocker, downgrade realism level
```

Prepare test data using project's existing seed/migration mechanisms when available.

**System boot validation** -- before running any tests, verify the system itself is deliverable:
- The target service starts successfully from a clean state (no cached artifacts)
- All health/readiness endpoints return healthy
- Startup logs contain no ERROR-level entries (WARNs are logged for review)
- Required configuration and environment variables are complete
- If any boot validation fails -> this is a delivery blocker, report immediately

### 2.2 Test Execution

Run tests with coverage enabled. **The test suite MUST include an E2E layer validated through external calls** (HTTP requests to running services, CLI invocations, or browser interactions -- not internal function imports). Load execution templates from `references/real-e2e-templates.md` when designing this layer.

- Detect and use the project's native test runner and coverage tool
- Execute all visible tests (hidden tests reserved)
- **E2E layer**: exercise all identified critical business flows through external interfaces. If the project exposes an HTTP API, at minimum send real HTTP requests to each endpoint. If CLI, invoke real commands. If UI, drive real browser interactions.
- Capture: pass/fail per test, assertion output, error messages, coverage data

### 2.3 Metrics Collection

Compute all 4 layers of metrics. Load detailed definitions from `references/metrics.md` when needed.

**Design Quality** (computed after test design, before execution):
| Metric | Formula | Threshold |
|--------|---------|-----------|
| Scenario Coverage | covered requirements / total requirements | MUST = 100% |
| Taxonomy Coverage | categories with >=1 test / 3 | MUST = 100% |
| Boundary Value Coverage | covered boundary points / total identified | SHOULD >= 90% |
| Data Feature Coverage | covered data dimensions / total identified | SHOULD >= 85% |

**Execution Quality** (computed after test run):
| Metric | Formula | Threshold |
|--------|---------|-----------|
| Pass Rate | passed tests / total tests | SHOULD >= 95% |
| Code Coverage | statements covered / total statements | SHOULD >= 80% |
| Assertion Density | total assertions / total tests | SHOULD >= 2.0 |
| Weak Assertion Ratio | weak assertions / total assertions | SHOULD <= 10% |
| Test Realism Ratio | real tests / total tests | MUST >= 70% |

**Delivery Quality** (computed from test results):
| Metric | Formula | Threshold |
|--------|---------|-----------|
| Expectation Match Rate | fully matching tests / total tests (core: MUST 100%) | Core: MUST=100%, Overall: SHOULD>=95% |
| Boundary Handling Rate | passing boundary tests / total boundary tests | SHOULD >= 90% |
| Regression Safety | still-passing tests / previously-passing tests | MUST = 100% |
| Business Flow Coverage | E2E-verified business flows / total identified business flows | MUST = 100% |

**Iteration Efficiency** (computed during fix loop):
| Metric | Formula | Threshold |
|--------|---------|-----------|
| Fix Convergence Rate | newly passing / previous failures | <20% for 2 rounds -> STOP |
| Fix Introduction Rate | newly failing / total fix attempts | >30% -> STOP |

---

## Phase 3: Feedback & Fix Loop

Triggered when **hard gate metrics** are not met.

### 3.1 Generate Feedback Report

Structure the report as JSON. Load schema from `references/feedback-schema.md` when needed.

Key sections:
- **round**: current iteration number
- **project_context**: language, framework, test runner, realism level
- **metrics**: all 4 layers with pass/fail per metric
- **gate_result**: `"pass"` | `"fix_and_retry"` | `"stop_and_report"`
- **failures_grouped**: cluster by root cause, each with affected tests + fix direction
- **fix_history**: timeline of each round's metrics before/after, fix description, newly passing/failing
- **hidden_tests**: total count, run status, results (null during fix loop, populated in Phase 4)
- **anti_patterns_detected**: names of anti-patterns found in current test suite
- **next_action**: what the Agent should do next

### 3.2 Fix Prioritization

Address the **largest failure cluster first** (most affected tests) -- highest probability of improving overall pass rate.

### 3.3 Convergence Control -- Triple Exit Conditions

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Max iterations | 5 rounds | Stop, report current state |
| No convergence | <20% convergence rate for 2 consecutive rounds | Stop, suggest fundamental issue |
| Regression | >30% fix introduction rate in any round | Stop, suggest wrong fix approach |

### 3.4 Fix Loop Cycle

```
while round <= 5 AND not converged_stop AND not regression_stop:
    read feedback report -> identify largest failure cluster
    apply targeted fix to code/tests
    re-run full test suite (or failed-only if convergence is high)
    compute new metrics
    generate new feedback report
    check exit conditions
    record iteration in fix history
```

### Phase 3 Output

- Fix history timeline (round, metrics before/after, fix description, newly passing/failing)
- Final feedback report with gate_result

---

## Phase 4: Validation & Output

### 4.1 Hidden Test Validation

Run ALL hidden tests (not exposed during fix loop):
- If hidden tests pass -> validates that fixes are genuine, not overfitted
- If hidden tests fail -> report failures, do NOT re-enter fix loop

### 4.2 Quality Report

Generate final quality report:
- **Verdict**: `"PASS"` (all hard gates met) or `"FAIL"` (hard gates not met) with specific reasons
- All 4 layers of metrics with pass/fail status
- Fix history timeline
- Hidden test validation results
- Anti-pattern scan summary
- Recommendations for improvement

### 4.3 Reusable Test Scripts

Output test scripts that can run independently in CI/CD:
- Follow project's native test format and directory conventions
- Include run instructions: prerequisites, service startup, how to run, expected output
- Include environment documentation: services needed, config required, ports

---

## Quality Gate Quick Reference

### Hard Gates (MUST pass -- blocks delivery)

| Metric | Threshold |
|--------|-----------|
| Scenario Coverage | = 100% |
| Taxonomy Coverage | = 100% |
| Test Realism Ratio | >= 70% |
| Expectation Match (core) | = 100% |
| Regression Safety | = 100% |
| Business Flow Coverage | = 100% |

### Soft Targets (SHOULD pass -- reported, does not block unless configured)

| Metric | Threshold |
|--------|-----------|
| Boundary Value Coverage | >= 90% |
| Data Feature Coverage | >= 85% |
| Pass Rate | >= 95% |
| Code Coverage | >= 80% |
| Assertion Density | >= 2.0 |
| Weak Assertion Ratio | <= 10% |
| Boundary Handling Rate | >= 90% |

---

## References

Load these files as needed during the workflow:

- **`references/metrics.md`** -- Complete definitions for all 14 metrics: calculation formulas, threshold rationale, and what it means when a metric is not met. Load when computing or interpreting metrics.

- **`references/test-taxonomy.md`** -- Detailed guidance for MFT/INV/DIR test categories with pseudocode examples, plus systematic boundary value analysis methods. Load during Phase 1 test design.

- **`references/feedback-schema.md`** -- Full JSON Schema for feedback reports with a populated example. Load when generating feedback reports in Phase 3.

- **`references/anti-patterns.md`** -- Detailed detection methods and fix strategies for all 5 anti-patterns: Happy Path Obsession, Weak Assertions, Leap-to-Code, Hallucinated Dependencies, Missing Traceability. Load during Phase 1 anti-pattern scan or Phase 3 feedback.

- **`references/real-e2e-templates.md`** -- Environment preparation scripts and real E2E test templates for HTTP API, CLI tools, and Browser automation. Load during Phase 2 environment preparation and test execution.
