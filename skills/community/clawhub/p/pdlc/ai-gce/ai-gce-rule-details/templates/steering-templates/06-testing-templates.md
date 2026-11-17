<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Testing Steering Templates

> **Purpose:** Used by the project-init-agent to generate testing-related steering files
> in the target project's `rules/` folder. These templates encode QA standards,
> coverage requirements, quality gates, and test generation guidance derived from `testing-strategy.md`.

---

## qa-standards.md (Always)

**Generates**: `rules/qa-standards.md`
**Derived From**: testing-strategy.md + project-governance.md + DEFINITION_OF_DONE.md

```markdown
---
inclusion: always
---

# QA Standards

## Test Generation Rules
- Every feature MUST have tests covering: happy path, error paths, boundaries, authorization
- Tests MUST verify behavior (observable outcomes), not implementation (internal calls)
- Test assertions MUST be specific: assert exact values, not just "not null"
- Test names MUST follow: {test_naming_convention}
- Tests MUST be independent: no shared mutable state, no execution order dependency

## Coverage Requirements
- Line coverage: minimum {line_coverage_business}% for business logic, {line_coverage_infra}% for infrastructure
- Branch coverage: minimum {branch_coverage}% for business logic
- Requirement coverage: 100% (every requirement has at least one test)
- Error path coverage: 100% (every documented error has a test)

## Quality Gates
- Build & Test stage CANNOT be approved with:
  - Any failing tests
  - Coverage below minimums
  - Missing tests for {critical_requirement_label} requirements
  - Unresolved security findings ({security_finding_threshold})

## AI Test Generation Guidance
- When generating tests, ALWAYS include:
  - At least 1 happy path test per method
  - At least 1 error/validation test per input parameter
  - Boundary value tests for numeric inputs
  - Authorization tests for protected endpoints
  - Integration tests for module boundary methods
```

---

## qa-review-triggers.md (FileMatch `{test_file_pattern}`)

**Generates**: `rules/qa-review-triggers.md`
**Derived From**: testing-strategy.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{test_file_pattern}"
---

# Test File Review Triggers

When test files are created or modified, verify:
1. Test assertions are specific (not just {weak_assertion_examples})
2. Test data is realistic (not {unrealistic_data_examples})
3. Async operations are properly awaited
4. Mocks verify important interactions (not just setup)
5. Each test tests ONE scenario (single logical assertion)
6. Negative tests exist alongside positive tests
```

---

## testing-advanced.md (Conditional — IF advanced testing strategy defined)

**Generates**: `rules/testing-advanced.md`
**Condition**: Generated IF testing-strategy.md defines property-based testing, mutation testing, or contract testing
**Derived From**: testing-strategy.md

```markdown
---
inclusion: always
---

# Advanced Testing Standards

## Technology
- Library: {advanced_test_library}
- Test Runner: {test_runner}
- Assertions: {assertion_library}
- Target Framework: {target_framework}

## {advanced_test_type} Configuration
- Default test count: {default_test_count} (local), {ci_test_count} (CI)
- Critical invariants: {critical_test_count} (local), {critical_ci_test_count} (CI)
- {reproduction_strategy}

## When to Use {advanced_test_type} vs Example-Based
- {advanced_test_type}: {advanced_test_use_cases}
- Example-based: {example_test_use_cases}
- Both: {combined_use_cases}
```

---

## testing-domain-specific.md (FileMatch `{domain_test_pattern}`)

**Generates**: `rules/testing-{domain_name}.md` (one per critical domain)
**Condition**: Generated IF domain-context.md identifies critical business invariants
**Derived From**: domain-context.md + testing-strategy.md

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{domain_test_pattern}"
---

# {Domain_Name} Testing Rules

## Mandatory Test Properties
Every {domain_name} module MUST have tests for:
{for_each_invariant}
- {invariant_name}: {invariant_test_description}
{end_for_each}

## Test Data Constraints
{for_each_domain_type}
- {type_name}: {valid_range_description}
  - Edge cases: {edge_cases}
  - Invalid states: {invalid_states}
{end_for_each}

## Test Isolation
- {domain_test_isolation_strategy}
- NEVER use production data in tests
- {domain_specific_test_rules}
```
