# Async Testing Patterns Reference

## async/await (Preferred)

The simplest and safest pattern. The test function is `async`, and you `await` async operations.

```javascript
test('fetches user', async () => {
  const user = await fetchUser(1);
  expect(user.name).toBe('Alice');
});
```

Any unhandled rejection inside an `async` test automatically fails the test.

## Returning Promises

If you return a promise, Jest waits for it to resolve. If it rejects, the test fails.

```javascript
test('fetches user', () => {
  return fetchUser(1).then(user => {
    expect(user.name).toBe('Alice');
  });
});
```

**Warning**: If you forget `return`, the promise is floating and assertions may be skipped.

## .resolves / .rejects

Chain `.resolves` or `.rejects` on `expect()` to unwrap promises inline. Must be `await`ed.

```javascript
test('resolves to user', async () => {
  await expect(fetchUser(1)).resolves.toEqual({ id: 1, name: 'Alice' });
});

test('rejects with error', async () => {
  await expect(fetchUser(-1)).rejects.toThrow('not found');
});
```

`.resolves` and `.rejects` return promises — you **must** `await` or `return` them.

## done Callback (Legacy)

For callback-based APIs. The test receives a `done` function and must call `done()` on success or `done(error)` on failure.

```javascript
test('calls callback', (done) => {
  fetchUser(1, (error, user) => {
    try {
      expect(error).toBeNull();
      expect(user.name).toBe('Alice');
      done();
    } catch (e) {
      done(e);
    }
  });
});
```

**Rules for `done`**:
- Always wrap `expect` in try/catch and call `done(error)` in the catch.
- If `done()` is never called, the test times out after `jest.setTimeout` (default: 5s).
- Do not mix `done` with `async` — Jest throws if both are used.

## expect.assertions(n)

Verifies that exactly `n` assertions ran during the test. Catches silently skipped assertions.

```javascript
test('handles errors', async () => {
  expect.assertions(1);
  try {
    await riskyOperation();
  } catch (e) {
    expect(e.message).toMatch('failed');
  }
});
```

## expect.hasAssertions()

Verifies that at least one assertion ran. Weaker than `expect.assertions(n)`.

```javascript
test('all items valid', async () => {
  expect.hasAssertions();
  const items = await getItems();
  items.forEach(item => {
    expect(item.valid).toBe(true);
  });
});
```

## Testing Rejected Promises

### Approach 1: .rejects (preferred)

```javascript
test('rejects on invalid input', async () => {
  await expect(processData(null)).rejects.toThrow('invalid');
});
```

### Approach 2: try/catch with assertions count

```javascript
test('rejects on invalid input', async () => {
  expect.assertions(2);
  try {
    await processData(null);
  } catch (e) {
    expect(e).toBeInstanceOf(ValidationError);
    expect(e.message).toMatch('invalid');
  }
});
```

### Approach 3: .catch handler

```javascript
test('rejects on invalid input', () => {
  expect.assertions(1);
  return processData(null).catch(e => {
    expect(e.message).toMatch('invalid');
  });
});
```

## Testing Async Iteration

```javascript
test('processes stream', async () => {
  const results = [];
  for await (const chunk of createStream()) {
    results.push(chunk);
  }
  expect(results).toEqual(['a', 'b', 'c']);
});
```

## Common Mistakes

### Missing await on .resolves/.rejects

```javascript
// BUG: Missing await — assertion is skipped
test('resolves', () => {
  expect(asyncFn()).resolves.toBe('value'); // no await or return — SKIPPED
});

// FIX
test('resolves', async () => {
  await expect(asyncFn()).resolves.toBe('value');
});
```

### Mixing done and async

```javascript
// BUG: Jest throws "An Async callback was invoked..."
test('bad', async (done) => {
  const data = await fetch('/api');
  done(); // ERROR — cannot use done with async
});

// FIX: Remove done, just use async/await
test('good', async () => {
  const data = await fetch('/api');
  expect(data).toBeDefined();
});
```

### Forgetting to return in .then chains

```javascript
// BUG: No return — floating promise
test('bad', () => {
  fetchData().then(data => { expect(data).toBeDefined(); });
});

// FIX
test('good', () => {
  return fetchData().then(data => { expect(data).toBeDefined(); });
});
```

## Timeouts

```javascript
// Per-test timeout (3rd argument)
test('slow operation', async () => {
  await longRunningTask();
}, 30000);

// Per-file timeout
jest.setTimeout(30000);
```
