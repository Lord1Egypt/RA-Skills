# Jest Object Reference

The `jest` object is available globally in every test file. It provides methods for mocking, timer control, module manipulation, and test configuration.

## Module Mocking

### `jest.mock(moduleName, factory?, options?)`

Mocks a module. Hoisted to the top of the file automatically.

```javascript
// Auto-mock (all exports become jest.fn())
jest.mock('./api');

// Factory mock
jest.mock('./api', () => ({
  fetchUser: jest.fn(() => ({ id: 1 })),
}));

// Virtual module (does not need to exist on disk)
jest.mock('virtual-module', () => ({ key: 'value' }), { virtual: true });
```

### `jest.unmock(moduleName)`

Undoes `jest.mock` — the real module is used. Also hoisted.

### `jest.doMock(moduleName, factory?, options?)`

Same as `jest.mock` but **not hoisted**. Use for per-test mocking with `jest.resetModules()`.

### `jest.dontMock(moduleName)`

Same as `jest.unmock` but not hoisted.

### `jest.resetModules()`

Clears the module registry cache. The next `require()` loads a fresh copy.

```javascript
beforeEach(() => {
  jest.resetModules();
});
```

### `jest.isolateModules(fn)`

Creates a sandboxed module registry for the duration of `fn`. Registry is restored after `fn` completes.

```javascript
jest.isolateModules(() => {
  jest.doMock('./config', () => ({ debug: true }));
  const app = require('./app'); // fresh, isolated instance
});
```

### `jest.requireActual(moduleName)`

Returns the real module, bypassing any mocks. Used inside `jest.mock` factories for partial mocking.

```javascript
jest.mock('./api', () => ({
  ...jest.requireActual('./api'),
  fetchUser: jest.fn(),
}));
```

### `jest.requireMock(moduleName)`

Returns the mock version of a module, even if `jest.mock` was not called (uses auto-mocking).

### `jest.createMockFromModule(moduleName)`

Creates an auto-mocked version of a module. Useful in manual mock files (`__mocks__/`).

```javascript
const utils = jest.createMockFromModule('./utils');
utils.format.mockReturnValue('formatted');
module.exports = utils;
```

## ESM Mocking

### `jest.unstable_mockModule(moduleName, factory, options?)`

Mocks a module for ES module imports. Must be called before `await import()`.

```javascript
jest.unstable_mockModule('./api.mjs', () => ({
  fetchUser: jest.fn(),
}));

const { fetchUser } = await import('./api.mjs');
```

## Timer Mocking

### `jest.useFakeTimers(config?)`

Replaces timer globals with fakes.

```javascript
jest.useFakeTimers();
jest.useFakeTimers({ now: new Date('2024-01-01') }); // fixed Date.now
jest.useFakeTimers({ doNotFake: ['Date', 'performance'] }); // selective
jest.useFakeTimers({ timerLimit: 1000 }); // max timers before error
```

### `jest.useRealTimers()`

Restores real timer implementations.

### Timer Advancement

| Method | Behavior |
|---|---|
| `jest.runAllTimers()` | Runs all pending timers recursively (unsafe for recursive timers) |
| `jest.runOnlyPendingTimers()` | Runs only currently pending timers |
| `jest.advanceTimersByTime(ms)` | Advances clock by `ms`, firing timers along the way |
| `jest.advanceTimersToNextTimer(steps?)` | Advances to the next timer (optionally repeat `steps` times) |

### Async Timer Methods (Jest 29.5+)

Same as above but flush microtask queue between timer executions:

```javascript
await jest.runAllTimersAsync();
await jest.runOnlyPendingTimersAsync();
await jest.advanceTimersByTimeAsync(1000);
await jest.advanceTimersToNextTimerAsync();
```

### Timer Inspection

```javascript
jest.getTimerCount();      // number of pending timers
jest.now();                // current fake clock time (ms)
jest.setSystemTime(date);  // set fake clock to specific time
jest.getRealSystemTime();  // real Date.now() even when faked
```

## Mock Cleanup

```javascript
jest.clearAllMocks();      // clear call history
jest.resetAllMocks();      // clear + remove implementations
jest.restoreAllMocks();    // clear + remove + restore originals
```

## Test Configuration

### `jest.setTimeout(milliseconds)`

Sets the default timeout for all tests and hooks in the file.

```javascript
jest.setTimeout(30000); // 30 seconds
```

### `jest.retryTimes(count, options?)`

Retries failed tests up to `count` times. Useful for flaky integration tests.

```javascript
jest.retryTimes(3);
jest.retryTimes(3, { logErrorsBeforeRetry: true });
```

## Property Replacement

### `jest.replaceProperty(object, propertyKey, value)`

Replaces a property value on an object. Restored by `jest.restoreAllMocks()`.

```javascript
jest.replaceProperty(process.env, 'NODE_ENV', 'test');
// later restored automatically if restoreMocks: true
```

### `jest.spyOn(object, methodName)`

See [Mock Functions Reference](./mock-functions.md).

## Misc

### `jest.mocked(source, options?)`

TypeScript helper — wraps a module or function with mock types.

```javascript
jest.mock('./api');
const api = jest.mocked(require('./api'));
// api.fetchUser is typed as jest.MockedFunction<typeof fetchUser>
```

### `jest.fn(implementation?)`

Creates a mock function. See [Mock Functions Reference](./mock-functions.md).
