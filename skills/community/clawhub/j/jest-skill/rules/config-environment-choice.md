---
title: Per-file @jest-environment docblock over global jsdom
impact: MEDIUM
description: Setting jsdom globally slows down Node-only tests and hides environment bugs. Use per-file @jest-environment docblocks to match each test file's actual needs.
tags: config, environment, jsdom, node, docblock, testEnvironment
---

# Per-file @jest-environment docblock over global jsdom

## Problem

Setting `testEnvironment: 'jsdom'` globally means every test file — including pure Node.js logic like API handlers, database queries, and utility functions — loads a full browser DOM simulation. This adds unnecessary overhead and can mask bugs where code accidentally depends on browser globals.

## Incorrect

```javascript
// jest.config.js — forces jsdom for all tests
module.exports = {
  testEnvironment: 'jsdom',
};

// src/utils/math.test.js — pure Node logic, doesn't need DOM
test('adds numbers', () => {
  expect(add(1, 2)).toBe(3); // works, but jsdom is loaded unnecessarily
  expect(typeof window).toBe('object'); // true — window exists, hiding a potential bug
});
```

## Correct

```javascript
// jest.config.js — default to node (faster, no DOM overhead)
module.exports = {
  testEnvironment: 'node',
};
```

```javascript
// src/components/Button.test.js — needs DOM, opt in with docblock
/**
 * @jest-environment jsdom
 */
import { render } from '@testing-library/react';
import { Button } from './Button';

test('renders button text', () => {
  const { getByText } = render(<Button>Click me</Button>);
  expect(getByText('Click me')).toBeInTheDocument();
});
```

```javascript
// src/utils/math.test.js — no docblock needed, uses default 'node'
test('adds numbers', () => {
  expect(add(1, 2)).toBe(3);
  expect(typeof window).toBe('undefined'); // correct — no DOM in Node
});
```

## Configuration Options

| Environment | Use for | Globals available |
|---|---|---|
| `node` (default) | API routes, CLI tools, utilities, DB logic | `process`, `Buffer`, Node APIs |
| `jsdom` | React/Vue/DOM components, browser code | `window`, `document`, `navigator` |
| `@jest-environment-jsdom-global` | Tests that need to modify jsdom options | Configurable jsdom |

## Why

- **Performance**: `jsdom` startup adds ~100ms per test file. In a large project with 500 test files where only 100 need DOM, that is 40 seconds of unnecessary overhead.
- **Correctness**: Code that accidentally uses `window` or `document` should fail fast in a `node` environment rather than silently working under `jsdom`.
- **Clarity**: The `@jest-environment` docblock at the top of a file documents its runtime requirements.

You can also set environment options:

```javascript
/**
 * @jest-environment jsdom
 * @jest-environment-options {"url": "https://example.com"}
 */
```
