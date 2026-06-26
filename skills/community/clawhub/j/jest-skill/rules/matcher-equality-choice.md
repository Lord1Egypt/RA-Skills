---
title: toBe vs toEqual vs toStrictEqual
impact: HIGH
description: Choose the right equality matcher — toBe for primitives and references, toEqual for deep value equality, toStrictEqual for deep equality with type checking.
tags: matcher, toBe, toEqual, toStrictEqual, equality, comparison
---

# toBe vs toEqual vs toStrictEqual

## Problem

Using `toBe` on objects compares by reference, not by value. Two objects with the same properties will fail `toBe` because they are different instances. Conversely, `toEqual` ignores `undefined` properties and does not check class instances, which can hide bugs.

## Incorrect

```javascript
// BUG: toBe compares by reference — two different objects with same shape fail
test('returns user', () => {
  const result = getUser();
  expect(result).toBe({ id: 1, name: 'Alice' }); // FAILS — different references
});
```

```javascript
// BUG: toEqual ignores undefined properties — hides missing fields
test('returns config', () => {
  const config = { host: 'localhost', port: undefined };
  expect(config).toEqual({ host: 'localhost' }); // PASSES — but port is present
});
```

## Correct

```javascript
// Use toBe for primitives and reference identity
test('returns count', () => {
  expect(getCount()).toBe(42);
  expect(getName()).toBe('Alice');
  expect(getFlag()).toBe(true);
});

// Use toEqual for deep value comparison
test('returns user object', () => {
  expect(getUser()).toEqual({ id: 1, name: 'Alice' });
});

// Use toStrictEqual for strict deep comparison (recommended default for objects)
test('returns exact config', () => {
  const config = { host: 'localhost', port: undefined };
  expect(config).not.toStrictEqual({ host: 'localhost' }); // FAILS — port is missing
  expect(config).toStrictEqual({ host: 'localhost', port: undefined }); // PASSES
});
```

## Decision Table

| Matcher | Reference check | Deep comparison | Checks undefined props | Checks class type |
|---|---|---|---|---|
| `toBe` | Yes (`Object.is`) | No | N/A | N/A |
| `toEqual` | No | Yes | No (ignores them) | No |
| `toStrictEqual` | No | Yes | Yes | Yes |

## Why

- **`toBe`**: Use for primitives (`number`, `string`, `boolean`, `null`, `undefined`) and when checking the exact same reference (`=== identity`). Uses `Object.is`, so it distinguishes `+0` from `-0` and `NaN` equals `NaN`.
- **`toEqual`**: Use for deep comparison when you don't care about `undefined` fields or class types. Good for comparing plain data.
- **`toStrictEqual`**: Use as your default for object comparison. It catches bugs that `toEqual` misses: extra `undefined` properties, sparse arrays, and class type mismatches.
