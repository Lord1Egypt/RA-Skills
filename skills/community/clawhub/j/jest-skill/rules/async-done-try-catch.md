---
title: Wrap expect in try/catch when using done callback
impact: HIGH
description: When using the done callback pattern, a failing expect throws and done is never called, causing the test to time out instead of reporting the actual assertion failure.
tags: async, done, callback, try-catch, timeout
---

# Wrap expect in try/catch when using done callback

## Problem

When using Jest's `done` callback for async tests, a failing `expect()` throws an error. If the error is not caught, `done()` is never called, and the test times out after 5 seconds with a generic timeout message instead of showing the actual assertion failure. This makes debugging much harder.

## Incorrect

```javascript
// BUG: If expect fails, done() is never called — test times out after 5s
test('calls callback with data', (done) => {
  fetchUser(1, (error, user) => {
    expect(user.name).toBe('Alice'); // if this fails, it throws
    done(); // never reached
  });
});
// Output: "Timeout - Async callback was not invoked within the 5000 ms timeout"
```

## Correct

```javascript
test('calls callback with data', (done) => {
  fetchUser(1, (error, user) => {
    try {
      expect(error).toBeNull();
      expect(user.name).toBe('Alice');
      done();
    } catch (e) {
      done(e); // passes the error to Jest — shows the real failure message
    }
  });
});
```

```javascript
// Better: Convert callback to promise and use async/await
test('calls callback with data', async () => {
  const user = await new Promise((resolve, reject) => {
    fetchUser(1, (error, data) => {
      if (error) reject(error);
      else resolve(data);
    });
  });
  expect(user.name).toBe('Alice');
});
```

## Why

- `done(error)` tells Jest the test failed and provides the actual error message.
- `done()` with no argument tells Jest the test passed.
- If neither is called, Jest waits until timeout — you lose the real failure info.

**Prefer async/await over `done`**. The `done` callback pattern exists for legacy callback-based APIs. Modern code should promisify callbacks and use `async`/`await`, which eliminates this entire class of bugs. Jest 30 deprecates `done` in favor of async patterns.
