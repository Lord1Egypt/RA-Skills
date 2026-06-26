# Post-Development Verification: Quality Metrics Reference

This document defines all 15 quality metrics organized across 4 quality layers. Each metric is used by the verification agent to assess deliverable readiness and guide the fix loop.

---

## Table of Contents

- [Layer 1: Design Quality Metrics](#layer-1-design-quality-metrics)
  - [1. Scenario Coverage Rate](#1-scenario-coverage-rate)
  - [2. Taxonomy Coverage Rate](#2-taxonomy-coverage-rate)
  - [3. Boundary Value Coverage Rate](#3-boundary-value-coverage-rate)
  - [4. Data Feature Coverage Rate](#4-data-feature-coverage-rate)
- [Layer 2: Execution Quality Metrics](#layer-2-execution-quality-metrics)
  - [5. Test Pass Rate](#5-test-pass-rate)
  - [6. Code Coverage](#6-code-coverage)
  - [7. Assertion Density](#7-assertion-density)
  - [8. Weak Assertion Ratio](#8-weak-assertion-ratio)
  - [9. Test Realism Ratio](#9-test-realism-ratio)
- [Layer 3: Delivery Quality Metrics](#layer-3-delivery-quality-metrics)
  - [10. Expectation Match Rate](#10-expectation-match-rate)
  - [11. Boundary Handling Rate](#11-boundary-handling-rate)
  - [12. Regression Safety Score](#12-regression-safety-score)
  - [12b. Business Flow Coverage](#12b-business-flow-coverage)
- [Layer 4: Iteration Efficiency Metrics](#layer-4-iteration-efficiency-metrics)
  - [13. Fix Convergence Rate](#13-fix-convergence-rate)
  - [14. Fix Introduction Rate](#14-fix-introduction-rate)
- [Threshold Classification](#threshold-classification)
- [Metric Collection Strategy](#metric-collection-strategy)

---

## Layer 1: Design Quality Metrics

> **Computed after test design, before test execution.** These metrics validate that the test plan is thorough enough to warrant running.

### 1. Scenario Coverage Rate

| Field | Value |
|---|---|
| **Formula** | `covered_requirements / total_requirements` |
| **Threshold** | **MUST = 100%** (hard gate) |
| **When to compute** | After test design phase, before execution |
| **Not met means** | One or more requirements have zero test coverage. Proceeding to execution would leave entire features unvalidated. Stop and add missing scenarios. |

### 2. Taxonomy Coverage Rate

| Field | Value |
|---|---|
| **Formula** | `taxonomy_categories_with_at_least_1_test / 3` (where 3 categories = MFT, INV, DIR) |
| **Threshold** | **MUST = 100%** (hard gate) |
| **When to compute** | After test design phase, before execution |
| **Not met means** | Tests only exercise one perspective (e.g., only normal paths or only invalid inputs). Blind spots exist where defects can hide. Every taxonomy category must have at least one representative test. |

### 3. Boundary Value Coverage Rate

| Field | Value |
|---|---|
| **Formula** | `covered_boundary_points / total_identified_boundary_points` |
| **Threshold** | **SHOULD >= 90%** (soft target) |
| **When to compute** | After test design phase, before execution |
| **Not met means** | Edge cases and boundary inputs are likely untested. Production may crash or produce incorrect results at data boundaries (e.g., zero, max value, empty string, off-by-one positions). Flag the uncovered boundaries and attempt to add tests before proceeding. |

### 4. Data Feature Coverage Rate

| Field | Value |
|---|---|
| **Formula** | `covered_data_feature_dimensions / total_identified_data_feature_dimensions` |
| **Threshold** | **SHOULD >= 85%** (soft target) |
| **When to compute** | After test design phase, before execution |
| **Not met means** | Certain data types, value ranges, or special values (null, empty, unicode, extreme magnitudes) are never tested. The system may fail silently or produce wrong results for unrepresented data patterns. Log which dimensions are missing and assess risk. |

---

## Layer 2: Execution Quality Metrics

> **Computed after test execution.** These metrics assess how well the tests ran and whether the test suite itself is of sufficient quality.

### 5. Test Pass Rate

| Field | Value |
|---|---|
| **Formula** | `passed_tests / total_tests` |
| **Threshold** | **SHOULD >= 95%** (soft target) |
| **When to compute** | After test execution phase |
| **Not met means** | A significant portion of functionality is broken. If below 80%, the deliverable is fundamentally unstable and should not proceed to delivery assessment. Investigate failure patterns -- are failures clustered in specific modules? |

### 6. Code Coverage

| Field | Value |
|---|---|
| **Formula** | `statements_covered / total_statements` (statement-level coverage) |
| **Threshold** | **SHOULD >= 80%** (soft target) |
| **When to compute** | After test execution phase (requires instrumentation) |
| **Not met means** | Large portions of the codebase are unexercised by any test. Untested code may harbor latent bugs. Prioritize covering the most critical and complex modules first. Do not blindly chase percentage -- a well-targeted 80% is better than a padded 95%. |

### 7. Assertion Density

| Field | Value |
|---|---|
| **Formula** | `total_assertions / total_tests` |
| **Threshold** | **SHOULD >= 2.0** (soft target) |
| **When to compute** | After test execution phase |
| **Not met means** | Tests contain too few assertions on average (e.g., many tests only check one thing). This indicates superficial validation -- tests may pass even when behavior is partially wrong. Each test should verify multiple relevant aspects of the output. |

### 8. Weak Assertion Ratio

| Field | Value |
|---|---|
| **Formula** | `weak_assertions / total_assertions` |
| **Threshold** | **SHOULD <= 10%** (soft target) |
| **When to compute** | After test execution phase |
| **Not met means** | A high proportion of assertions only verify shallow properties (e.g., checking that a value is not null, checking type, checking that an array has length > 0) without validating correctness. Such assertions give a false sense of coverage. Replace weak assertions with precise value/behavior checks. |

**Definition of weak assertions:**
- Checks that only verify existence, non-null, or type without examining value
- Checks that only verify a container is non-empty without examining contents
- Bare `assertTrue(result)` without inspecting what `result` actually is

### 9. Test Realism Ratio

| Field | Value |
|---|---|
| **Formula** | `real_execution_tests / total_tests` |
| **Threshold** | **MUST >= 70%** (hard gate, at L2 realism level) |
| **When to compute** | After test execution phase |
| **Not met means** | Too many tests rely on heavy mocking or stubbing. Integration issues between components are hidden behind fake boundaries. The test suite may pass while the real system fails. Increase the proportion of tests that exercise real component interactions. |

**Realism levels for reference:**
- **L0**: Fully mocked -- all dependencies replaced
- **L1**: Partially mocked -- external services mocked, internal components real
- **L2**: Integration-level -- real components, real data flows, only network/infra stubbed
- **L3**: End-to-end -- fully real execution

---

## Layer 3: Delivery Quality Metrics

> **Computed from test results.** These metrics determine whether the deliverable is ready for release.

### 10. Expectation Match Rate

| Field | Value |
|---|---|
| **Formula** | `tests_where_output_fully_matches_expectations / total_tests` |
| **Threshold** | Core functionality tests **MUST = 100%** (hard gate); overall **SHOULD >= 95%** (soft target) |
| **When to compute** | After test execution, during delivery assessment |
| **Not met means** | System behavior deviates from the expected specification. For core functionality, any deviation is a blocker -- the system does not do what it was designed to do. For non-core functionality, deviations indicate polish or correctness gaps that should be documented and triaged. |

**Definition of core functionality:** The primary use cases that define the purpose of the deliverable. Identified during requirements analysis. Typically the top 20% of requirements that deliver 80% of user value.

### 11. Boundary Handling Rate

| Field | Value |
|---|---|
| **Formula** | `passing_boundary_and_exception_tests / total_boundary_and_exception_tests` |
| **Threshold** | **SHOULD >= 90%** (soft target) |
| **When to compute** | After test execution, during delivery assessment |
| **Not met means** | The system handles normal cases correctly but fails on edge cases -- boundary values, invalid inputs, concurrent access, resource exhaustion, etc. Users will encounter these failures in production. Each failing boundary test represents a potential crash, data corruption, or silent error. |

### 12. Regression Safety Score

| Field | Value |
|---|---|
| **Formula** | `still_passing_tests / previously_passing_tests` |
| **Threshold** | **MUST = 100%** (hard gate) |
| **When to compute** | After each fix round, during delivery assessment |
| **Not met means** | Fixes or changes introduced new regressions -- code that was working before now breaks. This is a serious quality signal. Every regression must be investigated: either the fix is incorrect, or the original test had a hidden dependency. Do not proceed to delivery with any regression. |

### 12b. Business Flow Coverage

| Field | Value |
|---|---|
| **Formula** | `e2e_verified_business_flows / total_identified_business_flows` |
| **Threshold** | **MUST = 100%** (hard gate) |
| **When to compute** | After E2E test execution, during delivery assessment |
| **Not met means** | One or more critical business flows have not been validated through external calls (HTTP/CLI/Browser). The system may work in isolation but fail when a user walks through a real workflow end-to-end. This is the most direct measure of deliverability -- a flow that hasn't been externally validated is a flow that might break in production. Add E2E tests for every uncovered business flow using the templates in `references/real-e2e-templates.md`. |

**Definition of a business flow:** A multi-step user journey that traverses the system through its external interfaces (API endpoints, CLI commands, or browser interactions), involving two or more distinct operations linked by state or data. Examples: "register -> verify email -> login", "create order -> pay -> receive confirmation", "upload file -> process -> download result".

**Verification requirement:** Each business flow must be tested by sending real external requests through the running system -- not by calling internal functions or importing modules directly. The test must traverse the full flow from entry point to final outcome and verify the result at each step.

---

## Layer 4: Iteration Efficiency Metrics

> **Computed during the fix loop.** These are NOT pass/fail metrics. They are loop control signals that indicate when to stop iterating.

### 13. Fix Convergence Rate

| Field | Value |
|---|---|
| **Formula** | `newly_passing_tests_in_current_round / total_failures_in_previous_round` |
| **Threshold** | **< 20% for 2 consecutive rounds -> STOP the fix loop** |
| **When to compute** | After each fix round completes |
| **Not met means** | Fixes are not effective -- each round resolves very few failures. This typically indicates a fundamental design issue, architectural mismatch, or misunderstood requirements. Continuing to iterate will waste effort. STOP, reassess the approach, and consider a design-level change. |

**Example:**
```
Round 1: 20 failures
Round 2 fixes: 3 newly pass -> convergence = 3/20 = 15%
Round 3 fixes: 2 newly pass -> convergence = 2/17 ~ 12%
-> Two consecutive rounds below 20% -> STOP
```

### 14. Fix Introduction Rate

| Field | Value |
|---|---|
| **Formula** | `newly_failing_tests / total_fix_attempts` |
| **Threshold** | **> 30% in any round -> STOP the fix loop** |
| **When to compute** | After each fix round completes |
| **Not met means** | The fix approach is causing regressions faster than it resolves issues. This indicates the wrong fix strategy -- possibly cascading side effects, shared mutable state, or coupling between unrelated components. STOP and re-examine the root cause before applying more changes. |

**Example:**
```
Round N: applied 10 fixes
        4 previously-passing tests now fail
        -> introduction rate = 4/10 = 40%
        -> 40% > 30% -> STOP
```

---

## Threshold Classification

### Hard Gates (MUST)

Hard gates are **blocking thresholds**. If any MUST metric is not met, the deliverable **cannot proceed** to the next phase or to delivery. The agent must halt and either:

1. Fix the issue directly (add tests, fix regressions, improve realism), or
2. Escalate with a clear explanation of why the threshold cannot be met

Hard gates exist because they indicate fundamental quality problems that would result in delivering broken, incomplete, or misleadingly tested code.

| Hard Gate Metrics | Consequence of Failure |
|---|---|
| Scenario Coverage Rate < 100% | Uncovered requirements exist -- stop and add tests |
| Taxonomy Coverage Rate < 100% | Missing test perspectives -- stop and add tests |
| Test Realism Ratio < 70% | Tests are not trustworthy -- stop and increase realism |
| Expectation Match Rate (core) < 100% | Core functionality broken -- stop and fix |
| Regression Safety Score < 100% | Regressions introduced -- stop and investigate |
| Business Flow Coverage < 100% | Critical user journeys unverified through external calls -- add E2E tests |

### Soft Targets (SHOULD)

Soft targets are **advisory thresholds**. If a SHOULD metric is not met, the agent should:

1. Report the shortfall with context (which specific areas are weak),
2. Assess risk (what could go wrong given the gap),
3. Attempt to improve if time permits,
4. Proceed with documented justification if the gap is accepted

Soft targets represent best practices and risk indicators, not absolute blockers.

| Soft Target Metric | Risk When Below Threshold |
|---|---|
| Boundary Value Coverage Rate < 90% | Edge cases likely untested |
| Data Feature Coverage Rate < 85% | Data patterns untested |
| Test Pass Rate < 95% | Significant broken functionality |
| Code Coverage < 80% | Large untested code areas |
| Assertion Density < 2.0 | Superficial test validation |
| Weak Assertion Ratio > 10% | False confidence in test quality |
| Expectation Match Rate (overall) < 95% | Spec deviation in non-core areas |
| Boundary Handling Rate < 90% | Edge case failures in production |

---

## Metric Collection Strategy

### Automated Collection (from test runner output)

The following metrics can be extracted directly from standard test runner output with no manual intervention:

| Metric | Source | Collection Method |
|---|---|---|
| Test Pass Rate | Test runner stdout/stderr | Parse pass/fail/skip counts from runner output |
| Code Coverage | Coverage tool output (e.g., coverage report JSON) | Parse statement coverage percentage from coverage report |
| Assertion Density | Test runner output + static analysis | Count assertions via AST parsing of test files; divide by test count |
| Regression Safety Score | Comparison of test results across rounds | Diff pass/fail status between previous and current round results |
| Fix Convergence Rate | Comparison of test results across rounds | Count newly-passing tests by comparing current vs. previous round |
| Fix Introduction Rate | Comparison of test results across rounds | Count newly-failing tests by comparing current vs. previous round |

**Pseudocode for automated comparison across rounds:**
```
previous_results = load_results("round_N-1")
current_results  = load_results("round_N")

newly_passing = { t for t in current_results.passed if t in previous_results.failed }
newly_failing = { t for t in current_results.failed if t in previous_results.passed }

fix_convergence = len(newly_passing) / len(previous_results.failed)
fix_introduction = len(newly_failing) / len(previous_results.failed)
regression_safety = len(current_results.passed & previous_results.passed) / len(previous_results.passed)
```

### Semi-Automated Collection (agent analysis of test design)

The following metrics require the agent to analyze test design artifacts:

| Metric | Source | Collection Method |
|---|---|---|
| Scenario Coverage Rate | Requirements list + test scenario list | Agent maps each requirement to test scenarios; count coverage |
| Taxonomy Coverage Rate | Test scenario list | Agent classifies each test into MFT/INV/DIR categories; check all 3 present |
| Boundary Value Coverage Rate | Requirements + test scenario list | Agent extracts boundary points from requirements; maps to test cases |
| Data Feature Coverage Rate | Requirements + test scenario list | Agent extracts data dimensions from requirements; maps to test cases |

**Pseudocode for scenario coverage:**
```
requirements = extract_requirements(specification)
test_scenarios = extract_test_scenarios(test_plan)

coverage_map = {}
for req in requirements:
    coverage_map[req.id] = [s for s in test_scenarios if s.covers(req)]

scenario_coverage = count(coverage_map, has_tests=True) / len(requirements)
```

### Manual / Agent-Judgment Collection (requires reasoning)

The following metrics require the agent to exercise judgment about test quality:

| Metric | Source | Collection Method |
|---|---|---|
| Weak Assertion Ratio | Test source code | Agent inspects each assertion; classifies as "weak" or "strong" based on specificity |
| Test Realism Ratio | Test source code + configuration | Agent inspects test setup; classifies each test by realism level (L0-L3); counts L2+ as "real" |
| Expectation Match Rate | Test results + expected outputs | Agent compares actual output against documented expectations per test |
| Business Flow Coverage | Test plan + E2E test results | Agent lists all identified business flows from Phase 1 Step 0; verifies each has an E2E test that passed through external calls |

**Pseudocode for weak assertion classification:**
```
for assertion in test.assertions:
    if assertion.only_checks_existence:
        classify_as_weak(assertion)
    elif assertion.only_checks_type:
        classify_as_weak(assertion)
    elif assertion.checks_specific_value or assertion.checks_behavior:
        classify_as_strong(assertion)

weak_ratio = count(weak_assertions) / count(all_assertions)
```

### Summary: Collection Timing

| Phase | Metrics Collected |
|---|---|
| **After test design** | Scenario Coverage Rate, Taxonomy Coverage Rate, Boundary Value Coverage Rate, Data Feature Coverage Rate |
| **After test execution** | Test Pass Rate, Code Coverage, Assertion Density, Weak Assertion Ratio, Test Realism Ratio |
| **After delivery assessment** | Expectation Match Rate, Boundary Handling Rate, Regression Safety Score, Business Flow Coverage |
| **During fix loop** | Fix Convergence Rate, Fix Introduction Rate |
