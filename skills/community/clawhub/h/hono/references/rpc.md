# Hono RPC / Client

RPC is Hono's core feature: type-safe API calls between server and client through type sharing.

## Basic Usage

### Server Side

```ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

const route = app.post(
  '/posts',
  zValidator('json', z.object({
    title: z.string(),
    body: z.string(),
  })),
  (c) => {
    const { title, body } = c.req.valid('json')
    // ... create post
    return c.json({ id: '123', title, body }, 201)
  }
)

export type AppType = typeof route
```

### Client Side

```ts
import { hc } from 'hono/client'
import type { AppType } from './server'

const client = hc<AppType>('http://localhost:8787/')

// Request is auto-typed
const res = await client.posts.$post({
  json: { title: 'Hello', body: 'Hono is great!' }
})

if (res.ok) {
  const data = await res.json()  // { id: string, title: string, body: string }
  console.log(data.id)  // '123'
}
```

## Complete Example

### Server

```ts
// server/index.ts
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

const PostSchema = z.object({
  id: z.string(),
  title: z.string(),
  body: z.string(),
  createdAt: z.string(),
})

type Post = z.infer<typeof PostSchema>

// List
app.get('/posts', (c) => {
  const posts: Post[] = [{ id: '1', title: 'Hello', body: '...', createdAt: '2024-01-01' }]
  return c.json({ posts })
})

// Single
app.get('/posts/:id', zValidator('param', z.object({ id: z.string() })), (c) => {
  const { id } = c.req.valid('param')
  const post = { id, title: 'Hello', body: '...', createdAt: '2024-01-01' }
  return c.json({ post })
})

// Create
const CreateSchema = z.object({ title: z.string(), body: z.string() })
app.post('/posts', zValidator('json', CreateSchema), (c) => {
  const { title, body } = c.req.valid('json')
  return c.json({ id: crypto.randomUUID(), title, body, createdAt: new Date().toISOString() }, 201)
})

// Delete
app.delete('/posts/:id', zValidator('param', z.object({ id: z.string() })), (c) => {
  const { id } = c.req.valid('param')
  return c.json({ deleted: id })
})

export type AppType = typeof app
```

### Client

```ts
// client/index.ts
import { hc } from 'hono/client'
import type { AppType } from '../server'

const client = hc<AppType>('http://localhost:8787/')

// List
const { posts } = await client.posts.$get().then(r => r.json())

// Single
const { post } = await client.posts[':id'].$get({
  param: { id: '123' }
})

// Create
const res = await client.posts.$post({
  json: { title: 'New Post', body: 'Content' }
})
if (res.status === 201) {
  const { id } = await res.json()
}

// Delete
await client.posts[':id'].$delete({ param: { id: '123' } })
```

## Path Parameters and Queries

```ts
// Path parameters
client.users[':id'].$get({ param: { id: '123' } })

// Query parameters
client.search.$get({ query: { q: 'keyword', page: '1' } })

// JSON body
client.posts.$post({ json: { title: 'Hello' } })

// Form
client.upload.$post({ form: { file: new File([], 'name.txt') } })

// Headers
client.api.$get({}, { headers: { 'X-Token': 'secret' } })

// Combined
client.posts[':id'].$patch({
  param: { id: '123' },
  json: { title: 'Updated' }
})
```

**Note**: All param values are string type (except JSON body values transformed by validator).

## Cookies

```ts
// Server sets cookie
app.post('/login', (c) => {
  c.cookie('session', 'abc123', { httpOnly: true })
  return c.json({ ok: true })
})

// Client sends cookies
const client = hc<AppType>('http://localhost:8787/', {
  init: {
    credentials: 'include'  // crucial!
  }
})

// Subsequent requests include cookies automatically
const res = await client.me.$get()
```

## Status Codes and Response Types

```ts
// Server explicitly returns status codes
app.get('/posts/:id', async (c) => {
  const post = await db.posts.find(c.req.param('id'))
  if (!post) return c.json({ error: 'Not found' }, 404)
  return c.json({ post }, 200)
})

// Client gets different types per status
const res = await client.posts[':id'].$get({ param: { id: '123' } })

if (res.status === 404) {
  const { error } = await res.json()  // { error: string }
}

if (res.ok) {
  const { post } = await res.json()   // { post: Post }
}

// Infer response types
import { InferResponseType } from 'hono/client'

type PostResponse = InferResponseType<typeof client.posts[':id'].$get>
// PostResponse = { post: Post } | { error: string }

type PostResponse200 = InferResponseType<typeof client.posts[':id'].$get, 200>
// PostResponse200 = { post: Post }
```

