---
name: jest-config-validator
description: Validate jest.config.ts/js/json and Jest configuration in package.json for deprecated options, transform conflicts, and best practices. Use when validating Jest test runner configs, auditing test setups, migrating Jest versions, or linting jest.config files.
---

# Jest Config Validator

Validate `jest.config.ts`, `jest.config.js`, `jest.config.json`, and `package.json#jest` for deprecated options, transform conflicts, coverage misconfigurations, and best practices. Supports text, JSON, and summary output formats with CI-friendly exit codes.

## Commands

```bash
# Full validation (all 22+ rules)
python3 scripts/jest_config_validator.py validate jest.config.js

# Quick syntax-only check (structure rules only)
python3 scripts/jest_config_validator.py check jest.config.ts

# Explain config in human-readable form
python3 scripts/jest_config_validator.py explain jest.config.json

# Suggest improvements
python3 scripts/jest_config_validator.py suggest package.json

# JSON output (CI-friendly)
python3 scripts/jest_config_validator.py validate jest.config.js --format json

# Summary only (pass/fail + counts)
python3 scripts/jest_config_validator.py validate jest.config.js --format summary

# Strict mode (warnings become errors)
python3 scripts/jest_config_validator.py validate jest.config.js --strict
```

## Rules (22+)

| # | Category | Severity | Rule |
|---|----------|----------|------|
| S1 | Structure | Error | File not found or unreadable |
| S2 | Structure | Error | Empty config or missing module.exports/export default |
| S3 | Structure | Warning | Both jest.config and package.json#jest present (conflict) |
| S4 | Structure | Warning | Unknown top-level config keys detected |
| S5 | Structure | Error | Invalid JSON syntax (for .json configs) |
| T1 | Test Environment | Error | Invalid testEnvironment value |
| T2 | Test Environment | Warning | testEnvironment: jsdom without jest-environment-jsdom (Jest 28+) |
| T3 | Test Environment | Warning | testURL deprecated in Jest 28+ (use testEnvironmentOptions) |
| T4 | Test Environment | Warning | Empty testMatch or testPathPattern |
| X1 | Transforms | Warning | Overlapping transform patterns (conflict) |
| X2 | Transforms | Warning | ts-jest and babel-jest used together without clear separation |
| X3 | Transforms | Warning | transformIgnorePatterns too broad (may skip needed transforms) |
| X4 | Transforms | Warning | Missing transform for .tsx/.jsx when React detected |
| V1 | Coverage | Warning | collectCoverageFrom empty or too broad |
| V2 | Coverage | Warning | coverageThreshold set but collectCoverage not enabled |
| V3 | Coverage | Warning | Deprecated coverageReporters values |
| D1 | Deprecated | Warning | Deprecated Jest options detected |
| D2 | Deprecated | Warning | jest.fn() used inside config file (configs should not mock) |
| D3 | Deprecated | Warning | timers: 'fake' (old syntax, use fakeTimers object) |
| B1 | Best Practices | Info | No clearMocks/resetMocks/restoreMocks set |
| B2 | Best Practices | Warning | roots pointing outside project directory |
| B3 | Best Practices | Warning | setupFiles/setupFilesAfterFramework path pattern issues |
| B4 | Best Practices | Info | moduleNameMapper with complex regex missing comment |
| B5 | Best Practices | Warning | preset and manual config overlap |
| B6 | Best Practices | Warning | maxWorkers set to 1 in non-CI context |

## Output Formats

**text** (default): Human-readable with file path, rule code, severity, and message per finding.

**json**: Machine-readable JSON with `file`, `summary`, and `findings` array. Each finding has `rule`, `severity`, `message`, and `line` fields.

**summary**: One-line pass/fail with error/warning/info counts. Ideal for CI output gates.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No errors found (warnings/info may exist) |
| 1 | One or more errors found |
| 2 | File not found or parse error |
