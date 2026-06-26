---
title: beforeEach/afterEach are scoped to describe blocks
impact: HIGH
description: Setup and teardown hooks run for every test inside their describe block, including nested describes. Misunderstanding scope causes redundant setup or missing teardown.
tags: structure, beforeEach, afterEach, describe, scope, hooks
---

# beforeEach/afterEach are scoped to describe blocks

## Problem

Hooks declared inside a `describe` block only run for tests within that block (and its nested blocks). Hooks declared at the top level run for every test in the file. Misplacing hooks leads to either unnecessary setup for unrelated tests or missing setup for tests that need it.

## Incorrect

```javascript
// BUG: database cleanup runs for ALL tests, including 'math' tests that don't need it
beforeEach(() => {
  db.clear(); // runs before every test in the file
});

describe('user service', () => {
  test('creates user', async () => {
    await createUser({ name: 'Alice' });
    expect(await getUsers()).toHaveLength(1);
  });
});

describe('math utils', () => {
  test('adds numbers', () => {
    expect(add(1, 2)).toBe(3); // db.clear() ran unnecessarily
  });
});
```

## Correct

```javascript
describe('user service', () => {
  beforeEach(() => {
    db.clear(); // only runs before tests in this describe block
  });

  test('creates user', async () => {
    await createUser({ name: 'Alice' });
    expect(await getUsers()).toHaveLength(1);
  });
});

describe('math utils', () => {
  test('adds numbers', () => {
    expect(add(1, 2)).toBe(3); // no unnecessary db.clear()
  });
});
```

## Execution Order

```javascript
beforeAll(() => console.log('1 - beforeAll'));        // file-level
beforeEach(() => console.log('2 - top beforeEach'));

describe('group', () => {
  beforeEach(() => console.log('3 - group beforeEach'));
  afterEach(() => console.log('4 - group afterEach'));

  test('test', () => console.log('5 - test'));
});

afterEach(() => console.log('6 - top afterEach'));
afterAll(() => console.log('7 - afterAll'));

// Output: 1, 2, 3, 5, 4, 6, 7
```

## Why

- Top-level hooks affect every test — use them only for truly global setup (e.g., jest config, global mocks).
- Scoped hooks keep unrelated test groups independent.
- Nested describes inherit parent hooks: a test inside a nested describe runs both the parent's and its own `beforeEach`.
- `afterEach` runs in reverse order: innermost first, then outer.
