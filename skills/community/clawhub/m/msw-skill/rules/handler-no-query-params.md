---
title: Never Put Query Parameters in Handler URL Predicates
impact: CRITICAL
description: Query parameters in handler URLs silently match nothing. Read them from `request.url` inside the resolver instead.
tags: handler, url, query-params, predicate, silent-failure
---

# Never Put Query Parameters in Handler URL Predicates

## Problem

Developers put query params in the handler URL string. MSW strips query params from the URL before matching, so `http.get('/post?id=1', ...)` will never match any request.

## Incorrect

```typescript
// BUG: query parameters in the URL predicate are silently ignored
// This handler will NEVER match '/post?id=1'
http.get('/post?id=1', () => {
  return HttpResponse.json({ id: 1, title: 'First Post' })
})
```

## Correct

```typescript
http.get('/post', ({ request }) => {
  const url = new URL(request.url)
  const id = url.searchParams.get('id')

  if (id === '1') {
    return HttpResponse.json({ id: 1, title: 'First Post' })
  }

  return HttpResponse.json({ error: 'Not found' }, { status: 404 })
})
```

## Why

MSW matches handlers by pathname only. Query parameters are stripped before matching. Including them in the URL predicate creates a handler that silently never matches, which is extremely difficult to debug.
