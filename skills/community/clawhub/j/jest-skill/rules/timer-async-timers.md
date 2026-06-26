---
title: Use async timer methods when promises are involved
impact: HIGH
description: Synchronous timer methods (runAllTimers, advanceTimersByTime) do not flush microtask queues. When code mixes setTimeout with promises, use the async variants.
tags: timer, async, advanceTimersByTimeAsync, promise, microtask
---

# Use async timer methods when promises are involved

## Problem

When application code mixes timers with promises (e.g., `setTimeout` inside an `async` function, or a promise that resolves after a timeout), synchronous timer methods like `jest.advanceTimersByTime()` only advance timers — they do not flush the microtask queue. Promises remain unresolved, and assertions against their results fail or pass vacuously.

## Incorrect

```javascript
// BUG: advanceTimersByTime runs the timer, but the promise inside is not flushed
async function delayedFetch(url) {
  return new Promise(resolve => {
    setTimeout(async () => {
      const data = await fetch(url);
      resolve(data);
    }, 1000);
  });
}

test('fetches after delay', () => {
  jest.useFakeTimers();
  const promise = delayedFetch('/api');
  jest.advanceTimersByTime(1000); // timer fires, but promise chain is not flushed
  // promise is still pending here
});
```

## Correct

```javascript
// Jest 29.5+ provides async timer methods
test('fetches after delay', async () => {
  jest.useFakeTimers();
  const promise = delayedFetch('/api');

  // Async variant: advances timers AND flushes microtask queue
  await jest.advanceTimersByTimeAsync(1000);

  const data = await promise;
  expect(data).toBeDefined();
});
```

## Async Timer Methods (Jest 29.5+)

| Sync method | Async equivalent |
|---|---|
| `jest.runAllTimers()` | `jest.runAllTimersAsync()` |
| `jest.runOnlyPendingTimers()` | `jest.runOnlyPendingTimersAsync()` |
| `jest.advanceTimersByTime(ms)` | `jest.advanceTimersByTimeAsync(ms)` |
| `jest.advanceTimersToNextTimer()` | `jest.advanceTimersToNextTimerAsync()` |

## Why

JavaScript has two task queues:

1. **Macrotask queue**: `setTimeout`, `setInterval`, `setImmediate`
2. **Microtask queue**: `Promise.then`, `queueMicrotask`, `process.nextTick`

Synchronous timer methods only process the macrotask queue. The async variants interleave microtask flushing, matching how a real event loop works. Always use async timer methods when:

- Timer callbacks contain `await`
- Timer callbacks return or resolve promises
- Code under test chains `.then()` inside `setTimeout`

```javascript
afterEach(() => {
  jest.useRealTimers();
});
```
