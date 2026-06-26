# Hono Context API

Context (c) is the core object in Hono request handling, providing request info, response building, state management, and more.

## Creating Context

In handlers, Context is passed as the first argument:

```ts
app.get('/path', (c) => {
  // c is the Context object
  return c.text('OK')
})
```

## Response Methods

### c.text(body, status?)

Return plain text:

```ts
c.text('Hello World')
c.text('Not Found', 404)
c.text('Created', 201)
```

### c.json(body, status?)

Return JSON (auto sets Content-Type: application/json):

```ts
c.json({ message: 'OK' })
c.json({ error: 'Not found' }, 404)
c.json([1, 2, 3])
```

### c.html(body, status?)

Return HTML (auto sets Content-Type: text/html; charset=UTF-8):

```ts
c.html('<h1>Hello!</h1>')
c.html('<p>Not found</p>', 404)
```

### c.body(body, headers?, status?)

Return raw response body:

```ts
// String body
c.body('<xml>...</xml>', {
  'Content-Type': 'application/xml'
})

// Stream body (for large files, SSE, etc.)
const stream = new ReadableStream({
  start(controller) {
    controller.enqueue('data: hello\n\n')
    controller.close()
  }
})
c.body(stream, { 'Content-Type': 'text/event-stream' })

// null body
c.body(null, { 'Content-Type': 'image/png' })
```

### c.stream(body, headers?)

Return streaming response:

```ts
c.stream(
  new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 10; i++) {
        controller.enqueue(`data: ${i}\n\n`)
        await sleep(1000)
      }
      controller.close()
    }
  }),
  { 'Content-Type': 'text/event-stream' }
)
```

### c.redirect(path, status?)

Redirect:

```ts
c.redirect('/login')           // 302
c.redirect('/login', 301)      // 301
c.redirect('https://ext.com')  // external redirect
```

### c.notFound()

Return 404. **Not recommended in RPC mode** (type loss), use `c.json({}, 404)` instead.

## Request Info Reading

### c.req.param(key?)

Get path parameters:

```ts
// /users/:id
const id = c.req.param('id')       // string
const params = c.req.param()        // { id: string }

// Auto type inference
// /users/:id -> id: string
// /posts/:postId/comments/:commentId -> { postId: string, commentId: string }
```

### c.req.query(key?)

Get query parameters:

```ts
// /search?q=hello&page=1
const q = c.req.query('q')          // 'hello'
const page = c.req.query('page')    // '1'
const all = c.req.query()           // { q: 'hello', page: '1' }
```

### c.req.header(key?)

Get request headers (case-insensitive):

```ts
const auth = c.req.header('Authorization')
const contentType = c.req.header('content-type')  // case-insensitive
```

### c.req.cookie(key?)

Get cookies (requires cookie middleware):

```ts
const sessionId = c.req.cookie('session_id')
```

### c.req.valid(target)

Get validated data (requires validator):

```ts
app.post('/posts',
  zValidator('json', z.object({ title: z.string() })),
  (c) => {
    const { title } = c.req.valid('json')  // title: string
    return c.json({ title })
  }
)
```

Validation targets: `'json' | 'query' | 'param' | 'header' | 'form' | 'cookie'`

### c.req.path

Get request path:

```ts
c.req.path  // '/users/123'
```

### c.req.method

Get HTTP method:

```ts
c.req.method  // 'GET', 'POST', etc.
```

### c.req.raw

Get raw Request object:

```ts
const raw = c.req.raw
// Web standard Request object
```

## Response Setting

### c.header(key, value)

Set response header:

```ts
c.header('X-Custom-Header', 'value')
c.header('Content-Type', 'application/json')
c.header('Cache-Control', 'max-age=3600')
```

### c.status(status)

Set response status code (used after chaining response methods):

```ts
c.status(201)
return c.json({ id: '123' })  // 201 Created
```

### c.cookie(name, value, options?)

Set cookie:

```ts
c.cookie('session', 'abc123')
c.cookie('theme', 'dark', {
  path: '/',
  httpOnly: true,
  secure: true,
  sameSite: 'Strict',
  maxAge: 60 * 60 * 24,
})
```

Delete cookie:
```ts
c.cookie('session', '', { maxAge: 0 })
```

## Variable Storage (Context Variables)

### c.set(key, value) / c.get(key)

Share data between middleware and handlers:

```ts
// Middleware sets
app.use('*', async (c, next) => {
  c.set('requestId', crypto.randomUUID())
  await next()
})

// Handler reads
app.get('/api', (c) => {
  const id = c.get('requestId')
  return c.json({ requestId: id })
})
```

### c.var

Direct variable access (recommended):

```ts
app.use('*', async (c, next) => {
  c.set('user', { id: 1, name: 'Alice' })
  await next()
})

app.get('/profile', (c) => {
  const user = c.var.user  // { id: 1, name: 'Alice' }
  return c.json(user)
})
```

## Renderer

Used with JSX, sets global rendering template:

```ts
app.use('*', async (c, next) => {
  c.setRenderer((content) => {
    return c.html(
      <html>
        <head><title>My App</title></head>
        <body>{content}</body>
      </html>
    )
  })
  await next()
})

// Now can use c.render() directly
app.get('/about', (c) => {
  return c.render(<h1>About</h1>)
})
```

## Environment

### c.env

Access runtime environment variables/bindings:

```ts
// Cloudflare Workers
c.env.MY_KV  // KVNamespace
c.env.MY_D1  // D1Database

// Node.js
c.env.API_KEY

// Type extension
type Env = {
  Bindings: {
    MY_KV: KVNamespace
  }
}
const app = new Hono<{ Bindings: { MY_KV: KVNamespace } }>()
```

## Execution Context (Cloudflare Workers)

### c.executionCtx

Access execution context:

```ts
app.get('/stream', async (c) => {
  const { waitUntil, passThroughOnException } = c.executionCtx
  
  waitUntil(someAsyncOperation())
  passThroughOnException()
  
  return c.body(stream)
})
```

## Context Chaining

Most methods return Context, supporting chaining:

```ts
c.header('X-Request-Id', id)
  .header('X-Response-Time', `${duration}ms`)
  .json({ ok: true })
```

But usually you just `return` a Response directly.

## Context Type Extension

```ts
type MyEnv = {
  Variables: {
    user: { id: number; name: string }
    requestId: string
  }
  Bindings: {
    MY_KV: KVNamespace
  }
}

const app = new Hono<MyEnv>()
```

## Common Patterns

### JSON Response Wrapper

```ts
// Custom helper
const json = (data: any, status = 200) => c.json(data, status)

app.get('/users', (c) => json({ users: [] }))
app.post('/users', (c) => json({ user: { id: '1' } }, 201))
```

### Error Handling

```ts
class HttpError extends Error {
  constructor(public status: number, message: string) {
    super(message)
  }
}

app.onError((err, c) => {
  if (err instanceof HttpError) {
    return c.json({ error: err.message }, err.status)
  }
  console.error(err)
  return c.json({ error: 'Internal Server Error' }, 500)
})

app.get('/users/:id', (c) => {
  const user = db.find(c.req.param('id'))
  if (!user) throw new HttpError(404, 'User not found')
  return c.json({ user })
})
```

### Async Handler

```ts
app.get('/user/:id', async (c) => {
  const id = c.req.param('id')
  
  try {
    const user = await userService.findById(id)
    if (!user) return c.json({ error: 'Not found' }, 404)
    return c.json({ user })
  } catch (err) {
    throw err  // pass to onError
  }
})
```
