---
title: jest.isolateModules for per-test module state
impact: MEDIUM
description: jest.isolateModules creates a sandboxed module registry so each test gets a fresh module instance without affecting other tests.
tags: perf, isolateModules, module-state, sandbox, require, cache
---

# jest.isolateModules for per-test module state

## Problem

Node.js caches modules after first `require()`. If a module has internal state (counters, caches, singletons), that state persists across tests within the same worker. Using `jest.resetModules()` clears the cache globally, but `jest.isolateModules()` provides a scoped sandbox — cleaner and less likely to break unrelated imports.

## Incorrect

```javascript
// BUG: Module state leaks between tests
const counter = require('./counter'); // cached after first require

test('starts at zero', () => {
  expect(counter.get()).toBe(0);
  counter.increment();
});

test('still starts at zero', () => {
  expect(counter.get()).toBe(0); // FAILS — counter.get() returns 1
});
```

```javascript
// FRAGILE: resetModules clears ALL cached modules — may break shared setup
beforeEach(() => {
  jest.resetModules(); // clears everything, including mocks set up in beforeAll
});
```

## Correct

```javascript
test('starts at zero', () => {
  jest.isolateModules(() => {
    const counter = require('./counter'); // fresh instance
    expect(counter.get()).toBe(0);
    counter.increment();
    expect(counter.get()).toBe(1);
  });
  // module registry is restored — counter from other tests is unaffected
});

test('also starts at zero', () => {
  jest.isolateModules(() => {
    const counter = require('./counter'); // another fresh instance
    expect(counter.get()).toBe(0); // PASSES
  });
});
```

```javascript
// Combine with doMock for per-test mocks + fresh modules
test('uses mock config', () => {
  jest.isolateModules(() => {
    jest.doMock('./config', () => ({ debug: true }));
    const app = require('./app'); // gets fresh app with mocked config
    expect(app.isDebug()).toBe(true);
  });
});

test('uses different mock config', () => {
  jest.isolateModules(() => {
    jest.doMock('./config', () => ({ debug: false }));
    const app = require('./app'); // fresh app with different config
    expect(app.isDebug()).toBe(false);
  });
});
```

## jest.resetModules vs jest.isolateModules

| Feature | `jest.resetModules()` | `jest.isolateModules(fn)` |
|---|---|---|
| Scope | Global — clears entire registry | Scoped — only affects `require` inside `fn` |
| Side effects | May break `beforeAll` setup | Contained within callback |
| Use with `doMock` | Yes | Yes |
| Restores registry after | No — stays cleared | Yes — restores after callback |

## Why

`jest.isolateModules` is the safer choice when you need fresh module state. It does not clear shared mocks or setup from `beforeAll`, and it automatically restores the registry after the callback. Use it when:

- Testing modules with internal mutable state (singletons, caches, counters).
- Combining with `jest.doMock` for per-test mock configurations.
- Testing environment-dependent initialization (modules that read `process.env` at require time).
