---
name: hono
description: "Hono web framework skill for building APIs across all JS runtimes (Cloudflare Workers, Deno, Bun, Node.js, etc.). Covers routing, middleware, JSX, RPC client, Zod validation, and context extensions."
metadata:
  author: yuexiaoliang
  version: "1.0.0"
---

# Hono

Hono (Japanese for "flame" 🔥) is a small, fast web framework built on Web Standards. Works on all JS runtimes.

## Core API

```ts
import { Hono } from 'hono'
const app = new Hono()

app.get('/', (c) => c.text('Hello!'))
app.post('/api', async (c) => c.json({ ok: true }, 201))

export default app
```

### Context Core Methods

```ts
// Responses
c.text(str, status?)       // plain text
c.json(obj, status?)        // JSON
c.html(str)                 // HTML string
c.body(stream, headers?)    // raw body

// Requests
c.req.param('id')          // path params (type-inferred)
c.req.query('name')         // query params
c.req.valid('json')         // validated data (with validator)
c.req.header('x-token')     // request headers
c.req.cookie('session')     // cookies

// Variables/state
c.set('key', value)         // set variable (shared via middleware)
c.get('key')                // get variable
c.var.foo                   // access middleware-set variable

// Other
c.notFound()                // 404 (avoid in RPC)
c.redirect('/path', 302)    // redirect
```

## Routing

```ts
// Basic routes
app.get('/users/:id', (c) => c.json({ id: c.req.param('id') }))

// Regex routes
app.get('/posts/:id{.+}', (c) => { /* matches /posts/a/b/c */ })

// Route grouping
const api = new Hono()
api.get('/posts', ...)
api.get('/users', ...)
app.route('/api', api)

// HTTP methods
app.get|post|put|patch|delete|options|head

// Multiple paths
app.get(['/home', '/'], (c) => c.text('Home'))
```

## Project Creation

```bash
# npm
npm create hono@latest my-app -- --template cloudflare-workers --pm npm --install

# bun
bun create hono@latest my-app

# Common templates: cloudflare-workers, bun, deno, vercel, aws-lambda, nodejs
```

**npm create arg passing**: npm requires `--`, others optional. `--template` selects template, `--pm` specifies package manager, `--install` auto-installs deps.

## Large Application Structure

**Recommended**: Use `app.route()` for modular apps, not RoR-style Controllers (type inference breaks).

```ts
// authors.ts - separate Hono instance per module
const app = new Hono()
  .get('/', (c) => c.json('list'))
  .post('/', (c) => c.json('create', 201))
  .get('/:id', (c) => c.json(c.req.param('id')))

export default app
export type AppType = typeof app
```

```ts
// index.ts - compose
import authors from './authors'
const app = new Hono()
app.route('/authors', authors)
export default app
```

**RPC**: Chain methods to export types:
```ts
const route = app.get('/', (c) => c.json({ ok: true }))
export type AppType = typeof route  // or typeof app
```

## Middleware

```ts
// Built-in
import { cors, logger, etag } from 'hono/middleware'
app.use('*', cors(), logger(), etag())

// Custom
app.use('*', async (c, next) => {
  c.set('requestId', crypto.randomUUID())
  await next()
})

// Path-specific
app.use('/api/*', authenticate())

// Error handling
app.onError((err, c) => {
  return c.json({ error: err.message }, 500)
})
```

Common built-in middleware: cors, jwt, bearer-auth, basic-auth, logger, etag, secure-headers, cache, compress, body-limit, pretty-json, timing, request-id, ip-restriction

## Validators

```ts
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

app.post('/posts',
  zValidator('json', z.object({ title: z.string(), body: z.string() })),
  (c) => {
    const { title, body } = c.req.valid('json')
    return c.json({ ok: true }, 201)
  }
)

export type AppType = typeof app  // export for client
```

Validation targets: `json`, `form`, `query`, `param`, `header`, `cookie`

## RPC Client

```ts
import { hc } from 'hono/client'
import type { AppType } from './server'

const client = hc<AppType>('http://localhost:8787/')

// Request
const res = await client.posts.$post({
  json: { title: 'Hello', body: 'Hono!' }
})

// Response
if (res.ok) {
  const data = await res.json()
}
```

**Don't use `c.notFound()` in RPC mode** — use `c.json(..., 404)` instead, or type inference breaks.

Path params use `param`, queries use `query`, forms use `form`, JSON use `json`.

## JSX

```tsx
import { Hono } from 'hono'
import type { FC } from 'hono/jsx'

const app = new Hono()

const Layout: FC = (props) => (
  <html><body>{props.children}</body></html>
)

app.get('/', (c) => c.html(<Layout><h1>Hello!</h1></Layout>))
```

tsconfig.json needs:
```json
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "hono/jsx"
  }
}
```

## Helpers

| Helper | Purpose |
|--------|---------|
| `html` | Template literal HTML |
| `cookie` | Cookie read/write |
| `jwt` | JWT encode/decode |
| `ssg` | Static site generation |
| `streaming` | Streaming responses |
| `accepts` | Content negotiation |
| `factory` | Reusable handlers (preserves type inference) |

## Context Extensions (Variable Types)

```ts
// Define types
type Env = { Variables: { user: User } }

// Use
const app = new Hono<{ Variables: { user: User } }>()

app.use('*', async (c, next) => {
  c.set('user', { id: 1, name: 'Alice' })
  await next()
})

app.get('/me', (c) => c.json(c.var.user))
```

## Testing

```ts
// Method 1: app.request()
const res = await app.request('/api/posts?page=1', {
  method: 'POST',
  body: JSON.stringify({ title: 'Hello' }),
  headers: { 'Content-Type': 'application/json' }
})

// Method 2: fetch style
const res = await fetch('/api/posts', {
  method: 'POST',
  body: JSON.stringify({ title: 'Hello' })
})
const data = await res.json()
```

## Reference Docs

Detailed docs loaded on demand:
- [Routing](references/routing.md)
- [Middleware](references/middleware.md)
- [Helpers](references/helpers.md)
- [RPC/Client](references/rpc.md)
- [Context API](references/context.md)
