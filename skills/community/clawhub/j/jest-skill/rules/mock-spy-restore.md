---
title: Always restore jest.spyOn; prefer restoreMocks config
impact: CRITICAL
description: Spies replace real implementations and must be restored after each test to prevent cross-test contamination.
tags: mock, spyOn, restore, restoreMocks, afterEach
---

# Always restore jest.spyOn; prefer restoreMocks config

## Problem

`jest.spyOn` replaces a method on an existing object with a mock. If you forget to restore it, every subsequent test in the file sees the mocked version. This causes mysterious failures when tests run in a different order or when a new test is added.

## Incorrect

```javascript
// BUG: spy is never restored — console.error is mocked for all remaining tests
test('suppresses error output', () => {
  jest.spyOn(console, 'error').mockImplementation(() => {});
  doSomethingThatLogs();
  expect(console.error).toHaveBeenCalled();
});

test('later test', () => {
  // console.error is still mocked — real errors are silently swallowed
  triggerRealError(); // no output, bug hidden
});
```

## Correct

```javascript
// Option 1: Manual restore
afterEach(() => {
  jest.restoreAllMocks();
});

test('suppresses error output', () => {
  jest.spyOn(console, 'error').mockImplementation(() => {});
  doSomethingThatLogs();
  expect(console.error).toHaveBeenCalled();
});

test('later test', () => {
  // console.error is real again
  triggerRealError(); // errors print normally
});
```

```javascript
// Option 2: Config-level (preferred)
// jest.config.js
module.exports = {
  restoreMocks: true,
};
```

## Why

Setting `restoreMocks: true` in config is the safest approach because:

1. It applies globally — no test file can forget.
2. It restores the original implementation, not just a no-op `jest.fn()`.
3. It covers `jest.spyOn`, `jest.fn` used as replacements, and `jest.replaceProperty`.

If you only need the spy for a single assertion, use the spy's own `.mockRestore()`:

```javascript
test('one-off spy', () => {
  const spy = jest.spyOn(fs, 'readFileSync').mockReturnValue('data');
  expect(readConfig()).toBe('data');
  spy.mockRestore(); // restored immediately
});
```