## Don't Use c.notFound()

In RPC mode, `c.notFound()` return types cannot be correctly inferred by the client. **Use `c.json(obj, 404)` instead**:

```ts
// ❌ Not recommended
app.get('/posts/:id', (c) => {
  const post = db.find(c.req.param('id'))
  if (!post) return c.notFound()  // type lost
  return c.json({ post })
})

// ✅ Recommended
app.get('/posts/:id', (c) => {
  const post = db.find(c.req.param('id'))
  if (!post) return c.json({ error: 'Not found' }, 404)
  return c.json({ post }, 200)
})
```

**Alternative**: Use module augmentation to extend NotFoundResponse type:
```ts
import { Hono, TypedResponse } from 'hono'

declare module 'hono' {
  interface NotFoundResponse extends Response, TypedResponse<{ error: string }, 404, 'json'> {}
}

app.get('/posts/:id', (c) => {
  const post = db.find(c.req.param('id'))
  if (!post) return c.notFound()  // now type-safe
  return c.json({ post }, 200)
})
```

## $url() and $path()

```ts
// $url() - returns URL object (needs absolute URL)
const url = client.posts[':id'].$url({ param: { id: '123' } })
console.log(url.pathname)  // '/posts/123'

// $path() - returns path string (doesn't need base URL)
const path = client.posts[':id'].$path({ param: { id: '123' } })
console.log(path)  // '/posts/123'
```

## Infer Types

```ts
import { InferRequestType, InferResponseType } from 'hono/client'

// Infer request type
type CreatePostRequest = InferRequestType<typeof client.posts.$post>['json']
// { title: string, body: string }

// Infer response type
type PostResponse = InferResponseType<typeof client.posts.$get>
// { posts: Post[] }
```

## Global Error Responses

Use `ApplyGlobalResponse` to merge global error handler types:

```ts
import type { ApplyGlobalResponse } from 'hono/client'

const app = new Hono()
  .get('/users', (c) => c.json({ users: [] }))
  .onError((err, c) => c.json({ error: err.message }, 500))

type AppWithErrors = ApplyGlobalResponse<typeof app, {
  500: { json: { error: string } }
}>

const client = hc<AppWithErrors>('http://localhost')
```

## Monorepo Notes

1. **Hono version must match** (server and client)
2. **tsconfig.json must have `"strict": true`**
3. **Recommend TypeScript Project References** or pre-compiling client

### Pre-compile Client (Recommended for Large Projects)

```ts
// src/client.ts
import { app } from './app'
import { hc } from 'hono/client'

export type Client = ReturnType<typeof hc<typeof app>>
export const hcWithType = (...args: Parameters<typeof hc>): Client =>
  hc<typeof app>(...args)
```

After compile, use anywhere:
```ts
// anywhere
import { hcWithType } from './client'

const client = hcWithType('http://localhost')
const res = await client.posts.$get()
```

## File Upload

```ts
// Client
const file = new File([data], 'upload.png', { type: 'image/png' })
const res = await client.upload.$post({
  form: { file }
})

// Server
app.post('/upload', zValidator('form', z.object({
  file: z.instanceof(File)
})), async (c) => {
  const { file } = c.req.valid('form')
  // process file
  return c.json({ size: file.size })
})
```

## Cancel Requests

```ts
const abortController = new AbortController()

const res = await client.posts.$post({
  json: { title: 'Hello' }
}, {
  init: { signal: abortController.signal }
})

// Cancel
abortController.abort()
```

## Custom Fetch

```ts
// Cloudflare Workers Service Bindings
const client = hc<AppType>('http://localhost', {
  fetch: c.env.AUTH.fetch.bind(c.env.AUTH),
})

// Custom query serialization
const client = hc<AppType>('http://localhost', {
  buildSearchParams: (query) => {
    const sp = new URLSearchParams()
    for (const [k, v] of Object.entries(query)) {
      if (Array.isArray(v)) {
        v.forEach(item => sp.append(`${k}[]`, item))
      } else {
        sp.set(k, v)
      }
    }
    return sp
  },
})
```
