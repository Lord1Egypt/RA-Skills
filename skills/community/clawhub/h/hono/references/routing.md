# Hono Routing

## Basic Routes

```ts
const app = new Hono()

// HTTP methods
app.get(path, ...handlers)
app.post(path, ...handlers)
app.put(path, ...handlers)
app.patch(path, ...handlers)
app.delete(path, ...handlers)
app.options(path, ...handlers)
app.head(path, ...handlers)

// Any method
app.all('/webhook', (c) => c.text('OK'))

// Multiple paths
app.get(['/', '/home'], (c) => c.text('Home'))
```

## Path Parameters

```ts
// Basic params
app.get('/users/:id', (c) => {
  const id = c.req.param('id')  // auto-inferred as string
  return c.json({ id })
})

// Multiple params
app.get('/posts/:postId/comments/:commentId', (c) => {
  const { postId, commentId } = c.req.param()
})

// Optional params (use ?)
app.get('/api/:version?/users', (c) => {
  const version = c.req.param('version')  // undefined or string
})

// Regex params
app.get('/posts/:id{.+}', (c) => {
  // matches /posts/a/b/c, id = "a/b/c"
})

// Numeric only
app.get('/items/:id{[0-9]+}', (c) => {
  const id = c.req.param('id')  // type auto-inferred
})
```

**Type inference**: Path params are auto-inferred as literal types. For `/users/:id`, `c.req.param('id')` is `string`, but for fixed routes like `/users/:name` where name has specific values, types are more precise.

## Route Grouping (app.route)

```ts
// Basic grouping
const api = new Hono()
api.get('/users', ...)
api.post('/users', ...)
api.get('/users/:id', ...)
app.route('/api', api)
// => /api/users, /api/users/:id

// Nested grouping
const v1 = new Hono()
v1.get('/posts', ...)
app.route('/v1', v1)

const v2 = new Hono()
v2.get('/posts', ...)
app.route('/v2', v2)

app.route('/api', v1)
app.route('/api', v2)
```

## Route Prefix and Nesting

```ts
const app = new Hono()

// Nested routes
app.get('/posts/:id', (c) => c.text('post'))
app.get('/posts/:id/comments', (c) => c.text('comments'))
// Both :id type inference works independently
```

## Smart Router and Multiple Routers

Hono defaults to `SmartRouter` combining router strengths:
- **RegExpRouter**: Fastest, matches with single large regex
- **LinearRouter**: Fast registration, suitable for per-request init environments (e.g. Lambda)
- **PatternRouter**: Smallest, pattern-based matching

Specify router:
```ts
import { Hono } from 'hono'
import { LinearRouter } from 'hono/router/linear-router'

const app = new Hono({ router: LinearRouter })
```

## Route Priority

Routes match in registration order. With `app.route()`, child routes have priority.

```ts
app.get('/users', (c) => c.text('users list'))
app.get('/users/:id', (c) => c.text('user detail'))
// /users -> "users list"
// /users/123 -> "user detail"
```

## Async Handlers

```ts
app.get('/users/:id', async (c) => {
  const id = c.req.param('id')
  const user = await db.users.find(id)
  if (!user) return c.json({ error: 'not found' }, 404)
  return c.json(user)
})
```

## Middleware on Routes

```ts
// Global middleware
app.use(logger())

// Path-specific
app.use('/api/*', authenticate())
app.get('/api/public', (c) => c.json({ ok: true }))  // /api/public skips auth

// Middleware per route
app.get('/protected', authorize(), (c) => c.json({ secret: true }))
```

## Error Handling and 404

```ts
// 404 Handler
app.notFound((c) => c.json({ error: 'Not Found' }, 404))

// Error handler
app.onError((err, c) => {
  console.error(err)
  return c.json({ error: 'Internal Error' }, 500)
})

// Combined
app.notFound((c) => c.json({ error: 'Not Found' }, 404))
app.onError((err, c) => c.json({ error: err.message }, 500))
```

## Metadata on Routes

```ts
app.get('/', (c) => c.text('OK'), (c) => {
  // Third arg is pre-handler metadata handler
  // Can be used for permission checks
  return c.text('', 401)
})
```

## Regex-Based Routing

```ts
// matches both /posts/123 and /posts/abc
app.get('/posts/:id{[0-9]+}', (c) => c.text('numeric id'))
app.get('/posts/:id{[a-z]+}', (c) => c.text('alpha id'))
```

## Handler Return Types

```ts
// Auto-inferred, common forms:
c.text('str')              // Response
c.json(obj)                // Response (Content-Type: application/json)
c.json(obj, 201)           // with status
c.html('<div/>')           // Response (Content-Type: text/html; charset=UTF-8)
c.body(null)               // empty response
c.body(stream)             // streaming response
c.redirect('/url')         // 302 redirect
c.redirect('/url', 301)    // 301 permanent redirect
```

## Chained API

```ts
new Hono()
  .get('/', (c) => c.text('Hello'))
  .post('/users', (c) => c.json({ ok: true }, 201))
  .get('/users/:id', (c) => c.json({ id: c.req.param('id') }))
  .onError((err, c) => c.json({ error: err.message }, 500))
  .notFound((c) => c.json({ error: 'Not Found' }, 404))
```

## Mount (External App)

Mount another Hono app as middleware:

```ts
const otherApp = new Hono()
otherApp.get('/foo', (c) => c.text('foo'))

app.mount('/mount', otherApp)
// /mount/foo -> 'foo'
```
