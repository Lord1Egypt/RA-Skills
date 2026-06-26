---
name: test-coverage-report
description: Analyze test coverage gaps by comparing test files against source modules to identify untested code paths and critical functions.
version: 0.3.0
displayName: Test Coverage Report
metadata:
  openclaw:
    author: xd-test
    consumers:
      - name: xdclaw
        minVersion: 1.2.0
    permissions:
      filesystem:
        - read
      network: false
      shell: true
---

# Test Coverage Report

Identify test coverage gaps by analyzing the relationship between source modules and their corresponding test files.

## Analysis Steps

- Map each source file to its test file(s) using naming conventions (`.test.ts`, `.spec.ts`, `__tests__/`).
- Identify source files with no corresponding test file.
- For files with tests, check which exported functions and classes have test coverage.
- Prioritize coverage gaps by risk: public API surface, error handling paths, and data mutation functions.
- Check for test files that import from modules that no longer exist (orphaned tests).

## Risk Scoring

- Critical: Public API handlers with no test coverage.
- High: Data mutation functions (create, update, delete) without tests.
- Medium: Utility functions used by multiple modules without tests.
- Low: Internal helper functions with single callers.

## Output

Provide a coverage gap report sorted by risk level. For each gap, show the source file, the untested exports, and a suggested test outline.

