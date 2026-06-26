---
title: Mock non-deterministic values for stable snapshots
impact: MEDIUM
description: Date.now(), Math.random(), UUIDs, and other non-deterministic values must be mocked or replaced to produce reproducible snapshots.
tags: snapshot, deterministic, Date, random, uuid, mock
---

# Mock non-deterministic values for stable snapshots

## Problem

Snapshots that include non-deterministic values (current time, random numbers, generated IDs) produce different output on every run. The snapshot fails, developers blindly update it, and the test becomes useless.

## Incorrect

```javascript
// BUG: Date.now() produces a different timestamp every run
test('creates audit log', () => {
  const log = createAuditLog('user.login', { userId: 1 });
  expect(log).toMatchSnapshot();
  // Snapshot includes: timestamp: 1705312200000
  // Next run: timestamp: 1705312201234 — different, fails
});
```

## Correct

```javascript
// Option 1: Mock Date.now
test('creates audit log', () => {
  jest.useFakeTimers({ now: new Date('2024-01-15T12:00:00Z') });
  const log = createAuditLog('user.login', { userId: 1 });
  expect(log).toMatchSnapshot();
  // Snapshot always has: timestamp: 1705320000000
  jest.useRealTimers();
});
```

```javascript
// Option 2: Mock the random/UUID source
test('creates record with id', () => {
  jest.spyOn(crypto, 'randomUUID').mockReturnValue('00000000-0000-0000-0000-000000000001');
  const record = createRecord({ name: 'test' });
  expect(record).toMatchSnapshot();
});
```

```javascript
// Option 3: Use property matchers (see snapshot-property-matchers rule)
test('creates audit log', () => {
  const log = createAuditLog('user.login', { userId: 1 });
  expect(log).toMatchSnapshot({
    timestamp: expect.any(Number),
    id: expect.any(String),
  });
});
```

## Non-Deterministic Sources to Mock

| Source | Mock strategy |
|---|---|
| `Date.now()` / `new Date()` | `jest.useFakeTimers({ now: ... })` |
| `Math.random()` | `jest.spyOn(Math, 'random').mockReturnValue(0.5)` |
| `crypto.randomUUID()` | `jest.spyOn(crypto, 'randomUUID').mockReturnValue(...)` |
| Third-party ID generators | Mock the module: `jest.mock('uuid', ...)` |
| `process.hrtime` | `jest.spyOn(process, 'hrtime').mockReturnValue(...)` |
| File modification times | Use fixed test fixtures |

## Why

Deterministic tests are reproducible — they produce the same result regardless of when, where, or how many times they run. For snapshot tests, this means the snapshot file stays stable in version control, diffs are meaningful, and CI doesn't produce spurious failures.

Choose between mocking the source (options 1–2) and using property matchers (option 3) based on how many dynamic fields exist. If most of the object is dynamic, property matchers are simpler. If only one or two fields are dynamic, mocking the source keeps the snapshot more detailed.
