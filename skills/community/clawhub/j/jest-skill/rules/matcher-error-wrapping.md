---
title: Wrap throwing code in arrow function for toThrow
impact: HIGH
description: Passing a function call directly to expect() executes it immediately, throwing before toThrow can catch it. Wrap it in an arrow function.
tags: matcher, toThrow, arrow-function, error, exception
---

# Wrap throwing code in arrow function for toThrow

## Problem

`expect(fn).toThrow()` requires a function reference, not a function call. If you call the function inside `expect()`, it throws immediately, and Jest sees an unhandled exception instead of a caught assertion.

## Incorrect

```javascript
// BUG: validateAge(-1) executes immediately — throws before toThrow can catch it
test('rejects negative age', () => {
  expect(validateAge(-1)).toThrow('Age must be positive'); // UNCAUGHT ERROR
});
```

```javascript
// BUG: Same problem with async — rejects before .rejects can catch it
test('rejects invalid input', async () => {
  expect(fetchUser(null)).rejects.toThrow(); // UNCAUGHT REJECTION
});
```

## Correct

```javascript
// Wrap in arrow function
test('rejects negative age', () => {
  expect(() => validateAge(-1)).toThrow('Age must be positive');
});
```

```javascript
// For async: await + .rejects — do NOT wrap in arrow function
test('rejects invalid input', async () => {
  await expect(fetchUser(null)).rejects.toThrow('Invalid input');
});
```

```javascript
// Checking error type and message
test('throws TypeError', () => {
  expect(() => validateAge('abc')).toThrow(TypeError);
  expect(() => validateAge('abc')).toThrow('must be a number');
  expect(() => validateAge('abc')).toThrow(/must be a \w+/);
});
```

## Why

The key distinction:

| Pattern | What happens |
|---|---|
| `expect(fn())` | `fn()` executes, return value is passed to `expect` |
| `expect(() => fn())` | Arrow function is passed to `expect`, which calls it inside a try/catch |
| `expect(asyncFn())` | Promise is passed to `expect` — use with `.resolves`/`.rejects` |

- **Sync errors**: Always wrap in `() =>`.
- **Async errors (rejected promises)**: Pass the promise directly (do not wrap in arrow function), use `.rejects`, and `await` the whole expression.
