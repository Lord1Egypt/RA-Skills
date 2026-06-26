---
name: write-tests
description: Generate tests to achieve coverage targets
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: true
---

# Write Tests

Generate tests for specified code to achieve coverage targets.

## What It Does

1. Reads the target file(s)
2. Analyzes functions and classes to test
3. Identifies edge cases and error scenarios
4. Generates comprehensive test file(s)
5. Follows project testing patterns

## Usage

```
/write-tests <path> [coverage]
```

**Arguments:**
- `path` (required): File or directory to generate tests for
- `coverage` (optional): Target coverage percentage (default: 80)

## Output

Creates test files following project conventions:
- `*.test.ts` for TypeScript
- `*.test.js` for JavaScript
- `test_*.py` for Python

## Test Coverage

| Coverage | Description |
|----------|-------------|
| 80% | Standard target (default) |
| 90% | High coverage for critical code |
| 100% | Complete coverage (edge cases included) |

## What Gets Tested

- **Exported Functions**: All public functions
- **Classes**: Constructor, public methods
- **Edge Cases**: Null, undefined, empty, boundary values
- **Error Scenarios**: Exception handling, validation errors
- **Async Code**: Promise resolution/rejection

## Test Structure (TypeScript/Jest)

```typescript
describe('FunctionName', () => {
  beforeEach(() => {
    // Setup
  });

  it('should handle normal input', () => {
    // Arrange
    // Act
    // Assert
  });

  it('should handle edge case', () => {
    // Test edge case
  });

  it('should throw error for invalid input', () => {
    expect(() => fn(invalid)).toThrow();
  });
});
```

## Example

```
/write-tests src/utils/validator.ts 90
```

**Output:**
```
Generating tests for src/utils/validator.ts
Target coverage: 90%

Analyzing functions:
- validateEmail() - 3 test cases
- validatePassword() - 5 test cases
- validateUsername() - 4 test cases

Generated: src/utils/validator.test.ts

Test Summary:
- 12 test cases generated
- Estimated coverage: 92%

Run tests with: npm run test src/utils/validator.test.ts
```

## Test Patterns

The skill follows testing patterns from your project:

- **Jest** for JavaScript/TypeScript
- **Pytest** for Python
- Uses existing mock factories if available
- Follows AAA pattern (Arrange, Act, Assert)

## Next Command

After generating tests, run them with your test runner:
- `npm run test` for Jest
- `pytest` for Python
