---
title: __mocks__ directory conventions
impact: MEDIUM
description: Manual mocks in __mocks__ follow specific directory placement rules. Misplacing the mock file causes Jest to silently ignore it.
tags: module, manual-mock, __mocks__, directory, conventions
---

# __mocks__ directory conventions

## Problem

Jest looks for manual mocks in `__mocks__` directories, but the placement rules differ for user modules vs node_modules. Placing the mock in the wrong directory means Jest silently uses the real module, and the mock never activates.

## Incorrect

```
# BUG: Manual mock for node_module placed next to the test file — Jest ignores it
src/
├── __mocks__/
│   └── axios.js        ← WRONG: node_module mocks must be adjacent to node_modules
├── utils/
│   ├── __mocks__/
│   │   └── helpers.js   ← Correct for user module
│   └── helpers.js
└── app.test.js
```

## Correct

```
# Correct directory structure
project-root/
├── __mocks__/             ← node_module mocks go here (adjacent to node_modules)
│   └── axios.js
├── node_modules/
│   └── axios/
├── src/
│   ├── utils/
│   │   ├── __mocks__/     ← user module mocks go next to the real module
│   │   │   └── helpers.js
│   │   └── helpers.js
│   └── app.test.js
```

## Rules

| Module type | Mock location | Auto-mocked? |
|---|---|---|
| **User module** (`./utils/helpers`) | `./utils/__mocks__/helpers.js` | No — must call `jest.mock('./utils/helpers')` |
| **Node module** (`axios`) | `<rootDir>/__mocks__/axios.js` | Yes — auto-used without `jest.mock('axios')` |
| **Scoped package** (`@scope/pkg`) | `__mocks__/@scope/pkg.js` | Yes — auto-used |

## Manual Mock File Content

```javascript
// __mocks__/axios.js — manual mock for node_module
const axios = {
  get: jest.fn(() => Promise.resolve({ data: {} })),
  post: jest.fn(() => Promise.resolve({ data: {} })),
  create: jest.fn(function () { return this; }),
};

module.exports = axios;
```

```javascript
// src/utils/__mocks__/helpers.js — manual mock for user module
const helpers = jest.createMockFromModule('../helpers');

// Override specific functions
helpers.formatDate = jest.fn(() => '2024-01-01');

module.exports = helpers;
```

## Why

- **Node module mocks auto-activate** because node_modules are external dependencies you almost always want to control in tests.
- **User module mocks require explicit `jest.mock()`** because you usually want the real implementation and only mock selectively.
- `jest.createMockFromModule()` auto-generates mocks for all exports, which you can then override selectively. This is safer than writing the entire mock by hand because it stays in sync with the real module's export shape.
