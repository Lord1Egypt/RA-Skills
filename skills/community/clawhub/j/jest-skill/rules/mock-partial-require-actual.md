---
title: Use jest.requireActual for partial module mocking
impact: CRITICAL
description: When mocking only some exports of a module, spread jest.requireActual to preserve the real implementations of the rest.
tags: mock, requireActual, partial, jest.mock, spread
---

# Use jest.requireActual for partial module mocking

## Problem

When you `jest.mock()` a module, all of its exports become `undefined` (auto-mock) or whatever the factory returns. If you only want to mock one function and keep the rest real, you must explicitly spread `jest.requireActual`. Forgetting this causes the real exports to be missing, leading to `TypeError: X is not a function`.

## Incorrect

```javascript
// BUG: Only `fetchUser` is defined — all other exports from './api' are undefined
jest.mock('./api', () => ({
  fetchUser: jest.fn(),
}));

const { fetchUser, fetchPosts } = require('./api');

test('fetch posts still works', () => {
  fetchPosts(); // TypeError: fetchPosts is not a function
});
```

## Correct

```javascript
jest.mock('./api', () => ({
  ...jest.requireActual('./api'),
  fetchUser: jest.fn(), // only this export is mocked
}));

const { fetchUser, fetchPosts } = require('./api');

test('fetchUser is mocked', () => {
  fetchUser.mockReturnValue({ id: 1 });
  expect(fetchUser()).toEqual({ id: 1 });
});

test('fetchPosts is real', () => {
  // fetchPosts uses its actual implementation
  expect(typeof fetchPosts).toBe('function');
});
```

## Why

- `jest.requireActual` bypasses the mock registry and loads the real module.
- Spreading it into the factory object gives you all real exports as a baseline.
- You then override only the exports you want to control.

This pattern is essential for large modules where mocking everything would be impractical and fragile. It also makes tests more readable — you can see exactly which exports are faked.

### Common variant: ES module default export

```javascript
jest.mock('./config', () => ({
  __esModule: true,
  ...jest.requireActual('./config'),
  default: { apiUrl: 'http://test.local' },
}));
```

The `__esModule: true` flag is needed so Jest treats the mock as an ES module with a `default` property.
