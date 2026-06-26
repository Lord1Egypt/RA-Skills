# Test Anti-Patterns: Detection & Fix Strategies

Common anti-patterns in AI-generated tests that reduce effectiveness and create a false sense of security. The post-dev-verification skill runs anti-pattern detection as part of Phase 1 (test design) and reports any detected patterns in Phase 3 feedback.

---

## Table of Contents

- [1. Happy Path Obsession](#1-happy-path-obsession)
- [2. Weak Assertions](#2-weak-assertions)
- [3. Leap-to-Code](#3-leap-to-code)
- [4. Hallucinated Dependencies](#4-hallucinated-dependencies)
- [5. Missing Traceability](#5-missing-traceability)
- [Anti-Pattern Checklist](#anti-pattern-checklist)
- [Anti-Pattern Severity](#anti-pattern-severity)

---

## 1. Happy Path Obsession

### Definition

Tests only cover normal/happy path scenarios (>80% normal flow), ignoring error handling, boundary conditions, and failure states. This creates a false sense of security because the tests always pass in ideal conditions but fail to catch real-world failure modes.

### Detection Method

- **Scenario ratio check**: If >80% of test scenarios follow the pattern "valid input -> expected output" with no error, boundary, or exception tests, flag the suite.
- **Error path coverage check**: Verify that every error handling code path in the production code has at least one corresponding test.
- **Minimum threshold**: At least 30% of tests should target error/exception/failure scenarios.

**What to look for:**

- All test inputs are valid, well-formed, and within expected ranges
- No tests simulate timeouts, network failures, or service unavailability
- No tests for invalid authentication, missing permissions, or expired tokens
- No tests for malformed input (wrong types, missing fields, oversized payloads)
- No tests for concurrent access conflicts or race conditions

### Fix Strategy

1. **Audit error handling code**: List all error handling branches in the production code -- `try`/`catch` blocks, error return values, validation guards, rejection handlers.
2. **Create error branch tests**: Write at least one test for each identified error branch.
3. **Add boundary value tests**: Test with empty input, oversized input, wrong types, null/undefined values, and values at type limits (max integer, empty string, zero).
4. **Add integration failure tests**: Simulate external service failures -- database connection refused, API timeout, network partition, rate limiting responses.
5. **Set a target**: Ensure >=30% of tests exercise error/exception/failure scenarios.

### Pseudocode Detection Pattern

```
# Detection
normal_scenarios = count(scenarios where type == "happy_path")
total_scenarios = count(all scenarios)
ratio = normal_scenarios / total_scenarios
if ratio > 0.80:
    flag("happy_path_obsession", f"{ratio:.0%} scenarios are happy path")
```

---

## 2. Weak Assertions

### Definition

Assertions that only verify "something exists" or "something didn't crash" without verifying specific content. These tests give false confidence -- they pass even when the code produces incorrect results, as long as it produces *something*.

### Detection Method -- Weak Assertion Patterns

Scan for these common weak assertion patterns:

| Weak Assertion | Why It's Weak |
|---|---|
| `assert(result != null)` / `assert(result is not None)` | Only proves a value was returned, not that it's correct |
| `assert(result != undefined)` | Same -- existence != correctness |
| `assert(response.status == 200)` without body check | Confirms request didn't fail, but doesn't verify response content |
| `assert(len(array) > 0)` without content check | Confirms non-empty, but array could contain wrong data |
| `assert(error is None)` -- only checks no error | Confirms no crash, doesn't verify correctness of the result |
| `assert(typeof result === "object")` -- only checks type | Type is correct, but content could be entirely wrong |
| `assert(true)` / `assert(1)` -- tautological | Always passes; asserts nothing meaningful |

**Additional signals of weak assertions:**

- A test file has many passing tests but the code it tests has known bugs
- Assertions never reference specific expected values (magic numbers, strings, IDs)
- `try`/`catch` blocks in tests that catch all exceptions and silently pass

### Fix Strategy -- Replace with Specific Assertions

| Weak Assertion | Replace With |
|---|---|
| `assert(result != null)` | `assert(result.name == "expected_name" and result.id > 0)` |
| `assert(status == 200)` | Add `assert(response.body.items.length == expected_count)` and `assert(response.body.items[0].field == "value")` |
| `assert(len(array) > 0)` | `assert(array[0].key == "expected" and len(array) == expected_size)` |
| `assert(error is None)` | `assert(error is None) and assert(result.value == expected_value)` -- verify correctness alongside no-error check |

**Rule of thumb for response tests:** Each response test should verify all three:
1. **Status code** -- was the request handled correctly?
2. **Body structure** -- does the response have the expected shape?
3. **At least one specific field value** -- is the actual data correct?

### Pseudocode Detection Pattern

```
# Detection
weak_patterns = [
    "assert(result != null)",
    "assert(result is not None)",
    "assert(response.status == 200)",  # only status, no body check
    "assert(len(array) > 0)",          # only existence, no content
    "assert(error is None)",            # only no-error, no correctness
]
for each assertion in test_suite:
    if matches_any(assertion, weak_patterns) and no_specific_check_nearby(assertion):
        flag("weak_assertion", assertion)
```

---

## 3. Leap-to-Code

### Definition

Writing test code immediately without first analyzing the system's structure, dependencies, constraints, and semantics. This leads to tests that reference non-existent modules, miss critical paths, and have low real coverage despite appearing comprehensive.

### Root Cause

AI models (and developers) often jump straight to writing test code based on assumptions about how the system works rather than reading and analyzing the actual codebase. The result is a test suite that looks plausible but doesn't align with reality.

### Detection Method

- **Import mismatch**: Test code references imports or modules not present in the actual codebase (hallucinated dependencies).
- **Structural mismatch**: Test structure doesn't reflect actual code structure -- testing functions that don't exist, calling methods with wrong signatures, or asserting on properties that aren't returned.
- **No pre-analysis evidence**: No comments, annotations, or documentation describing what was analyzed before tests were written. The test file appears to have been written in a vacuum.

**Red flags:**

- Test imports a module that doesn't exist in the project
- Test calls `function(arg1, arg2)` but the actual function signature is `function(arg1, arg2, arg3)`
- Test asserts on a return type that differs from the actual return type
- Test mocks an interface that doesn't match the real interface
- Test covers a feature that was removed or renamed

### Fix Strategy

1. **STOP writing test code immediately.**
2. **Complete structure analysis**: Map all functions, their signatures, parameters, return types, and side effects. Document what each module exports.
3. **Complete dependency analysis**: Identify all external services, databases, APIs, and third-party libraries the code interacts with. Map their interfaces.
4. **Complete constraint analysis**: Document business rules, data invariants, API contracts, and behavioral guarantees that the code must satisfy.
5. **Only then write test code** based on the verified analysis -- not assumptions.

### Pseudocode Detection Pattern

```
# Detection
for each import/reference in test_code:
    if not exists_in_codebase(import):
        flag("hallucinated_dependency", f"{import} not found in project")
```

---

## 4. Hallucinated Dependencies

### Definition

Test code references functions, modules, imports, or APIs that don't exist in the actual codebase. This is a specific and severe manifestation of the Leap-to-Code anti-pattern. Tests with hallucinated dependencies cannot even compile or run, making them entirely worthless.

### Common Forms

- **Wrong module paths**: `import { userService } from "./services/UserService"` when the actual path is `./services/user-service`
- **Non-existent functions**: Calling `getUserById()` when the actual function is `fetchUser()`
- **Wrong parameter names**: Passing `{ username }` when the function expects `{ email }`
- **Fabricated utility functions**: Importing a `validateEmail()` helper that was never written
- **Wrong class names**: Instantiating `UserAccount` when the class is `Account`
- **Phantom API endpoints**: Testing against `/api/v2/users` when only `/api/v1/users` exists

### Detection Method

1. **Parse all imports** in test files and verify each resolved module exists in the project source or installed dependencies.
2. **Check function calls** against actual exported functions -- verify name, arity (parameter count), and parameter types.
3. **Check class names and method names** against the actual codebase.
4. **Run the project's type checker or linter** -- it will catch unresolved references.
5. **Attempt to execute the tests** -- hallucinated dependencies cause immediate compilation or import failures.

**Systematic verification:**

```
for each test_file in test_directory:
    for each import in test_file.imports:
        resolved = resolve_module(import)
        if resolved is None:
            flag("hallucinated_import", import)
    for each call in test_file.function_calls:
        target = resolve_target(call)
        if target is None:
            flag("hallucinated_function", call.name)
        elif call.arity != target.arity:
            flag("arity_mismatch", call.name)
```

### Fix Strategy

1. **List all unresolved references** in the test code.
2. **For each unresolved reference**, either:
   - Remove it if the test doesn't need it
   - Replace it with the correct actual reference from the codebase
3. **Re-run the type checker / linter** to catch any remaining issues.
4. **Run the test suite** to confirm all tests can at least compile and execute.

### Relationship to Leap-to-Code

Hallucinated Dependencies is the most visible symptom of Leap-to-Code. If you detect hallucinated dependencies, the root cause is almost always insufficient pre-analysis. Fixing the dependencies without fixing the analysis process will lead to other problems (missed paths, wrong assertions, etc.).

---

## 5. Missing Traceability

### Definition

Tests lack clear links to the requirements or scenarios they validate. This makes it impossible to determine whether all requirements are covered, which requirement a failing test relates to, or what behavior a test was intended to verify when it needs to be updated.

### Detection Method -- Generic Test Name Patterns

Scan test names for these patterns:

| Pattern | Examples | Problem |
|---|---|---|
| Numeric suffixes | `test_1`, `test_2`, `test_3` | No meaning; impossible to know what each tests |
| Generic subject | `test_func`, `test_function`, `test_method` | Doesn't identify which function or what about it |
| Vague outcome | `test_it_works`, `test_works`, `test_correct` | Doesn't specify what "works" means |
| Single letter | `test_a`, `test_b` | No information at all |
| Trivially short | `test_run`, `test_go`, `test_do` | No indication of input, condition, or expected result |

**Additional signals:**

- No comments or annotations linking tests to requirements documents, tickets, or specifications
- Test descriptions use vague language like "checks the feature" or "verifies the function"
- Reading the test body is the only way to understand what it validates
- No requirement-to-test mapping exists

### Fix Strategy

1. **Rename tests to describe specific behavior** using the pattern `test_<subject>_<condition>_<expected_result>`:
   - `test_submit_empty_form_returns_422`
   - `test_delete_nonexistent_user_returns_404`
   - `test_transfer_insufficient_funds_raises_error`
   - `test_login_valid_credentials_returns_jwt_token`

2. **Add requirement links** as comments or annotations:
   ```
   // Validates REQ-3.2: Input validation for email field
   // Covers user story US-42: User cannot submit form with invalid email
   // Scenario: AC-7 from PRD -- System rejects malformed phone numbers
   ```

3. **Create a requirement-to-test mapping table** that lists each requirement and the tests that cover it. This makes gaps immediately visible.

### Pseudocode Detection Pattern

```
# Detection
generic_patterns = [
    r"test_\d+$",          # test_1, test_2
    r"test_func",          # test_func
    r"test_it_",           # test_it_works
    r"test_[a-z]$",        # test_a
]
for each test_name in test_suite:
    if matches_any(test_name, generic_patterns):
        flag("missing_traceability", test_name)
```

---

## Anti-Pattern Checklist

Run this checklist after completing test design (Phase 1). Every item must pass before proceeding.

1.  **Happy path ratio <= 70%** -- error/boundary/exception tests make up >=30% of the test suite
2.  **No weak assertions** -- each assertion verifies specific content, not just existence or non-crash
3.  **Structure analysis completed before test code** -- no hallucinated imports or fabricated function calls
4.  **All imports/references exist in actual codebase** -- every module, function, and class resolves correctly
5.  **All test names describe specific behavior** -- follows `test_<subject>_<condition>_<expected_result>` pattern
6.  **Each test links to a requirement or scenario** -- traceable via name, comment, or annotation

---

## Anti-Pattern Severity

| Anti-Pattern | Severity | Impact if Undetected |
|---|---|---|
| **Happy Path Obsession** | High | Error handling untested; production crashes on edge cases that tests should have caught |
| **Weak Assertions** | High | Tests pass but bugs go undetected; false green builds; developers trust passing tests that verify nothing meaningful |
| **Leap-to-Code** | Medium | Low real coverage despite appearing comprehensive; critical code paths untested; tests misaligned with actual system behavior |
| **Hallucinated Dependencies** | Critical | Tests don't even compile or run; entire test suite is dead code; wastes time and creates confusion |
| **Missing Traceability** | Low | Hard to maintain tests; unclear what's covered; requirement gaps go unnoticed; test updates become guesswork |
