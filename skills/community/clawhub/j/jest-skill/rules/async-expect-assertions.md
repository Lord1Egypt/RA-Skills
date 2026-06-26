---
title: Use expect.assertions(n) to verify async assertions ran
impact: CRITICAL
description: expect.assertions(n) ensures exactly n assertions execute, catching tests that silently skip assertions in async code paths.
tags: async, expect.assertions, expect.hasAssertions, guard, false-positive
---

# Use expect.assertions(n) to verify async assertions ran

## Problem

Async tests can silently pass with zero assertions if a promise is not awaited, a `.catch` branch is never entered, or a conditional code path is skipped. `expect.assertions(n)` acts as a safety net — if the test completes with fewer than `n` assertions, it fails.

## Incorrect

```javascript
// BUG: If fetchUser resolves instead of rejecting, the catch block never runs
// and the test passes with 0 assertions
test('handles fetch error', async () => {
  try {
    await fetchUser(-1);
  } catch (error) {
    expect(error.message).toMatch('not found');
  }
});
```

## Correct

```javascript
test('handles fetch error', async () => {
  expect.assertions(1); // fails if the catch block is skipped
  try {
    await fetchUser(-1);
  } catch (error) {
    expect(error.message).toMatch('not found');
  }
});
```

```javascript
// Alternative: use .rejects instead of try/catch
test('handles fetch error', async () => {
  await expect(fetchUser(-1)).rejects.toThrow('not found');
});
```

## When to Use

| Scenario | Recommendation |
|---|---|
| try/catch around async code | Always use `expect.assertions(n)` |
| `.then()` / `.catch()` chains | Always use `expect.assertions(n)` |
| Conditional `expect` calls | Always use `expect.assertions(n)` |
| Linear async/await (no branching) | `expect.hasAssertions()` is sufficient |
| Synchronous tests | Not needed |

## Why

- `expect.assertions(n)` verifies the **exact** count of assertions that ran.
- `expect.hasAssertions()` is a weaker check — it only verifies that **at least one** assertion ran. Use it when you cannot predict the exact count.
- Both must be called at the top of the test body, before any async operations.

```javascript
// expect.hasAssertions example — useful when iterating over dynamic data
test('all items are valid', async () => {
  expect.hasAssertions();
  const items = await getItems();
  items.forEach(item => {
    expect(item.id).toBeDefined();
  });
});
```
