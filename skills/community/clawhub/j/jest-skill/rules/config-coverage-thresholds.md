---
title: Set per-directory coverage thresholds
impact: MEDIUM
description: Global coverage thresholds are too coarse — high coverage in one area masks low coverage in critical code. Use per-directory thresholds for meaningful enforcement.
tags: config, coverage, threshold, coverageThreshold, per-directory
---

# Set per-directory coverage thresholds

## Problem

A single global coverage threshold (e.g., 80% lines) averages coverage across the entire codebase. Well-tested utility code can mask untested critical business logic. Per-directory thresholds let you enforce higher standards where it matters most.

## Incorrect

```javascript
// jest.config.js — single global threshold
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
// Problem: src/utils/ has 98% coverage, src/payments/ has 40%
// Average is above 80%, so CI passes — but payment logic is barely tested
```

## Correct

```javascript
// jest.config.js — per-directory thresholds
module.exports = {
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
    './src/payments/': {
      branches: 90,
      functions: 95,
      lines: 95,
      statements: 95,
    },
    './src/auth/': {
      branches: 85,
      functions: 90,
      lines: 90,
      statements: 90,
    },
    './src/utils/': {
      branches: 60,
      functions: 60,
      lines: 60,
      statements: 60,
    },
  },
};
```

## Threshold Types

| Metric | What it measures | Hardest to game |
|---|---|---|
| `statements` | Individual statements executed | Easiest |
| `lines` | Source lines executed | Easy |
| `functions` | Functions called at least once | Medium |
| `branches` | if/else/switch branches taken | Hardest — best quality signal |

## Why

- **Critical code** (payments, auth, data validation) should have the highest thresholds.
- **Utility code** can have moderate thresholds — it's usually well-tested by nature.
- **Generated or third-party code** can have lower thresholds or be excluded via `coveragePathIgnorePatterns`.
- `branches` is the most meaningful metric — it catches untested error paths, edge cases, and conditional logic.

You can also set thresholds per file using glob patterns:

```javascript
coverageThreshold: {
  './src/payments/**/*.ts': {
    branches: 90,
    lines: 95,
  },
}
```
