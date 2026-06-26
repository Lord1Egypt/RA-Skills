---
title: Use doNotFake to leave specific APIs real
impact: MEDIUM
description: jest.useFakeTimers fakes all timer APIs by default. Use the doNotFake option to keep specific APIs (like Date, performance, queueMicrotask) real.
tags: timer, useFakeTimers, doNotFake, Date, performance, selective
---

# Use doNotFake to leave specific APIs real

## Problem

`jest.useFakeTimers()` replaces all timer-related globals by default: `setTimeout`, `setInterval`, `setImmediate`, `clearTimeout`, `clearInterval`, `clearImmediate`, `Date`, `performance`, and `queueMicrotask`. This can break libraries that rely on real `Date.now()` or `performance.now()` for non-timer purposes (e.g., logging, UUID generation, cache TTL calculations).

## Incorrect

```javascript
// BUG: Date is faked — uuid library that uses Date.now() returns the same ID every time
test('creates unique records', () => {
  jest.useFakeTimers();
  const a = createRecord(); // uses uuid internally
  const b = createRecord();
  expect(a.id).not.toBe(b.id); // FAILS — Date.now() is frozen
});
```

## Correct

```javascript
test('creates unique records', () => {
  jest.useFakeTimers({ doNotFake: ['Date'] });
  const a = createRecord();
  const b = createRecord();
  expect(a.id).not.toBe(b.id); // PASSES — Date is real
});
```

```javascript
// Keep multiple APIs real
test('measures performance', () => {
  jest.useFakeTimers({
    doNotFake: ['Date', 'performance', 'queueMicrotask'],
  });
  // setTimeout and setInterval are fake
  // Date, performance.now(), and queueMicrotask are real
});
```

## Fakeable APIs

All APIs that `useFakeTimers` can fake:

| API | Default faked | Common reason to keep real |
|---|---|---|
| `setTimeout` | Yes | Rarely |
| `setInterval` | Yes | Rarely |
| `setImmediate` | Yes | Rarely |
| `clearTimeout` | Yes | Rarely |
| `clearInterval` | Yes | Rarely |
| `clearImmediate` | Yes | Rarely |
| `Date` | Yes | UUID generation, logging, cache TTL |
| `performance` | Yes | Benchmarking, metrics libraries |
| `queueMicrotask` | Yes | Promise-based code, React rendering |

## Why

Faking everything by default is Jest's safest option for deterministic tests, but it can cause surprising failures in code that reads the clock for non-scheduling purposes. The `doNotFake` option gives you surgical control.

You can also set a fixed fake time for `Date`:

```javascript
jest.useFakeTimers({ now: new Date('2024-01-01T00:00:00Z') });
expect(Date.now()).toBe(1704067200000); // frozen at Jan 1, 2024
```
