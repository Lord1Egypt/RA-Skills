---
title: jest.mock factory cannot reference outer variables
impact: CRITICAL
description: Jest hoists jest.mock() calls above imports, so factory functions cannot reference variables declared in the module scope.
tags: mock, hoisting, factory, jest.mock, scope
---

# jest.mock factory cannot reference outer variables

## Problem

Jest automatically hoists `jest.mock()` calls to the top of the file, before any `import` or `require` statements. This means the factory function runs before any module-scoped variables are initialized. Referencing them causes `ReferenceError` or silently uses `undefined`.

## Incorrect

```javascript
// BUG: mockUser is not initialized when jest.mock runs (hoisted above this line)
const mockUser = { id: 1, name: 'Alice' };

jest.mock('./userService', () => ({
  getUser: jest.fn(() => mockUser), // ReferenceError: mockUser is not defined
}));
```

## Correct

```javascript
// Option 1: Inline the value inside the factory
jest.mock('./userService', () => ({
  getUser: jest.fn(() => ({ id: 1, name: 'Alice' })),
}));
```

```javascript
// Option 2: Use a variable prefixed with `mock` — Jest's special exception
const mockUser = { id: 1, name: 'Alice' };

jest.mock('./userService', () => ({
  getUser: jest.fn(() => mockUser),
}));
// Works because Jest allows variables starting with `mock` to be referenced in factories.
// The variable must be declared with `const`, `let`, or `var` — not a function call result.
```

```javascript
// Option 3: Set the return value inside each test instead
jest.mock('./userService');
const { getUser } = require('./userService');

test('returns user', () => {
  getUser.mockReturnValue({ id: 1, name: 'Alice' });
  // ...
});
```

## Why

The `mock` prefix exception exists specifically for this hoisting issue. Jest's Babel plugin detects variables starting with `mock` and allows them in the hoisted scope. However, this is fragile:

- The variable must be a simple declaration, not a function call like `const mockUser = createUser()`.
- Misspelling the prefix (e.g., `mocked`, `my_mock`) breaks the exception.
- The variable is still uninitialized if it depends on other imports.

**Safest approach**: Define the mock return value inside individual tests using `mockReturnValue` or `mockImplementation`, not in the factory.
