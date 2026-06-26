# Testing Protocol

> **Validation requirements and testing standards for autonomous development**
> Priority: HIGH | Category: Quality Assurance

## Overview

Autonomous agents must not compromise code quality. This skill defines testing standards, validation requirements, and quality gates that agents must follow.

## Testing Philosophy

```yaml
core_principles:
  test_before_trust:
    concept: "No code change is complete without tests"
    implementation: "Tests are part of the Definition of Done"

  validate_assumptions:
    concept: "Every claim must be verifiable"
    implementation: "Observable, measurable success criteria"

  fail_fast:
    concept: "Catch issues before they reach production"
    implementation: "Test at every layer of the stack"

  document_behavior:
    concept: "Tests are executable documentation"
    implementation: "Tests describe expected behavior"
```

## Test Categories

### 1. Unit Tests

```yaml
purpose: "Validate individual functions/components in isolation"

requirements:
  coverage:
    minimum: "80% of new code"
    target: "90%+ for critical paths"

  characteristics:
    - "Fast (milliseconds)"
    - "Isolated (no external dependencies)"
    - "Deterministic (same result every time)"
    - "Clear (one assertion per test ideally)"

example_structure:
  file: "tests/unit/auth.test.js"
  content:
    - "Test valid authentication"
    - "Test invalid password"
    - "Test missing credentials"
    - "Test token generation"
    - "Test token validation"
```

### 2. Integration Tests

```yaml
purpose: "Validate interactions between components"

requirements:
  scope:
    - "Database interactions"
    - "API endpoint integration"
    - "Service communication"
    - "External dependencies (mocked)"

  characteristics:
    - "Realistic component interaction"
    - "Controlled external dependencies"
    - "Clear setup/teardown"
    - "Repeatable"

example_structure:
  file: "tests/integration/api.test.js"
  content:
    - "Test full authentication flow"
    - "Test API with database"
    - "Test error handling through stack"
```

### 3. End-to-End Tests

```yaml
purpose: "Validate complete user workflows"

requirements:
  scope:
    - "Critical user journeys"
    - "Cross-service workflows"
    - "UI interactions (if applicable)"

  characteristics:
    - "Realistic user scenarios"
    - "Full stack integration"
    - "Critical path coverage only"

example_structure:
  file: "tests/e2e/user-workflow.test.js"
  content:
    - "Test user registration and login"
    - "Test user completes core action"
    - "Test user logout"
```

### 4. Manual Verification

```yaml
purpose: "Validate what cannot be automated"

requirements:
  cases:
    - "Visual verification"
    - "User experience validation"
    - "Performance observation"
    - "Error message clarity"

  documentation:
    - "Steps to reproduce"
    - "Expected observation"
    - "Actual observation"
    - "Screenshots where applicable"
```

## Testing Workflow

### During Development

```yaml
test_driven_approach:
  optional: true
  when: "Complex logic or critical paths"

  steps:
    1: "Write failing test for desired behavior"
    2: "Run test, confirm it fails"
    3: "Write minimum code to pass test"
    4: "Run test, confirm it passes"
    5: "Refactor if needed"
    6: "Run all tests, confirm nothing broke"

test_after_approach:
  default: true
  when: "Most development work"

  steps:
    1: "Make code change"
    2: "Write tests for new behavior"
    3: "Run new tests, confirm pass"
    4: "Run all tests, confirm nothing broke"
    5: "Fix any failures"
    6: "Re-run until all pass"
```

### Test Writing Standards

```yaml
naming:
  convention: "describe(what) test(condition expected)"
  examples:
    good: "test('returns 401 when password is invalid')"
    bad: "test('auth')"

structure:
  arrange_act_assert:
    arrange: "Setup test data and conditions"
    act: "Execute the function/behavior"
    assert: "Verify expected outcome"

  example:
    describe('authenticateUser', () => {
      it('returns JWT token for valid credentials', () => {
        // Arrange
        const user = { email: 'test@example.com', password: 'correct' }

        // Act
        const result = authenticateUser(user)

        // Assert
        expect(result).toHaveProperty('token')
        expect(result.token).toMatch(/^[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+$/)
      })
    })
```

## Test Coverage Requirements

### Minimum Coverage Standards

```yaml
coverage_thresholds:
  critical_paths:
    lines: 90
    functions: 90
    branches: 85
    statements: 90

  standard_code:
    lines: 80
    functions: 80
    branches: 75
    statements: 80

  utility_code:
    lines: 70
    functions: 70
    branches: 65
    statements: 70
```

### Coverage Analysis

```bash
# Generate coverage report
npm test -- --coverage

# Check coverage against thresholds
npm test -- --coverage --coverageThreshold='{\"global\":{\"lines\":80}}'

# Find uncovered lines
npm test -- --coverage --verbose

# HTML coverage report
npm test -- --coverage --coverageReporters=html
# Open coverage/index.html
```

