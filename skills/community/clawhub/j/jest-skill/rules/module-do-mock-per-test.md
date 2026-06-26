---
title: jest.doMock + resetModules for per-test mocks
impact: MEDIUM
description: jest.doMock is not hoisted, allowing different mock implementations per test when combined with jest.resetModules and inline require.
tags: module, doMock, resetModules, per-test, require
---

# jest.doMock + resetModules for per-test mocks

## Problem

`jest.mock()` is hoisted and applies file-wide. If different tests need different mock implementations of the same module, `jest.mock()` with `mockReturnValue` per test works for simple cases, but sometimes you need entirely different module shapes or factory functions per test. `jest.doMock()` is not hoisted, so you can call it inside individual tests.

## Incorrect

```javascript
// BUG: jest.mock is hoisted — both tests get the same mock
jest.mock('./config', () => ({ env: 'test' }));

test('uses test config', () => {
  const config = require('./config');
  expect(config.env).toBe('test'); // works
});

test('uses production config', () => {
  // No way to change the jest.mock factory for this test only
  jest.mock('./config', () => ({ env: 'production' })); // this second jest.mock is ignored
  const config = require('./config');
  expect(config.env).toBe('production'); // FAILS — still 'test'
});
```

## Correct

```javascript
beforeEach(() => {
  jest.resetModules(); // clear the module registry between tests
});

test('uses test config', () => {
  jest.doMock('./config', () => ({ env: 'test' }));
  const config = require('./config'); // fresh require after doMock
  expect(config.env).toBe('test');
});

test('uses production config', () => {
  jest.doMock('./config', () => ({ env: 'production' }));
  const config = require('./config'); // gets the production mock
  expect(config.env).toBe('production');
});
```

## jest.mock vs jest.doMock

| Feature | `jest.mock()` | `jest.doMock()` |
|---|---|---|
| Hoisted | Yes | No |
| Scope | Entire file | From call site onward |
| Per-test mocks | No (one factory per file) | Yes |
| Requires `resetModules` | No | Yes (to clear cached modules) |
| Has `jest.dontMock()` | `jest.unmock()` | `jest.dontMock()` |

## Why

- `jest.resetModules()` clears the module registry so the next `require()` loads a fresh copy.
- `jest.doMock()` registers the mock without hoisting, so it only affects `require()` calls after it.
- This pattern is useful for testing configuration-dependent behavior, environment-specific code, or feature flags where each test needs a different module state.

```javascript
// Also works with jest.isolateModules for scoped require
test('isolated module', () => {
  jest.isolateModules(() => {
    jest.doMock('./config', () => ({ env: 'staging' }));
    const config = require('./config');
    expect(config.env).toBe('staging');
  });
  // module registry is restored here
});
```
