# Hono Helpers

## html - Template Literal HTML

Good for simple templates without full JSX:

```ts
import { Hono } from 'hono'
import { html } from 'hono/html'

const app = new Hono()

const Layout = (props: { title: string; children?: any }) => html`
  <!DOCTYPE html>
  <html>
    <head><title>${props.title}</title></head>
    <body>${props.children}</body>
  </html>
`

app.get('/', (c) => {
  return c.html(
    <Layout title="My Page">
      <h1>Hello!</h1>
      <p>Welcome to Hono</p>
    </Layout>
  )
})
```

Mix with JSX:
```ts
app.get('/mixed', (c) => {
  const content = <div>Content</div>
  return c.html(<Layout>{content}</Layout>)
})
```

## cookie - Cookie Read/Write

```ts
import { cookie } from 'hono/cookie'

// Read
app.get('/', (c) => {
  const sessionId = c.req.cookie('session_id')
  return c.text(sessionId ? `Session: ${sessionId}` : 'No session')
})

// Write
app.post('/login', (c) => {
  c.cookie('session_id', 'abc123', {
    path: '/',
    httpOnly: true,
    secure: true,
    sameSite: 'Strict',
    maxAge: 60 * 60 * 24,  // 1 day
  })
  return c.json({ ok: true })
})

// Delete
app.post('/logout', (c) => {
  c.cookie('session_id', '', { maxAge: 0 })
  return c.text('Logged out')
})
```

**Register middleware first**:
```ts
import { poweredBy } from 'hono/middleware'
app.use('*', cookie())
```

## jwt - JWT Encode/Decode

```ts
import { jwt } from 'hono/jwt'
import { sign, verify } from 'hono/jwt'

const secret = 'my-secret'

// Sign
app.post('/login', (c) => {
  const token = sign({ sub: 'user123', name: 'Alice' }, secret)
  return c.json({ token })
})

// Verify
app.get('/protected', async (c) => {
  const payload = await verify(c.req.header('Authorization')!, secret)
  return c.json({ userId: payload.sub })
})

// With middleware
import { jwt } from 'hono/middleware'
app.use('/api/*', jwt({ secret }))
```

## ssg - Static Site Generation

```ts
import { Hono } from 'hono'
import { ssg } from 'hono/ssg'

const app = new Hono()

app.get('/', (c) => c.html('<h1>Home</h1>'))
app.get('/about', (c) => c.html('<h1>About</h1>'))
app.get('/posts/:id', (c) => {
  const { id } = c.req.param()
  return c.html(`<h1>Post ${id}</h1>`)
})

// Generate static files
await ssg(app, {
  getOrigin: () => 'https://example.com',
  writer: await createWriter(),  // fs, etc.
  routes: [
    { path: '/' },
    { path: '/about' },
    { path: '/posts/1' },
    { path: '/posts/2' },
  ],
})
```

## streaming - Streaming Responses

```ts
import { streaming } from 'hono/streaming'

app.get('/stream', async (c) => {
  return streaming(c, async (stream) => {
    const writer = stream.getWritingWriter()
    for (let i = 0; i < 10; i++) {
      writer.write(`data: ${i}\n\n`)
      await sleep(1000)
    }
    writer.close()
  })
})
```

SSG streaming:
```ts
import { serveStatic } from 'hono/cloudflare-workers'

// SSE example
app.get('/events', async (c) => {
  const { readable, writable } = new TransformStream()
  const writer = writable.getWriter()
  
  // Async write
  ;(async () => {
    for (let i = 0; i < 5; i++) {
      writer.write(`data: message ${i}\n\n`)
      await new Promise(r => setTimeout(r, 1000))
    }
    writer.close()
  })()
  
  return new Response(readable, {
    headers: { 'Content-Type': 'text/event-stream' }
  })
})
```

## accepts - Content Negotiation

```ts
import { accepts } from 'hono/accepts'

app.get('/', (c) => {
  const lang = accepts(c, {
    supports: { language: ['en', 'ja', 'zh'] },
    default: 'en',
  })
  // lang: 'en' | 'ja' | 'zh'
  return c.text(`Language: ${lang}`)
})
```

## factory - Reusable Handlers

Solves RoR-style Controller type inference issues:

```ts
import { createFactory } from 'hono/factory'

const factory = createFactory()

// Middleware factory
const setupAuth = factory.createMiddleware(async (c, next) => {
  const token = c.req.header('Authorization')
  if (!token) return c.text('Unauthorized', 401)
  c.set('user', { id: 1, name: 'Alice' })
  await next()
})

// Handlers factory
const handlers = factory.createHandlers(
  setupAuth,
  (c) => {
    const user = c.var.user
    return c.json(user)
  }
)

app.get('/profile', ...handlers)
```

## conninfo - Connection Info

```ts
import { conninfo } from 'hono/conninfo'

app.use('*', conninfo())

app.get('/', (c) => {
  const { remote, local, major, minor } = c.env.conninfo
  return c.json({ remote, local })
})
```

## proxy - Proxy

```ts
import { proxy } from 'hono/proxy'

app.get('/proxy', proxy('https://api.example.com'))

// With transform
app.get('/api', proxy('https://api.example.com/v1', {
  rewriteRequest: (url) => {
    url.pathname = '/api' + url.pathname
  },
}))
```

## adapter - Runtime Adapters

```ts
// Cloudflare Workers
import { showRoutes } from 'hono/cloudflare-workers'

// Bun
import { serve } from 'hono/bun'

// Node.js
import { serve } from '@hono/node-server'
```

## testing - Testing Helpers

```ts
import { testClient } from 'hono/testing'

const app = new Hono().get('/hello', (c) => c.text('Hi!'))

const client = testClient(app)

// Direct call
const res = await client.hello.$get()
// res.headers.get('Content-Type')
// await res.text() === 'Hi!'

// Request level
const res = await client.request('/hello')
```

## websocket - WebSocket Support

Requires WebSocket-enabled runtime (Cloudflare Workers, etc.):

```ts
import { websocket } from 'hono/websocket'

app.use('/ws', websocket())

// Server
app.ws('/ws', (c) => {
  c.websocket({
    onMessage: (event, ws) => {
      ws.send('pong')
    },
    onClose: () => {},
  })
})
```

## dev - Dev Helpers

```ts
import { poweredBy } from 'hono/dev'

app.use('*', poweredBy())  // Adds X-Powered-By header
```
