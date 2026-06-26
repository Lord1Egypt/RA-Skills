# Mock Functions Reference

## Creating Mocks

### `jest.fn()`

Creates a standalone mock function with no implementation (returns `undefined`).

```javascript
const mock = jest.fn();
mock('arg1', 'arg2');
expect(mock).toHaveBeenCalledWith('arg1', 'arg2');
```

### `jest.fn(implementation)`

Creates a mock with a default implementation.

```javascript
const add = jest.fn((a, b) => a + b);
expect(add(1, 2)).toBe(3);
expect(add).toHaveBeenCalledTimes(1);
```

### `jest.spyOn(object, methodName)`

Wraps an existing method with a mock while preserving the original implementation. The original can be restored with `.mockRestore()`.

```javascript
const spy = jest.spyOn(console, 'log');
console.log('hello');
expect(spy).toHaveBeenCalledWith('hello');
spy.mockRestore(); // restores original console.log
```

### `jest.spyOn(object, methodName, accessType)`

Spy on getters or setters.

```javascript
const spy = jest.spyOn(obj, 'value', 'get').mockReturnValue(42);
expect(obj.value).toBe(42);
```

## Mock Return Values

```javascript
const mock = jest.fn();

// Single return value
mock.mockReturnValue(42);
expect(mock()).toBe(42);

// One-time return value (used once, then falls back to default)
mock.mockReturnValueOnce(1).mockReturnValueOnce(2).mockReturnValue(99);
expect(mock()).toBe(1);  // first call
expect(mock()).toBe(2);  // second call
expect(mock()).toBe(99); // all subsequent calls

// Resolved promise
mock.mockResolvedValue({ data: 'ok' });
await expect(mock()).resolves.toEqual({ data: 'ok' });

// Rejected promise
mock.mockRejectedValue(new Error('fail'));
await expect(mock()).rejects.toThrow('fail');

// One-time resolved/rejected
mock.mockResolvedValueOnce('first').mockRejectedValueOnce(new Error('second'));
```

## Mock Implementations

```javascript
const mock = jest.fn();

// Permanent implementation
mock.mockImplementation((x) => x * 2);
expect(mock(5)).toBe(10);

// One-time implementation
mock.mockImplementationOnce((x) => x + 1).mockImplementationOnce((x) => x + 2);
expect(mock(0)).toBe(1);
expect(mock(0)).toBe(2);
```

## The `.mock` Property

Every mock function has a `.mock` property that records all calls, return values, instances, and contexts.

```javascript
const mock = jest.fn((x) => x + 1);
mock.call(thisArg, 10);
mock(20);

mock.mock.calls;          // [[10], [20]] — arguments of each call
mock.mock.results;         // [{ type: 'return', value: 11 }, { type: 'return', value: 21 }]
mock.mock.instances;       // [thisArg, undefined] — `this` value for each call
mock.mock.contexts;        // same as instances (Jest 29.6+)
mock.mock.lastCall;        // [20] — arguments of last call
```

### Result types

| `type` | Meaning |
|---|---|
| `'return'` | Function returned normally |
| `'throw'` | Function threw an error |
| `'incomplete'` | Function is still executing (recursive calls) |

## Clearing, Resetting, Restoring

| Method | Instance version | Config version | Effect |
|---|---|---|---|
| `mockClear()` | `mock.mockClear()` | `clearMocks: true` | Clears `mock.calls`, `mock.instances`, `mock.results` |
| `mockReset()` | `mock.mockReset()` | `resetMocks: true` | `mockClear()` + removes implementation (returns `undefined`) |
| `mockRestore()` | `mock.mockRestore()` | `restoreMocks: true` | `mockReset()` + restores original implementation (spyOn only) |

```javascript
// Config-level (recommended)
module.exports = { restoreMocks: true };

// Manual
afterEach(() => {
  jest.restoreAllMocks();
});
```

## Mock Matchers

```javascript
const fn = jest.fn();
fn('a', 'b');
fn('c');

expect(fn).toHaveBeenCalled();                  // called at least once
expect(fn).toHaveBeenCalledTimes(2);             // called exactly 2 times
expect(fn).toHaveBeenCalledWith('a', 'b');       // any call had these args
expect(fn).toHaveBeenLastCalledWith('c');         // last call had these args
expect(fn).toHaveBeenNthCalledWith(1, 'a', 'b'); // first call had these args
```

## Mocking Modules

```javascript
// Auto-mock all exports
jest.mock('./module');

// Mock with factory
jest.mock('./module', () => ({
  fn: jest.fn(() => 'mocked'),
}));

// Partial mock — keep some exports real
jest.mock('./module', () => ({
  ...jest.requireActual('./module'),
  fn: jest.fn(),
}));
```

## Replacing Properties

```javascript
// jest.replaceProperty (Jest 29.4+)
const replaced = jest.replaceProperty(process, 'env', { NODE_ENV: 'test' });
expect(process.env.NODE_ENV).toBe('test');
replaced.restore(); // or use restoreMocks config
```

## TypeScript Helpers

```typescript
import { jest, type Mocked } from '@jest/globals';

// Type a mocked module
jest.mock('./api');
const api = jest.mocked(require('./api'));
// api.fetchUser is now typed as jest.Mock<typeof fetchUser>

// Type a single mock function
const fn = jest.fn<(x: number) => string>();
fn.mockReturnValue('hello');
```
