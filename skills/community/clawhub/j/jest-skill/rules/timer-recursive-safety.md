---
title: Use runOnlyPendingTimers for recursive timers
impact: HIGH
description: jest.runAllTimers enters an infinite loop when code schedules new timers inside timer callbacks (e.g., recursive setTimeout). Use runOnlyPendingTimers instead.
tags: timer, runAllTimers, runOnlyPendingTimers, recursive, setTimeout, infinite-loop
---

# Use runOnlyPendingTimers for recursive timers

## Problem

`jest.runAllTimers()` runs all pending timers, including any new timers created during execution. If a timer callback schedules another timer (common in polling, retry, and animation patterns), `runAllTimers` enters an infinite loop and the test hangs or crashes with a max recursion error.

## Incorrect

```javascript
// BUG: poll() schedules a new setTimeout each time — runAllTimers loops forever
function poll(callback) {
  fetchData().then(data => {
    callback(data);
    setTimeout(() => poll(callback), 1000); // recursive timer
  });
}

test('polls for data', () => {
  jest.useFakeTimers();
  const cb = jest.fn();
  poll(cb);
  jest.runAllTimers(); // INFINITE LOOP — hangs or throws "Aborting after running 100000 timers"
});
```

## Correct

```javascript
test('polls for data', () => {
  jest.useFakeTimers();
  const cb = jest.fn();
  poll(cb);

  // Run only the timers currently in the queue — does not chase new ones
  jest.runOnlyPendingTimers();
  expect(cb).toHaveBeenCalledTimes(1);

  // Advance one more cycle
  jest.runOnlyPendingTimers();
  expect(cb).toHaveBeenCalledTimes(2);
});
```

```javascript
// Alternative: advanceTimersByTime for precise control
test('polls every second', () => {
  jest.useFakeTimers();
  const cb = jest.fn();
  poll(cb);

  jest.advanceTimersByTime(3000); // advance 3 seconds
  expect(cb).toHaveBeenCalledTimes(3);
});
```

## Decision Table

| Method | Behavior | Safe for recursive timers |
|---|---|---|
| `runAllTimers()` | Runs all timers including newly created ones | No — infinite loop |
| `runOnlyPendingTimers()` | Runs only timers in the queue at call time | Yes |
| `advanceTimersByTime(ms)` | Advances clock by `ms`, running timers that fire | Yes |
| `advanceTimersToNextTimer()` | Advances to the next timer and runs it | Yes |

## Why

Recursive timers are extremely common: `setInterval`, polling loops, retry-with-backoff, `requestAnimationFrame` polyfills, and debounce/throttle implementations all create new timers from within timer callbacks. Always use `runOnlyPendingTimers` or `advanceTimersByTime` unless you are certain no recursive timers exist.
