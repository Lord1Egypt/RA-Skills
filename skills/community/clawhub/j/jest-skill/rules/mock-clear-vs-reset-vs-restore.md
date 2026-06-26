---
title: clearAllMocks vs resetAllMocks vs restoreAllMocks
impact: CRITICAL
description: Understand the difference between clearing, resetting, and restoring mocks to avoid stale state leaking between tests.
tags: mock, clearAllMocks, resetAllMocks, restoreAllMocks, isolation
---

# clearAllMocks vs resetAllMocks vs restoreAllMocks

## Problem

Jest provides three mock-cleanup functions that sound similar but do very different things. Using `clearAllMocks` when you need `restoreAllMocks` leaves mock implementations in place, causing later tests to silently use stale fakes. Using `resetAllMocks` destroys custom implementations you intended to keep.

## Incorrect

```javascript
// BUG: clearAllMocks only clears call history — the mock implementation stays
afterEach(() => {
  jest.clearAllMocks();
});

test('first', () => {
  jest.spyOn(Math, 'random').mockReturnValue(0.5);
  expect(Math.random()).toBe(0.5);
});

test('second', () => {
  // Math.random is STILL mocked — returns 0.5, not a real random number
  expect(Math.random()).not.toBe(0.5); // FAILS
});
```

## Correct

```javascript
afterEach(() => {
  jest.restoreAllMocks();
});

test('first', () => {
  jest.spyOn(Math, 'random').mockReturnValue(0.5);
  expect(Math.random()).toBe(0.5);
});

test('second', () => {
  // Math.random is restored to the real implementation
  expect(typeof Math.random()).toBe('number'); // PASSES
});
```

## Decision Table

| Function | Clears calls/instances | Removes mock implementation | Restores original |
|---|---|---|---|
| `clearAllMocks` | Yes | No | No |
| `resetAllMocks` | Yes | Yes (resets to `jest.fn()`) | No |
| `restoreAllMocks` | Yes | Yes | Yes |

## Why

- **clearAllMocks**: Use between tests when you want to keep the mock implementation but reset counters (e.g., checking `toHaveBeenCalledTimes` per test).
- **resetAllMocks**: Use when you want every test to set up its own mock implementation from scratch. Mocks become no-op `jest.fn()`.
- **restoreAllMocks**: Use when you used `jest.spyOn` and want the original implementation back. This is the safest default for `afterEach`.

Prefer setting `restoreMocks: true` in `jest.config` so you never forget:

```javascript
// jest.config.js
module.exports = {
  restoreMocks: true,
};
```
