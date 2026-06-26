---
title: Use Explicit Milliseconds with `delay()` in Tests
impact: MEDIUM
description: '`delay()` without arguments uses a realistic random delay in the browser but is instant (negated) in Node.js. Use `delay(ms)` for predictable test behavior.'
tags: utility, delay, timing, node, browser, testing
---

# Use Explicit Milliseconds with `delay()`

## Problem

`await delay()` in Node.js test environment does nothing — it resolves immediately. Developers expect a 200ms delay and write timing-dependent assertions.

## Incorrect

```typescript
// BUG: delay() without args is instant in Node.js
http.get('/api/data', async () => {
  await delay() // No-op in Node.js — resolves immediately
  return HttpResponse.json({ data: 'loaded' })
})

// Test expects loading state but never sees it
test('shows loading spinner', async () => {
  render(<DataLoader />)
  // Loading spinner never appears because response is instant
  expect(screen.getByRole('progressbar')).toBeInTheDocument() // FAILS
})
```

## Correct

```typescript
http.get('/api/data', async () => {
  await delay(200) // Explicit: always waits 200ms, even in Node.js
  return HttpResponse.json({ data: 'loaded' })
})

// For testing timeouts:
http.get('/api/slow', async () => {
  await delay('infinite') // Never resolves — tests timeout handling
  return HttpResponse.json({ data: 'never reached' })
})
```

## Delay Behavior by Environment

| Usage | Browser | Node.js | Recommendation |
|-------|---------|---------|----------------|
| `delay()` | Random realistic delay | Instant (negated) | Avoid in tests |
| `delay(ms)` | Waits `ms` | Waits `ms` | Use in tests |
| `delay('real')` | Random realistic delay | Random realistic delay | Simulating real latency |
| `delay('infinite')` | Never resolves | Never resolves | Testing timeouts |

## Why

The no-argument `delay()` is designed for browser mocking where you want realistic-feeling latency without slowing down tests. In Node.js test environments, it's negated to keep tests fast. If your test depends on a delay (e.g., testing loading states), always specify explicit milliseconds.
