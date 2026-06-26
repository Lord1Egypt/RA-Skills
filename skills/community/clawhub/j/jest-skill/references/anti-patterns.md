# Anti-Patterns Reference

Common Jest mistakes that cause silent failures, flaky tests, or false positives. Each pattern includes the bug, why it's wrong, and the fix.

## 1. Floating Promise — Assertions Never Run

```javascript
// BAD: Missing await — test passes with 0 assertions
test('fetches data', () => {
  fetchData().then(data => {
    expect(data).toBeDefined(); // never runs
  });
});

// GOOD
test('fetches data', async () => {
  const data = await fetchData();
  expect(data).toBeDefined();
});
```

## 2. Missing expect.assertions — Silent Skip

```javascript
// BAD: If the try branch succeeds, catch never runs, test passes vacuously
test('handles error', async () => {
  try {
    await riskyOp();
  } catch (e) {
    expect(e.message).toMatch('error');
  }
});

// GOOD
test('handles error', async () => {
  expect.assertions(1);
  try {
    await riskyOp();
  } catch (e) {
    expect(e.message).toMatch('error');
  }
});
```

## 3. toBe on Objects — Reference Comparison

```javascript
// BAD: Different object references
expect(getUser()).toBe({ name: 'Alice' }); // FAILS

// GOOD
expect(getUser()).toEqual({ name: 'Alice' });
```

## 4. toThrow Without Wrapper

```javascript
// BAD: Function executes immediately
expect(throwingFn()).toThrow(); // UNCAUGHT ERROR

// GOOD
expect(() => throwingFn()).toThrow();
```

## 5. clearAllMocks Instead of restoreAllMocks

```javascript
// BAD: Implementations persist
afterEach(() => jest.clearAllMocks());

// GOOD
afterEach(() => jest.restoreAllMocks());

// BEST
// jest.config.js: { restoreMocks: true }
```

## 6. Shared Mutable State

```javascript
// BAD: Tests depend on order
const items = [];
test('adds item', () => { items.push('a'); expect(items).toHaveLength(1); });
test('adds another', () => { items.push('b'); expect(items).toHaveLength(2); }); // order-dependent

// GOOD
let items;
beforeEach(() => { items = []; });
test('adds item', () => { items.push('a'); expect(items).toHaveLength(1); });
test('adds another', () => { items.push('b'); expect(items).toHaveLength(1); });
```

## 7. runAllTimers With Recursive Timers

```javascript
// BAD: Infinite loop
jest.useFakeTimers();
startPolling();
jest.runAllTimers(); // hangs

// GOOD
jest.runOnlyPendingTimers();
// or
jest.advanceTimersByTime(5000);
```

## 8. Mock Factory Referencing Outer Variables

```javascript
// BAD: Variable not initialized when factory runs (hoisting)
const mockData = loadFixtures();
jest.mock('./api', () => ({ getData: () => mockData }));

// GOOD: Inline or use `mock` prefix
jest.mock('./api', () => ({ getData: () => ({ id: 1 }) }));
```

## 9. Forgetting jest.requireActual in Partial Mocks

```javascript
// BAD: All exports except mocked ones are undefined
jest.mock('./utils', () => ({ format: jest.fn() }));

// GOOD
jest.mock('./utils', () => ({
  ...jest.requireActual('./utils'),
  format: jest.fn(),
}));
```

## 10. Test Defined in Async Context

```javascript
// BAD: Tests are never registered
(async () => {
  const cases = await loadCases();
  cases.forEach(c => test(c.name, () => { /* ... */ }));
})();

// GOOD: Use test.each with synchronous data
const cases = require('./cases.json');
test.each(cases)('$name', ({ input, expected }) => {
  expect(process(input)).toBe(expected);
});
```

## 11. Not Awaiting .resolves/.rejects

```javascript
// BAD: Floating assertion
test('resolves', () => {
  expect(asyncFn()).resolves.toBe('value'); // no await
});

// GOOD
test('resolves', async () => {
  await expect(asyncFn()).resolves.toBe('value');
});
```

## 12. done With try but No catch

```javascript
// BAD: Assertion failure causes timeout instead of real error
test('callback test', (done) => {
  asyncOp((err, data) => {
    expect(data).toBe('value'); // throws, done never called → timeout
    done();
  });
});

// GOOD
test('callback test', (done) => {
  asyncOp((err, data) => {
    try {
      expect(data).toBe('value');
      done();
    } catch (e) {
      done(e);
    }
  });
});
```

## 13. Forgetting useRealTimers in afterEach

```javascript
// BAD: Fake timers leak to next test file (in same worker)
test('timer test', () => {
  jest.useFakeTimers();
  // ... test code
  // forgot to restore
});

// GOOD
afterEach(() => {
  jest.useRealTimers();
});
```

## 14. Large Snapshots That Get Rubber-Stamp Updated

```javascript
// BAD: 500-line snapshot nobody reviews
expect(renderer.create(<EntirePage />).toJSON()).toMatchSnapshot();

// GOOD: Small, focused snapshots
expect(renderer.create(<Header />).toJSON()).toMatchSnapshot();
expect(formatOutput(data)).toMatchInlineSnapshot(`"expected output"`);
```

## 15. Sync Timer Methods With Async Code

```javascript
// BAD: Promises not flushed
jest.useFakeTimers();
startAsyncPoller();
jest.advanceTimersByTime(5000); // timers fire but promises don't resolve

// GOOD: Use async timer methods
await jest.advanceTimersByTimeAsync(5000);
```
