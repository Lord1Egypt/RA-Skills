# Jest — Complete Guide

> This document is for AI agents and LLMs to follow when writing, reviewing, or debugging Jest tests. It compiles all rules and references into a single executable guide.

**Baseline:** jest ^29.0.0 / ^30.0.0 with JavaScript or TypeScript

---

## Abstract

Jest is the most widely-used JavaScript testing framework, providing a test runner, assertion library, mock system, and coverage reporter in one package. This guide covers the most impactful patterns and pitfalls: mock lifecycle management (clear vs reset vs restore), async testing traps (floating promises, missing assertion guards), matcher selection (toBe vs toEqual vs toStrictEqual), timer mocking (recursive safety, async timers), module mocking (hoisting, ESM, per-test mocks), snapshot testing (determinism, property matchers), configuration (coverage thresholds, environments, ESM transforms), and CI optimization (workers, sharding). Each rule includes incorrect and correct code examples targeting specific mistakes AI agents commonly make.

---

## Table of Contents

1. [Mock Design](#1-mock-design) — CRITICAL
2. [Async Testing](#2-async-testing) — CRITICAL
3. [Matcher Usage](#3-matcher-usage) — HIGH
4. [Timer Mocking](#4-timer-mocking) — HIGH
5. [Test Structure](#5-test-structure) — HIGH
6. [Module Mocking](#6-module-mocking) — MEDIUM
7. [Snapshot Testing](#7-snapshot-testing) — MEDIUM
8. [Configuration](#8-configuration) — MEDIUM
9. [Performance & CI](#9-performance--ci) — MEDIUM

---

## 1. Mock Design
**Impact: CRITICAL**

### Rule: clearAllMocks vs resetAllMocks vs restoreAllMocks

Jest provides three mock-cleanup functions with very different behaviors. Using the wrong one leaves stale mocks in place.

```javascript
// INCORRECT — clearAllMocks only clears call history, not implementations
afterEach(() => {
  jest.clearAllMocks();
});

test('first', () => {
  jest.spyOn(Math, 'random').mockReturnValue(0.5);
  expect(Math.random()).toBe(0.5);
});

test('second', () => {
  // Math.random is STILL mocked — returns 0.5
  expect(Math.random()).not.toBe(0.5); // FAILS
});

// CORRECT — restoreAllMocks restores original implementations
afterEach(() => {
  jest.restoreAllMocks();
});
```

| Function | Clears calls | Removes implementation | Restores original |
|---|---|---|---|
| `clearAllMocks` | Yes | No | No |
| `resetAllMocks` | Yes | Yes (→ `jest.fn()`) | No |
| `restoreAllMocks` | Yes | Yes | Yes |

Prefer `restoreMocks: true` in `jest.config.js` as the safest default.

### Rule: Always Restore jest.spyOn

`jest.spyOn` replaces a method on an existing object. If not restored, every subsequent test sees the mock.

```javascript
// INCORRECT — spy is never restored
test('suppresses errors', () => {
  jest.spyOn(console, 'error').mockImplementation(() => {});
  doSomething();
  expect(console.error).toHaveBeenCalled();
});
// console.error stays mocked for all remaining tests

// CORRECT
afterEach(() => jest.restoreAllMocks());
// or: jest.config.js → { restoreMocks: true }
```

### Rule: jest.mock Factory Cannot Reference Outer Variables

Jest hoists `jest.mock()` above all imports. Factory functions run before module-scoped variables are initialized.

```javascript
// INCORRECT — mockUser is not initialized when factory runs
const mockUser = { id: 1, name: 'Alice' };
jest.mock('./userService', () => ({
  getUser: jest.fn(() => mockUser), // ReferenceError
}));

// CORRECT — inline the value
jest.mock('./userService', () => ({
  getUser: jest.fn(() => ({ id: 1, name: 'Alice' })),
}));

// CORRECT — use `mock` prefix (Jest's special exception)
const mockUser = { id: 1, name: 'Alice' };
jest.mock('./userService', () => ({
  getUser: jest.fn(() => mockUser), // works with `mock` prefix
}));
```

### Rule: Use jest.requireActual for Partial Module Mocking

When mocking only some exports, spread `jest.requireActual` to keep the rest real.

```javascript
// INCORRECT — all exports except fetchUser are undefined
jest.mock('./api', () => ({
  fetchUser: jest.fn(),
}));

// CORRECT
jest.mock('./api', () => ({
  ...jest.requireActual('./api'),
  fetchUser: jest.fn(),
}));
```

### Rule: What to Mock and What Not to Mock

Mock things that are **external, slow, non-deterministic, or have side effects**. Do not mock things that are **internal, fast, deterministic, and pure**.

```javascript
// MOCK: External boundaries
jest.mock('./api-client');     // HTTP calls
jest.mock('./db');             // Database
jest.useFakeTimers();          // Date/time
jest.spyOn(Math, 'random').mockReturnValue(0.5); // Randomness

// DON'T MOCK: Internal logic
// BAD — mocking a utility you own
jest.mock('./utils/formatCurrency'); // tests nothing real

// BAD — mocking the function under test
jest.spyOn(userService, 'validateAge');
userService.validateAge(25);
expect(userService.validateAge).toHaveBeenCalled(); // tautological
```

**Decision framework**: Draw a line around your unit under test. Mock everything that crosses that line outward (DB, HTTP, filesystem, clock). Don't mock anything inside it (pure functions, mappers, validators, data structures).

```javascript
// BAD: Over-mocked — proves nothing
jest.mock('./userRepository');
jest.mock('./validator');
jest.mock('./mapper');
// All internal logic is mocked away

// GOOD: Only mock the external boundary
jest.mock('./userRepository');
test('creates user with validation', async () => {
  userRepository.save.mockResolvedValue({ id: 1, name: 'Alice' });
  const result = await userService.createUser({ name: 'Alice' });
  // Tests real validation, real mapping, real business logic
  expect(result).toEqual({ id: 1, name: 'Alice' });
});
```

---

## 2. Async Testing
**Impact: CRITICAL**

### Rule: Always Return/Await Promises

If an async test does not `await` or `return` its promise, Jest considers it synchronous. Assertions inside `.then()` never run — the test passes with zero assertions.

```javascript
// INCORRECT — missing await
test('fetches user', () => {
  fetchUser(1).then(user => {
    expect(user.name).toBe('Alice'); // NEVER EXECUTES
  });
});

// CORRECT
test('fetches user', async () => {
  const user = await fetchUser(1);
  expect(user.name).toBe('Alice');
});

// CORRECT — .resolves
test('fetches user', async () => {
  await expect(fetchUser(1)).resolves.toEqual({ id: 1, name: 'Alice' });
});
```

### Rule: Use expect.assertions(n) for Async Guards

`expect.assertions(n)` catches tests that silently skip assertions in async code paths.

```javascript
// INCORRECT — if fetchUser resolves, catch never runs, test passes vacuously
test('handles error', async () => {
  try {
    await fetchUser(-1);
  } catch (error) {
    expect(error.message).toMatch('not found');
  }
});

// CORRECT
test('handles error', async () => {
  expect.assertions(1);
  try {
    await fetchUser(-1);
  } catch (error) {
    expect(error.message).toMatch('not found');
  }
});

// BETTER — use .rejects
test('handles error', async () => {
  await expect(fetchUser(-1)).rejects.toThrow('not found');
});
```

### Rule: Wrap expect in try/catch When Using done Callback

A failing `expect` throws, preventing `done()` from being called. The test times out instead of showing the real error.

```javascript
// INCORRECT — timeout instead of assertion error
test('callback test', (done) => {
  fetchUser(1, (err, user) => {
    expect(user.name).toBe('Alice');
    done();
  });
});

// CORRECT
test('callback test', (done) => {
  fetchUser(1, (err, user) => {
    try {
      expect(user.name).toBe('Alice');
      done();
    } catch (e) {
      done(e);
    }
  });
});
```

Prefer async/await over `done`. Jest 30 deprecates `done`.

---

## 3. Matcher Usage
**Impact: HIGH**

### Rule: toBe vs toEqual vs toStrictEqual

```javascript
// INCORRECT — toBe compares by reference
expect(getUser()).toBe({ name: 'Alice' }); // FAILS

// CORRECT
expect(getUser()).toEqual({ name: 'Alice' });
expect(getUser()).toStrictEqual({ name: 'Alice' }); // stricter: checks undefined props + class
```

| Matcher | Reference check | Deep compare | Checks undefined props | Checks class |
|---|---|---|---|---|
| `toBe` | Yes (`Object.is`) | No | N/A | N/A |
| `toEqual` | No | Yes | No | No |
| `toStrictEqual` | No | Yes | Yes | Yes |

Use `toBe` for primitives, `toStrictEqual` for objects (default choice), `toEqual` when you intentionally ignore `undefined` properties.

### Rule: Use toBeCloseTo for Floats

```javascript
// INCORRECT — 0.1 + 0.2 = 0.30000000000000004
expect(0.1 + 0.2).toBe(0.3); // FAILS

// CORRECT
expect(0.1 + 0.2).toBeCloseTo(0.3);
expect(calculateTax(100, 0.07)).toBeCloseTo(7.0, 2);
```

### Rule: Wrap Throwing Code in Arrow Function for toThrow

```javascript
// INCORRECT — executes immediately
expect(validateAge(-1)).toThrow(); // UNCAUGHT ERROR

// CORRECT — wrap in arrow function
expect(() => validateAge(-1)).toThrow('Age must be positive');

// For async: pass promise directly, use .rejects
await expect(fetchUser(null)).rejects.toThrow('Invalid');
```

---

## 4. Timer Mocking
**Impact: HIGH**

### Rule: Use runOnlyPendingTimers for Recursive Timers

`jest.runAllTimers()` enters an infinite loop when timer callbacks schedule new timers.

```javascript
// INCORRECT — infinite loop
jest.useFakeTimers();
startPolling();
jest.runAllTimers(); // hangs

// CORRECT
jest.runOnlyPendingTimers(); // one cycle at a time
// or
jest.advanceTimersByTime(3000); // precise control
```

### Rule: Use Async Timer Methods When Promises Are Involved

Synchronous timer methods don't flush the microtask queue. When code mixes timers with promises, use async variants.

```javascript
// INCORRECT — promises not flushed
jest.advanceTimersByTime(1000);

// CORRECT (Jest 29.5+)
await jest.advanceTimersByTimeAsync(1000);
await jest.runOnlyPendingTimersAsync();
```

### Rule: Use doNotFake to Leave Specific APIs Real

```javascript
// INCORRECT — Date is faked, uuid library returns same ID
jest.useFakeTimers();

// CORRECT
jest.useFakeTimers({ doNotFake: ['Date', 'performance'] });
```

---

## 5. Test Structure
**Impact: HIGH**

### Rule: beforeEach/afterEach Are Scoped to describe Blocks

Hooks inside a `describe` only run for tests in that block. Top-level hooks run for every test in the file.

```javascript
describe('user service', () => {
  beforeEach(() => db.clear()); // only for user service tests
  test('creates user', () => { /* ... */ });
});

describe('math utils', () => {
  test('adds numbers', () => { /* ... */ }); // db.clear() does NOT run
});
```

### Rule: Each Test Must Be Independent

Tests sharing mutable state break when run in different order or individually.

```javascript
// INCORRECT
const items = [];
test('adds', () => { items.push('a'); expect(items).toHaveLength(1); });
test('adds more', () => { items.push('b'); expect(items).toHaveLength(2); }); // order-dependent

// CORRECT
let items;
beforeEach(() => { items = []; });
test('adds', () => { items.push('a'); expect(items).toHaveLength(1); });
test('adds more', () => { items.push('b'); expect(items).toHaveLength(1); });
```

### Rule: Tests Must Be Defined Synchronously

Jest discovers tests by running the file synchronously. Tests inside async callbacks are never registered.

```javascript
// INCORRECT — tests never run
(async () => {
  const cases = await loadCases();
  cases.forEach(c => test(c.name, () => { /* ... */ }));
})();

// CORRECT — use test.each with synchronous data
const cases = require('./cases.json');
test.each(cases)('$name', ({ input, expected }) => {
  expect(process(input)).toBe(expected);
});
```

---

## 6. Module Mocking
**Impact: MEDIUM**

### Rule: __mocks__ Directory Conventions

| Module type | Mock location | Auto-used? |
|---|---|---|
| User module (`./utils/helpers`) | `./utils/__mocks__/helpers.js` | No — needs `jest.mock()` |
| Node module (`axios`) | `<rootDir>/__mocks__/axios.js` | Yes |
| Scoped (`@scope/pkg`) | `__mocks__/@scope/pkg.js` | Yes |

### Rule: Use jest.unstable_mockModule for ESM

`jest.mock()` relies on CJS hoisting. For native ESM, use `jest.unstable_mockModule` + dynamic `import()`.

```javascript
jest.unstable_mockModule('./api.mjs', () => ({
  fetchUser: jest.fn(),
}));

test('ESM mock', async () => {
  const { fetchUser } = await import('./api.mjs');
  fetchUser.mockReturnValue({ id: 1 });
  expect(fetchUser()).toEqual({ id: 1 });
});
```

### Rule: jest.doMock + resetModules for Per-Test Mocks

`jest.mock()` is hoisted and file-wide. `jest.doMock()` is not hoisted — use it for per-test mocking.

```javascript
beforeEach(() => jest.resetModules());

test('test config', () => {
  jest.doMock('./config', () => ({ env: 'test' }));
  const config = require('./config');
  expect(config.env).toBe('test');
});

test('prod config', () => {
  jest.doMock('./config', () => ({ env: 'production' }));
  const config = require('./config');
  expect(config.env).toBe('production');
});
```

---

## 7. Snapshot Testing
**Impact: MEDIUM**

### Rule: Keep Snapshots Small and Focused

Large snapshots get rubber-stamp updated. Prefer specific matchers, then inline snapshots, then small external snapshots.

```javascript
// INCORRECT — 500-line snapshot
expect(renderer.create(<Page />).toJSON()).toMatchSnapshot();

// CORRECT — targeted
expect(getByTestId('greeting')).toMatchSnapshot();
expect(formatGreeting('Alice')).toMatchInlineSnapshot(`"Hello, Alice!"`);

// BEST — specific matcher
expect(getByText('Hello, Alice!')).toBeInTheDocument();
```

### Rule: Use Property Matchers for Dynamic Fields

```javascript
expect(createUser({ name: 'Alice' })).toMatchSnapshot({
  id: expect.any(String),
  createdAt: expect.any(Date),
});
// Snapshot pins name: "Alice" but allows any String id and any Date createdAt
```

### Rule: Mock Non-Deterministic Values

```javascript
jest.useFakeTimers({ now: new Date('2024-01-01') });
jest.spyOn(Math, 'random').mockReturnValue(0.5);
jest.spyOn(crypto, 'randomUUID').mockReturnValue('00000000-0000-0000-0000-000000000001');
```

---

## 8. Configuration
**Impact: MEDIUM**

### Rule: Set Per-Directory Coverage Thresholds

Global thresholds average coverage across the codebase. Per-directory thresholds enforce higher standards where it matters.

```javascript
module.exports = {
  coverageThreshold: {
    global: { branches: 70, functions: 70, lines: 70, statements: 70 },
    './src/payments/': { branches: 90, lines: 95 },
    './src/auth/': { branches: 85, lines: 90 },
  },
};
```

### Rule: Configure transformIgnorePatterns for ESM Packages

Jest's default skips `node_modules/`. ESM-only packages need a negative lookahead.

```javascript
module.exports = {
  transformIgnorePatterns: [
    '/node_modules/(?!(uuid|nanoid|chalk)/)',
  ],
};
```

### Rule: Per-File @jest-environment Docblock

Default to `'node'` globally. Use docblock for files that need DOM.

```javascript
// jest.config.js
module.exports = { testEnvironment: 'node' };

// Component test file:
/**
 * @jest-environment jsdom
 */
```

---

## 9. Performance & CI
**Impact: MEDIUM**

### Rule: --runInBand or --maxWorkers for CI

Default worker count can overwhelm CI containers. Use `--runInBand` for small suites, `--maxWorkers` for control.

```bash
npx jest --runInBand              # serial — best for < 100 tests
npx jest --maxWorkers=2           # fixed workers
npx jest --maxWorkers=50%         # scales with container
npx jest --shard=1/4              # split across CI jobs
```

### Rule: jest.isolateModules for Per-Test Module State

`jest.isolateModules` creates a sandboxed module registry without affecting other tests.

```javascript
test('fresh module', () => {
  jest.isolateModules(() => {
    jest.doMock('./config', () => ({ debug: true }));
    const app = require('./app');
    expect(app.isDebug()).toBe(true);
  });
});
```

---

## Quick Reference: Mock Cleanup

```javascript
// jest.config.js (recommended)
module.exports = { restoreMocks: true };

// Manual
afterEach(() => jest.restoreAllMocks());
```

## Quick Reference: Async Testing

```javascript
// Always await
test('async', async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});

// Guard with assertions count
test('error handling', async () => {
  expect.assertions(1);
  await expect(badCall()).rejects.toThrow('error');
});
```

## Quick Reference: Timer Mocking

```javascript
jest.useFakeTimers();
// Use async variants when code mixes timers + promises:
await jest.advanceTimersByTimeAsync(1000);
// Restore:
jest.useRealTimers();
```

## Quick Reference: Matchers

| Need | Matcher |
|------|---------|
| Primitive equality | `toBe` |
| Deep object equality | `toStrictEqual` |
| Loose deep equality | `toEqual` |
| Float comparison | `toBeCloseTo` |
| Error thrown | `expect(() => fn()).toThrow()` |
| Promise resolves | `await expect(p).resolves.toBe()` |
| Promise rejects | `await expect(p).rejects.toThrow()` |
| Mock called | `toHaveBeenCalledWith()` |
| Partial object match | `toMatchObject()` |
| Array contains | `toContain()` / `toContainEqual()` |
