---
title: Use `HttpResponse.error()` for Network Failures
impact: HIGH
description: Simulate network errors with `HttpResponse.error()`, not by throwing inside resolvers.
tags: response, error, network, HttpResponse.error
---

# Use `HttpResponse.error()` for Network Failures

## Problem

Throwing an error inside a resolver doesn't simulate a network failure — it crashes the handler. Use `HttpResponse.error()` which produces a `TypeError: Failed to fetch` on the client side.

## Incorrect

```typescript
// BUG: throwing crashes the handler — client gets unhandled error, not a network failure
http.get('/api/data', () => {
  throw new Error('Network failure')
})
```

## Correct

```typescript
// Simulates a network error (TypeError: Failed to fetch)
http.get('/api/data', () => {
  return HttpResponse.error()
})
```

## Why

`HttpResponse.error()` creates a `Response` with `type: "error"`, which the Fetch API translates to a `TypeError: Failed to fetch`. This is what applications actually see during real network failures (DNS errors, connection refused, etc.). Throwing inside a resolver is an unhandled exception in MSW internals.
