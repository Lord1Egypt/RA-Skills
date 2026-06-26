# Handler API Reference

## Table of Contents

- [HTTP Handlers](#http-handlers)
- [GraphQL Handlers](#graphql-handlers)
- [URL Predicates](#url-predicates)
- [Path Parameters](#path-parameters)
- [Handler Options](#handler-options)
- [matchRequestUrl Utility](#matchrequesturl-utility)

## HTTP Handlers

All methods on the `http` namespace:

| Method | Description |
|--------|-------------|
| `http.get(predicate, resolver, options?)` | GET requests |
| `http.post(predicate, resolver, options?)` | POST requests |
| `http.put(predicate, resolver, options?)` | PUT requests |
| `http.patch(predicate, resolver, options?)` | PATCH requests |
| `http.delete(predicate, resolver, options?)` | DELETE requests |
| `http.head(predicate, resolver, options?)` | HEAD requests |
| `http.options(predicate, resolver, options?)` | OPTIONS requests |
| `http.all(predicate, resolver, options?)` | Any HTTP method |

### Signature

```typescript
http.get(
  predicate: string | RegExp | URL | ((input: { request: Request }) => boolean),
  resolver: (info: {
    request: Request
    params: Record<string, string | string[]>
    cookies: Record<string, string>
    requestId: string
  }) => Response | HttpResponse | undefined | void | Promise<...>,
  options?: { once?: boolean }
)
```

## GraphQL Handlers

| Method | Description |
|--------|-------------|
| `graphql.query(operationName, resolver)` | GraphQL queries |
| `graphql.mutation(operationName, resolver)` | GraphQL mutations |
| `graphql.operation(resolver)` | Any GraphQL operation |
| `graphql.link(url)` | Scoped namespace for specific endpoint |

### GraphQL Resolver Info

```typescript
graphql.query('GetUser', ({
  query,           // DocumentNode — parsed GraphQL query
  variables,       // Record<string, any> — query variables
  operationName,   // string — operation name
  request,         // Request — standard Fetch API Request
  cookies,         // Record<string, string>
  requestId,       // string
}) => {
  return HttpResponse.json({ data: { user: { id: variables.id } } })
})
```

## URL Predicates

### String — Exact pathname match

```typescript
http.get('/api/user', resolver)
```

### String with params — Captures path parameters

```typescript
http.get('/api/user/:id', resolver)
```

### Wildcard — Matches path prefix

```typescript
http.get('/api/*', resolver) // matches /api/anything
```

### Absolute URL — Full URL match

```typescript
http.get('https://api.example.com/user', resolver)
```

### RegExp — Pattern matching

```typescript
http.get(/\/api\/user\/\d+/, resolver)
```

### Custom function — Programmatic matching

```typescript
http.get(
  ({ request }) => {
    const url = new URL(request.url)
    return url.pathname.startsWith('/api') && url.searchParams.has('v')
  },
  resolver,
)
```

## Path Parameters

### Single parameter

```typescript
http.get('/user/:id', ({ params }) => {
  const { id } = params // string
  return HttpResponse.json({ id })
})
```

### Multiple parameters

```typescript
http.get('/user/:userId/post/:postId', ({ params }) => {
  const { userId, postId } = params
  return HttpResponse.json({ userId, postId })
})
```

### Wildcard parameter

```typescript
http.get('/files/*', ({ params }) => {
  const path = params['*'] // everything after /files/
  return HttpResponse.json({ path })
})
```

## Handler Options

### One-time handler

Automatically removed after the first matching request:

```typescript
http.get('/api/data', resolver, { once: true })
```

Useful for testing retry logic — first request fails, second succeeds:

```typescript
server.use(
  http.get('/api/data', () => new HttpResponse(null, { status: 500 }), { once: true })
)
// First request → 500 (one-time handler consumed)
// Second request → default handler responds
```

## matchRequestUrl Utility

Utility for programmatic URL matching outside of handlers:

```typescript
import { matchRequestUrl } from 'msw'

const match = matchRequestUrl(
  new URL('https://example.com/user/abc-123'),
  '/user/:id',
)

if (match) {
  console.log(match.params.id) // 'abc-123'
}
```
