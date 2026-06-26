---
title: Always return/await promises or assertions are skipped
impact: CRITICAL
description: An async test that does not return or await its promise will pass even if the assertion inside would fail.
tags: async, await, promise, return, false-positive
---

# Always return/await promises or assertions are skipped

## Problem

If a test calls an async function but does not `await` or `return` the promise, Jest considers the test synchronous. The test finishes before the promise resolves, so any `expect` inside the `.then()` or after the `await` never runs. The test passes with zero assertions — a silent false positive.

## Incorrect

```javascript
// BUG: Missing `await` — test completes before the promise resolves
test('fetches user', () => {
  fetchUser(1).then(user => {
    expect(user.name).toBe('Alice'); // NEVER EXECUTES
  });
  // test ends here, passes with 0 assertions
});
```

```javascript
// BUG: Missing `return` — same problem with promise chain
test('fetches user', () => {
  // no return statement
  fetchUser(1).then(user => {
    expect(user.name).toBe('Alice'); // NEVER EXECUTES
  });
});
```

## Correct

```javascript
// Option 1: async/await (preferred)
test('fetches user', async () => {
  const user = await fetchUser(1);
  expect(user.name).toBe('Alice');
});
```

```javascript
// Option 2: return the promise
test('fetches user', () => {
  return fetchUser(1).then(user => {
    expect(user.name).toBe('Alice');
  });
});
```

```javascript
// Option 3: .resolves matcher
test('fetches user', async () => {
  await expect(fetchUser(1)).resolves.toEqual({ id: 1, name: 'Alice' });
});
```

## Why

Jest cannot detect that a test has a floating promise. The test runner marks the test as passed because the synchronous body completed without throwing. By the time the promise rejects, the test is already done.

**Pair with `expect.assertions(n)`** to guard against this class of bug:

```javascript
test('fetches user', async () => {
  expect.assertions(1);
  const user = await fetchUser(1);
  expect(user.name).toBe('Alice');
});
```

If you accidentally remove the `await`, `expect.assertions(1)` will fail the test because zero assertions ran.
