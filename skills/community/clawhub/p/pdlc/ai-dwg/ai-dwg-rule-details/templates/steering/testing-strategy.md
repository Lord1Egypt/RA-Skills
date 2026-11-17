<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: testing-strategy.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Quality Attributes + Technology Stack | date: {generation-date} -->

# Testing Strategy

## Test Pyramid
<!-- begin: AP-sourced -->
| Level | Scope | Speed | Coverage Target |
|-------|-------|:-----:|:---------------:|
| Unit | Single function/class | Fast | {target}% |
| Integration | Module + DB/API | Medium | Key flows |
| E2E | Full user journey | Slow | Critical paths |
<!-- end: AP-sourced -->

## Test Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| TEST-01 | Unit tests: required for all business logic |
| TEST-02 | Integration tests: required for all API endpoints |
| TEST-03 | E2E: critical user journeys only |
| TEST-04 | Test data: factories/builders — no hardcoded |
| TEST-05 | Mocking: mock externals, never mock the SUT |
| TEST-06 | Naming: `should {expected behavior} when {condition}` |
| TEST-07 | Arrange-Act-Assert structure |
| TEST-08 | One assertion per test (logical, not literal) |
<!-- end: AP-sourced -->

## What to Test
<!-- begin: AP-sourced -->
- Business logic (domain rules, calculations, state transitions)
- API contract (request/response format, status codes, validation)
- Data access (queries return correct data, scoping works)
- Error paths (invalid input, failures, edge cases)
- Security (auth required, unauthorized rejected, tenant isolated)
<!-- end: AP-sourced -->

## What NOT to Test
- Framework boilerplate (DI wiring, module declarations)
- Simple getters/setters with no logic
- Third-party library internals
- Configuration reading (trust the framework)

## Test Tools
<!-- begin: AP-sourced -->
| Tool | Purpose |
|------|---------|
| {unit-test-framework} | Unit + integration tests |
| {e2e-framework} | End-to-end tests |
| {mock-library} | Mocking external deps |
| {coverage-tool} | Coverage reporting |
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/team-to-agreements.md` (Target 5).
