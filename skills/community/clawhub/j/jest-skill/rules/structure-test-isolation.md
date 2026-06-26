---
title: Each test must be independent; reset state in beforeEach
impact: HIGH
description: Tests that depend on execution order or shared mutable state create flaky failures. Reset all shared state in beforeEach.
tags: structure, isolation, beforeEach, shared-state, flaky
---

# Each test must be independent; reset state in beforeEach

## Problem

When tests share mutable state (variables, mocks, database records) and rely on a previous test's side effects, they become order-dependent. Running a single test in isolation fails, `--randomize` shuffles the order and breaks them, and adding or removing tests causes cascading failures.

## Incorrect

```javascript
// BUG: tests share `users` array and depend on execution order
const users = [];

test('adds a user', () => {
  users.push({ name: 'Alice' });
  expect(users).toHaveLength(1);
});

test('adds another user', () => {
  users.push({ name: 'Bob' });
  expect(users).toHaveLength(2); // FAILS if run alone — depends on first test
});

test('finds Alice', () => {
  expect(users.find(u => u.name === 'Alice')).toBeDefined(); // FAILS if run alone
});
```

## Correct

```javascript
let users;

beforeEach(() => {
  users = []; // fresh state for every test
});

test('adds a user', () => {
  users.push({ name: 'Alice' });
  expect(users).toHaveLength(1);
});

test('adds another user', () => {
  users.push({ name: 'Bob' });
  expect(users).toHaveLength(1); // correct — starts fresh
});

test('finds user when added', () => {
  users.push({ name: 'Alice' });
  expect(users.find(u => u.name === 'Alice')).toBeDefined();
});
```

## Checklist for Test Isolation

| State type | Reset strategy |
|---|---|
| Module-level variables | Re-initialize in `beforeEach` |
| Mocks | `jest.restoreAllMocks()` in `afterEach` (or `restoreMocks: true` in config) |
| Database/external state | `db.clear()` or transaction rollback in `beforeEach` |
| DOM | `document.body.innerHTML = ''` in `afterEach` or use `jsdom` auto-cleanup |
| Fake timers | `jest.useRealTimers()` in `afterEach` |
| Environment variables | Save and restore in `beforeEach`/`afterEach` |

## Why

- Isolated tests can run in any order, in parallel, and individually (`test.only`).
- `jest --randomize` is a useful tool for detecting order-dependent tests — enable it periodically.
- `beforeEach` is preferred over `beforeAll` for state setup because `beforeAll` creates shared state across tests, which reintroduces the coupling problem.
