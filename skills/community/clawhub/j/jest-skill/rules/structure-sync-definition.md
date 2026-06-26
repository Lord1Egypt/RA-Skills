---
title: Tests must be defined synchronously
impact: HIGH
description: Jest collects test definitions synchronously. Tests defined inside async callbacks, promises, or setTimeout are never registered and silently skipped.
tags: structure, sync, definition, describe, test, registration
---

# Tests must be defined synchronously

## Problem

Jest discovers tests by running the file synchronously and collecting all `test()` and `describe()` calls. If you define tests inside an `async` callback, a `setTimeout`, or a `.then()` handler, Jest finishes collection before those callbacks execute. The tests are never registered and never run — the test file passes with zero tests, which is a silent failure.

## Incorrect

```javascript
// BUG: Tests inside async IIFE are never registered
(async () => {
  const fixtures = await loadFixtures();

  fixtures.forEach(fixture => {
    test(`validates ${fixture.name}`, () => {
      expect(validate(fixture.input)).toBe(fixture.expected);
    });
  });
})();
// Jest output: "Your test suite must contain at least one test."
```

```javascript
// BUG: Tests inside .then() are never registered
fetch('/api/test-cases').then(cases => {
  cases.forEach(c => {
    test(c.name, () => {
      expect(run(c.input)).toBe(c.output);
    });
  });
});
```

## Correct

```javascript
// Option 1: Use synchronous data
const fixtures = [
  { name: 'positive', input: 5, expected: true },
  { name: 'negative', input: -1, expected: false },
  { name: 'zero', input: 0, expected: false },
];

describe.each(fixtures)('validates $name', ({ input, expected }) => {
  test(`returns ${expected}`, () => {
    expect(validate(input)).toBe(expected);
  });
});
```

```javascript
// Option 2: test.each with inline table
test.each([
  [5, true],
  [-1, false],
  [0, false],
])('validate(%i) returns %s', (input, expected) => {
  expect(validate(input)).toBe(expected);
});
```

```javascript
// Option 3: Load fixtures synchronously via require
const fixtures = require('./fixtures.json');

describe.each(fixtures)('$name', ({ input, expected }) => {
  test('validates correctly', () => {
    expect(validate(input)).toBe(expected);
  });
});
```

## Why

Jest's test lifecycle:

1. **Collection phase** (synchronous): Jest `require()`s the test file and records all `describe`, `test`, `beforeEach`, etc.
2. **Execution phase** (can be async): Jest runs collected tests with their hooks.

Any `test()` call that happens after collection (i.e., in an async callback) is too late — Jest has already started executing the tests it found. Use `test.each` or `describe.each` for data-driven tests, and load test data synchronously with `require()` or by inlining it.
