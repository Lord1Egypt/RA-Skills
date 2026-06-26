# MSW Anti-Patterns

## Table of Contents

1. [Using v1 `rest` namespace](#1-using-v1-rest-namespace)
2. [Putting query params in URL predicates](#2-putting-query-params-in-url-predicates)
3. [Importing setupServer from wrong path](#3-importing-setupserver-from-wrong-path)
4. [Missing afterEach(resetHandlers)](#4-missing-aftereachresethandlers)
5. [Asserting on fetch calls](#5-asserting-on-fetch-calls)
6. [Not awaiting request.json()](#6-not-awaiting-requestjson)
7. [Using native Response for cookies](#7-using-native-response-for-cookies)
8. [Not using server.boundary() for concurrent tests](#8-not-using-serverboundary-for-concurrent-tests)
9. [Not setting onUnhandledRequest: 'error'](#9-not-setting-onunhandledrequest-error)
10. [Throwing errors inside resolvers](#10-throwing-errors-inside-resolvers)

## 1. Using v1 `rest` namespace

```typescript
// BAD
import { rest } from 'msw'
rest.get('/api/user', (req, res, ctx) => res(ctx.json({ name: 'John' })))

// GOOD
import { http, HttpResponse } from 'msw'
http.get('/api/user', () => HttpResponse.json({ name: 'John' }))
```

## 2. Putting query params in URL predicates

```typescript
// BAD: silently matches nothing
http.get('/post?id=1', resolver)

// GOOD: read query params inside resolver
http.get('/post', ({ request }) => {
  const url = new URL(request.url)
  const id = url.searchParams.get('id')
  return HttpResponse.json({ id })
})
```

## 3. Importing setupServer from wrong path

```typescript
// BAD
import { setupServer } from 'msw'

// GOOD
import { setupServer } from 'msw/node'
```

## 4. Missing afterEach(resetHandlers)

```typescript
// BAD: handlers leak between tests
beforeAll(() => server.listen())
afterAll(() => server.close())

// GOOD: reset after each test
beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

## 5. Asserting on fetch calls

```typescript
// BAD: tests implementation, not behavior
expect(fetch).toHaveBeenCalledWith('/api/login', expect.objectContaining({
  method: 'POST',
}))

// GOOD: tests what the user sees
await waitFor(() => {
  expect(screen.getByText('Welcome!')).toBeInTheDocument()
})
```

## 6. Not awaiting request.json()

```typescript
// BAD: body is a ReadableStream, not parsed data
http.post('/api/user', ({ request }) => {
  const body = request.body
  return HttpResponse.json({ received: body })
})

// GOOD: await the async method
http.post('/api/user', async ({ request }) => {
  const body = await request.json()
  return HttpResponse.json({ received: body })
})
```

## 7. Using native Response for cookies

```typescript
// BAD: Set-Cookie silently dropped
new Response(null, {
  headers: { 'Set-Cookie': 'token=abc' },
})

// GOOD: HttpResponse supports Set-Cookie
new HttpResponse(null, {
  headers: { 'Set-Cookie': 'token=abc' },
})
```

## 8. Not using server.boundary() for concurrent tests

```typescript
// BAD: overrides leak across concurrent tests
it.concurrent('test A', async () => {
  server.use(http.get('/api/user', () => HttpResponse.json({ role: 'admin' })))
})

// GOOD: boundary isolates overrides
it.concurrent('test A', server.boundary(async () => {
  server.use(http.get('/api/user', () => HttpResponse.json({ role: 'admin' })))
}))
```

## 9. Not setting onUnhandledRequest: 'error'

```typescript
// BAD: unhandled requests silently pass through
server.listen()

// GOOD: missing handlers fail the test
server.listen({ onUnhandledRequest: 'error' })
```

## 10. Throwing errors inside resolvers

```typescript
// BAD: crashes handler internals
http.get('/api/data', () => {
  throw new Error('Network failure')
})

// GOOD: simulates actual network error
http.get('/api/data', () => {
  return HttpResponse.error()
})
```