## Quality Gates

### Pre-Commit Checklist

```yaml
before_considering_complete:
  unit_tests:
    - [ ] "All new unit tests pass"
    - [ ] "All existing unit tests still pass"
    - [ ] "Coverage thresholds met"
    - [ ] "No test warnings"

  integration_tests:
    - [ ] "All new integration tests pass"
    - [ ] "All existing integration tests still pass"

  manual_verification:
    - [ ] "Core user path tested manually"
    - [ ] "Error scenarios tested"
    - [ ] "Edge cases considered"
```

### Pre-Merge Checklist

```yaml
before_merge:
  automated:
    - [ ] "All tests pass (unit + integration + e2e)"
    - [ ] "Coverage report generated"
    - [ ] "No linting errors"
    - [ ] "No security vulnerabilities found"

  review:
    - [ ] "Code reviewed"
    - [ ] "Tests reviewed"
    - [ ] "Documentation reviewed"
    - [ ] "Performance impact assessed"
```

## Test Data Management

### Fixtures and Factories

```yaml
test_data_principles:
  use_factories:
    reason: "Flexible, maintainable test data"
    tool: "Factory Boy, Rosie, or similar"

  avoid_hardcoded:
    problem: "Fragile, hard to maintain"
    solution: "Generate data programmatically"

  cleanup:
    requirement: "Clean up test data after each test"
    implementation: "beforeEach/afterEach hooks"

example_factory:
  # Python Factory Boy example
  class UserFactory(factory.Factory):
    class Meta:
      model = User

    email = factory.Faker('email')
    name = factory.Faker('name')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
```

### Mock and Stub Standards

```yaml
when_to_mock:
  external_apis: "Always mock (slow, unreliable)"
  database: "Sometimes mock for unit tests"
  file_system: "Mock for unit tests, real for integration"
  time: "Always mock (determinism)"

  dont_mock:
    - "The code you're testing"
    - "Simple value objects"
    - "Internal logic"
```

## Test Documentation

### Test Documentation Requirements

```yaml
in_code:
  - "Clear test names describing scenario"
  - "Comments for complex setup"
  - "Comments explaining assertions"

  separate_docs:
    - "Testing strategy document"
    - "Test data guide"
    - "How to run tests locally"
    - "CI/CD test configuration"
```

### Test README Template

```markdown
# Testing Guide

## Running Tests

### All Tests
```bash
npm test
```

### Unit Tests Only
```bash
npm run test:unit
```

### Integration Tests Only
```bash
npm run test:integration
```

### Specific Test File
```bash
npm test -- auth.test.js
```

### With Coverage
```bash
npm test -- --coverage
```

## Test Structure

```
tests/
├── unit/           # Isolated component tests
├── integration/    # Cross-component tests
├── e2e/           # Full workflow tests
└── fixtures/      # Test data and factories
```

## Writing Tests

1. Use `describe` blocks for grouping
2. Use `test` or `it` for individual tests
3. Follow Arrange-Act-Assert pattern
4. One assertion per test (ideal)
5. Descriptive test names

## CI/CD

Tests run automatically on:
- Every pull request
- Every merge to main
- Daily scheduled run
```

## Common Testing Pitfalls

### ❌ Testing Implementation Details

```javascript
// BAD - Tests internal structure
test('user has password property', () => {
  expect(user).toHaveProperty('password')
})

// GOOD - Tests behavior
test('user can authenticate with correct password', () => {
  expect(user.authenticate('correct')).toBe(true)
})
```

### ❌ Brittle Test Data

```javascript
// BAD - Hardcoded, fragile
const user = {
  email: 'test@example.com',
  password: 'password123',
  id: 1,
  createdAt: '2024-01-01'
}

// GOOD - Generated, flexible
const user = UserFactory.create()
```

### ❌ Overspecified Tests

```javascript
// BAD - Tests too many things
test('user authentication', () => {
  // Tests 10 different scenarios
})

// GOOD - Focused tests
test('authenticates with valid credentials', () => { })
test('rejects invalid password', () => { })
test('handles missing user', () => { })
```

### ❌ No Teardown

```javascript
// BAD - Leaves test data
afterEach(() => {
  // Nothing
})

// GOOD - Cleans up
afterEach(async () => {
  await Database.truncate()
})
```

## Test Monitoring

### Track Test Health

```bash
# Test failure rate
openclaw metrics test-failures

# Test execution time
openclaw metrics test-duration

# Coverage trends
openclaw metrics coverage-trend

# Flaky test detection
openclaw metrics flaky-tests
```

## Key Takeaway

**Tests are not optional. They're the contract between what you think your code does and what it actually does.** Never skip them.

---

**Related Skills**: `execution-discipline.md`, `scope-control.md`, `docs-first.md`
