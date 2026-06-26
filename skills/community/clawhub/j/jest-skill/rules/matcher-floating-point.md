---
title: Use toBeCloseTo for floats, never toBe
impact: HIGH
description: Floating-point arithmetic produces rounding errors. toBe fails on values like 0.1 + 0.2; use toBeCloseTo instead.
tags: matcher, toBeCloseTo, floating-point, precision, toBe
---

# Use toBeCloseTo for floats, never toBe

## Problem

IEEE 754 floating-point arithmetic means `0.1 + 0.2 === 0.30000000000000004`, not `0.3`. Using `toBe` or `toEqual` for float comparisons causes tests to fail unpredictably on values that are mathematically equal but differ by a tiny rounding error.

## Incorrect

```javascript
// BUG: 0.1 + 0.2 = 0.30000000000000004, not 0.3
test('calculates total', () => {
  expect(0.1 + 0.2).toBe(0.3); // FAILS
});

test('calculates tax', () => {
  expect(calculateTax(100, 0.07)).toEqual(7.0); // May fail on edge cases
});
```

## Correct

```javascript
test('calculates total', () => {
  expect(0.1 + 0.2).toBeCloseTo(0.3); // PASSES — default precision is 5
});

test('calculates tax', () => {
  expect(calculateTax(100, 0.07)).toBeCloseTo(7.0, 2); // 2 decimal places
});
```

## Why

`toBeCloseTo(expected, precision)` checks that `|received - expected| < 10^(-precision) / 2`. The default precision is `5`, meaning differences smaller than `0.000005` are considered equal.

| Precision | Tolerance | Use case |
|---|---|---|
| 0 | 0.5 | Rough estimates |
| 2 | 0.005 | Currency (2 decimal places) |
| 5 | 0.000005 | General floating-point (default) |
| 10 | 5e-11 | Scientific computation |

**When to use `toBe` with numbers**: Only for integers or values you know are exact (e.g., array `.length`, counter increments, enum values).
