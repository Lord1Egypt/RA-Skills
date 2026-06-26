# Hono Middleware

## Built-in Middleware Import Paths

All built-in middleware imported from `hono/middleware`:

```ts
import {
  cors,
  logger,
  etag,
  jwt,
  bearerAuth,
  basicAuth,
  compress,
  secureHeaders,
  cache,
  bodyLimit,
  prettyJSON,
  requestId,
  timing,
  ipRestriction,
  language,
  contextStorage,
  trailingSlash,
  methodOverride,
  combine,
  timeout,
} from 'hono/middleware'
```

## CORS

```ts
import { cors } from 'hono/middleware'

// Allow all origins (dev)
app.use('*', cors())

// Production config
app.use('*', cors({
  origin: 'https://example.com',
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowHeaders: ['Content-Type', 'Authorization'],
  exposeHeaders: ['X-Custom-Header'],
  maxAge: 86400,
  credentials: true,
}))
```

## Logger

```ts
import { logger } from 'hono/middleware'

app.use('*', logger())

// Custom format
app.use('*', logger((c, next) => {
  const start = Date.now()
  await next()
  console.log(`${c.req.method} ${c.req.path} - ${Date.now() - start}ms`)
}))
```

## ETag

```ts
import { etag } from 'hono/middleware'

app.use('*', etag())

app.get('/api', (c) => c.json({ hello: 'world' }))
// Auto-generates ETag, supports conditional requests (If-None-Match)
```

## JWT Auth

```ts
import { jwt } from 'hono/middleware'
import { signingKey } from './constants'

app.use('/api/*', jwt({ secret: signingKey }))

app.get('/api/secret', (c) => {
  const payload = c.var.jwtPayload
  return c.json({ userId: payload.sub })
})
```

## Bearer Auth

```ts
import { bearerAuth } from 'hono/middleware'

app.use('/api/*', bearerAuth({ token: 'my-secret-token' }))

// Or dynamic verification
app.use('/api/*', bearerAuth({
  verify: async (token, c) => {
    return token === await getValidToken()
  }
}))
```

## Basic Auth

```ts
import { basicAuth } from 'hono/middleware'

app.use('*', basicAuth({
  username: 'admin',
  password: 'secret-password',
}))

// Dynamic verification
app.use('*', basicAuth({
  verify: async (username, password, c) => {
    return username === 'admin' && password === await getPassword()
  }
}))
```

## Cache

```ts
import { cache } from 'hono/middleware'

// Memory cache
app.get('/static/*', cache())

// Custom strategy
app.get('/static/*', cache({
  cacheName: 'my-cache',
  maxAge: 60 * 60 * 24,  // 24 hours
  wait: true,              // wait for fresh content
  cacheControl: 'max-age=86400',
}))
```

## Body Limit

```ts
import { bodyLimit } from 'hono/middleware'

app.use('*', bodyLimit({ maxSize: 1024 * 1024 }))  // 1MB
```

## Compress

```ts
import { compress } from 'hono/middleware'

app.use('*', compress())
// Auto gzip/deflate
```

## Secure Headers

```ts
import { secureHeaders } from 'hono/middleware'

app.use('*', secureHeaders())

// Custom config
app.use('*', secureHeaders({
  crossOriginEmbedderPolicy: false,
  crossOriginResourcePolicy: { policy: 'cross-origin' },
  crossOriginOpenerPolicy: 'same-origin',
  contentSecurityPolicy: {
    defaultSrc: "'self'",
    scriptSrc: "'self' 'unsafe-inline'",
  },
  xFrameOptions: 'DENY',
  xContentTypeOptions: 'nosniff',
  referrerPolicy: 'no-referrer',
}))
```

## Request ID

```ts
import { requestId } from 'hono/middleware'

app.use('*', requestId())

app.get('/', (c) => {
  const id = c.req.header('X-Request-Id')
  return c.json({ requestId: id })
})
```

## Timing

```ts
import { timing } from 'hono/middleware'

app.use('*', timing())
// Adds X-Response-Time header with DNS, TCP, TLS, Time-To-First-Byte info
```

## IP Restriction

```ts
import { ipRestriction } from 'hono/middleware'

app.use('*', ipRestriction({
  allowList: ['127.0.0.1', '::1'],
  // or
  denyList: ['192.168.1.0/24'],
}))
```

## Pretty JSON

```ts
import { prettyJSON } from 'hono/middleware'

app.use('*', prettyJSON())
// Only prettifies output when Accept: application/json and format=pretty
```

## Trailing Slash

```ts
import { trailingSlash } from 'hono/middleware'

app.use('*', trailingSlash())
// /users/ -> /users
// /users -> /users/ (configurable)
```

## Method Override

```ts
import { methodOverride } from 'hono/middleware'

app.use('*', methodOverride())
// Allows method override via _method query param or X-HTTP-Method-Override header
```

## Timeout

```ts
import { timeout } from 'hono/middleware'

app.use('*', timeout(30 * 1000))  // 30 second timeout
// Returns 503 Service Unavailable on timeout
```

## Context Storage

```ts
import { contextStorage } from 'hono/middleware'

app.use('*', contextStorage())

// Store data in context, survives async boundaries
```

## Combine

```ts
import { combine } from 'hono/middleware'

app.use('*', combine(
  cors(),
  logger(),
  requestId(),
))
```

## Language

```ts
import { language } from 'hono/middleware'

app.use('*', language())
// Sets c.var.language based on Accept-Language header
```

## Custom Middleware

```ts
// Sync middleware
app.use('*', async (c, next) => {
  // pre logic
  const start = Date.now()
  
  await next()  // call subsequent handlers
  
  // post logic
  c.header('X-Response-Time', `${Date.now() - start}ms`)
})

// Async middleware
app.use('*', async (c, next) => {
  const data = await fetchFromExternalService()
  c.set('externalData', data)
  await next()
})

// Conditional middleware
app.use('/api/*', authenticate())
```

## Middleware and Context

```ts
// Set values for downstream handlers
app.use('*', async (c, next) => {
  c.set('user', { id: 1, name: 'Alice' })
  c.set('requestId', crypto.randomUUID())
  await next()
})

app.get('/profile', (c) => {
  const user = c.var.user  // type-safe
  return c.json(user)
})
```

## Environment Variable Type Extensions

```ts
type Env = {
  Variables: {
    user: { id: number; name: string }
    requestId: string
  }
  Bindings: {
    MY_KV: KVNamespace
  }
}

const app = new Hono<{ Variables: { user: User } }>()
```

## Error Handling in Middleware

```ts
app.use('*', async (c, next) => {
  try {
    await next()
  } catch (err) {
    if (err instanceof ValidationError) {
      return c.json({ error: 'Validation failed' }, 400)
    }
    throw err  // pass to onError
  }
})
```

## Third-party Middleware

Common third-party middleware:
- `@hono/zod-validator` - Zod validation
- `@hono/node-server` - Node.js adapter
- GraphQL Server, Firebase Auth, Sentry, etc.

```ts
import { zValidator } from '@hono/zod-validator'
```
