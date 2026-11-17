# Deployment — NextJS

## Pick the Output Mode

| Situation | Mode |
|-----------|------|
| Vercel | Default output; zero config |
| Docker / any Node host | `output: 'standalone'` |
| No server features needed (pure static site) | `output: 'export'` → any static host |
| **Default when unsure** | `standalone` — keeps every feature, runs anywhere Node runs |

## Standalone (the fragile part — copy exactly)

```javascript
// next.config.js
module.exports = { output: 'standalone' }
```

```bash
npm run build
# REQUIRED: standalone does NOT include static assets
cp -r .next/static .next/standalone/.next/static
cp -r public .next/standalone/public
node .next/standalone/server.js   # port 3000; set HOSTNAME=0.0.0.0 in containers
```

Skipping the two `cp` lines is the #1 standalone failure: the app boots, pages render, but all JS/CSS 404s.

## Docker

```dockerfile
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT=3000 HOSTNAME="0.0.0.0"
CMD ["node", "server.js"]
```

`.dockerignore`: `node_modules`, `.next`, `.git`.

**Build-time trap:** `next build` pre-renders static pages, so any page touching the database at build needs a reachable `DATABASE_URL` *inside the builder stage* — or mark those routes `dynamic = 'force-dynamic'` so they render at request time. A build that "works locally, fails in CI" with connection errors is this.

## Environment Variables

```
Loading order (first wins):
1. .env.local            (gitignored; not loaded in test)
2. .env.[environment].local
3. .env.[environment]
4. .env
```

- No prefix → server only. `NEXT_PUBLIC_` → **inlined into the client bundle at build time** (SKILL.md Rule 8).
- Consequence for Docker: if any `NEXT_PUBLIC_` var differs between staging and prod, one image cannot serve both — either build per environment, or keep runtime config server-side and pass it via a Server Component.
- Server-side `process.env` reads are runtime on dynamic routes — those you can override at deploy.

## Self-Hosted ISR and Caching

- ISR state lives in `.next/cache` — persist it across deploys or every deploy cold-starts all ISR pages.
- **Multiple instances = divergent caches**: each pod regenerates independently, so two users can see different "latest" pages, and `revalidateTag` only purges the instance that ran it. Fix: shared cache via a custom `cacheHandler` in `next.config` (Redis is the usual backend) — or accept the drift for low-write content.
- Image optimization: `next >=15` bundles sharp automatically; on 14 self-hosted, install `sharp` explicitly or optimization falls back to a much slower path.

## Reverse Proxy (nginx)

Standard proxy directives work; the Next.js-specific mistake is buffering:

```nginx
location / {
    proxy_pass http://localhost:3000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_buffering off;   # buffering holds the response until complete — kills streaming/Suspense
}
```

If streaming works locally but pages "hang then appear all at once" behind the proxy, buffering (nginx, or a CDN in front) is the cause.

## Static Export

```javascript
module.exports = { output: 'export' }   // output in /out
```

Loses: route handlers, Server Actions, ISR/revalidation, middleware, image optimization (needs a custom loader), dynamic routes without `generateStaticParams`. If the site needs any of these, it isn't a static-export project — use standalone.

## Health Check

```typescript
// app/api/health/route.ts
export async function GET() {
  try {
    await db.$queryRaw`SELECT 1`
    return Response.json({ status: 'healthy' })
  } catch (e) {
    return Response.json({ status: 'unhealthy' }, { status: 503 })
  }
}
```

Point container orchestration/load balancer probes here, not at `/` — the home page being cached can mask a dead database.

## Process Manager (bare metal)

```javascript
// ecosystem.config.js — PM2 cluster across cores
module.exports = {
  apps: [{
    name: 'nextjs-app',
    script: '.next/standalone/server.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: { NODE_ENV: 'production', PORT: 3000 },
  }],
}
```

Cluster mode multiplies the ISR cache-divergence problem above — same fix (shared cacheHandler) applies.

## Pre-Deploy Checklist

- [ ] `next build` clean locally — build errors never get better in CI
- [ ] Build output symbols match intent: `○`/`●` for content pages, `ƒ` only where expected (`caching.md`, Debugging)
- [ ] Cache behavior verified with `next build && next start`, not dev
- [ ] Secrets have no `NEXT_PUBLIC_` prefix; grep the client bundle if unsure
- [ ] Standalone: static + public copied; container sets `HOSTNAME=0.0.0.0`
- [ ] Multi-instance: ISR cache strategy decided (shared handler vs accepted drift)
