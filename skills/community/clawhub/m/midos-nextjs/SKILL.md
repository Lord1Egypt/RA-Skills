---
name: nextjs
description: Next.js 15/16 App Router patterns — async APIs, caching semantics, Turbopack, Server Components, Route Handlers, and migration from v14
version: 1.0.0
tags:
  - nextjs
  - react
  - web-development
  - frontend
  - midos
---

# Next.js App Router Production Patterns

## Description

Production Next.js patterns for the App Router era (v15/v16). Covers the critical breaking changes from v14 (async request APIs, uncached-by-default semantics), Turbopack performance improvements, React 19 integration, Route Handler caching strategies, and Server/Client Component boundaries. Validated against official releases with 0.96 confidence.

## Usage

Install this skill to get production-ready Next.js patterns including:
- Async cookies(), headers(), params, searchParams migration from v14
- Explicit cache configuration for Route Handlers (uncached by default in v15+)
- Turbopack setup (76% faster startup, 96% faster HMR)
- Server Component patterns for data fetching
- Complete migration checklist from v14 to v15/v16

When working on Next.js projects, this skill provides context for:
- Avoiding the most common hydration and async API errors
- Configuring staleTime for the client router cache
- Using instrumentation.js for APM and observability setup
- Choosing when to use force-static vs force-dynamic vs revalidate

## Key Patterns

### Breaking Change: Async Request APIs

CRITICAL: cookies(), headers(), params, and searchParams are now async.

```typescript
// WRONG (Next.js 14 style)
export function AdminPanel() {
  const cookieStore = cookies(); // Synchronous -- no longer works
  const token = cookieStore.get('token');
  return <div>Token: {token?.value}</div>;
}

// CORRECT (Next.js 15+ style)
export async function AdminPanel() {
  const cookieStore = await cookies(); // Must await
  const token = cookieStore.get('token');
  return <div>Token: {token?.value}</div>;
}
```

Automated migration (handles ~95% of cases):
```bash
npx @next/codemod@canary next-async-request-api
```

All affected APIs: `cookies()`, `headers()`, `draftMode()`, `params`, `searchParams` -- all must be awaited.

### Breaking Change: Caching Semantics

GET Route Handlers and `fetch()` are uncached by default in v15+.

```typescript
// Next.js 14: cached automatically (dangerous assumption)
export async function GET() {
  const data = await fetch('https://api.example.com/data');
  return Response.json(data);
}

// Next.js 15+: explicitly opt into caching
export const revalidate = 60; // Cache for 60 seconds
export async function GET() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 60 }
  });
  return Response.json(await data.json());
}

// Or: cache forever
export const dynamic = 'force-static';

// Or: never cache (user-specific data)
export const dynamic = 'force-dynamic';
```

Restore v14 client router cache behavior if needed:
```javascript
// next.config.js
module.exports = {
  experimental: {
    staleTimes: { dynamic: 30, static: 180 },
  },
};
```

### Server Component with Async APIs

```typescript
// app/dashboard/page.tsx
import { cookies, headers } from 'next/headers';

export default async function Dashboard() {
  const cookieStore = await cookies();
  const headersList = await headers();
  const token = cookieStore.get('session');
  const userAgent = headersList.get('user-agent');
  return <div><h1>Dashboard</h1><p>Session: {token?.value}</p></div>;
}
```

### Dynamic Route with Params

```typescript
// app/blog/[slug]/page.tsx
interface PageProps {
  params: Promise<{ slug: string }>;
}

export default async function BlogPost({ params }: PageProps) {
  const { slug } = await params;  // Must await in v15+
  const post = await fetch(`https://api.com/posts/${slug}`);
  return <article>{/* ... */}</article>;
}
```

### Turbopack (Development Performance)

```bash
next dev --turbo   # Enable Turbopack (default in dev for v15+)
next build         # Still uses Webpack for production
```

Performance gains: 76% faster local server startup, 96% faster HMR, 45% faster initial route compilation.

### instrumentation.js (Observability)

```javascript
// instrumentation.js (project root)
export async function register() {
  if (process.env.NEXT_RUNTIME === 'nodejs') {
    const { setupMonitoring } = await import('./monitoring');
    setupMonitoring(); // DataDog, Sentry, New Relic, etc.
  }
}
```

### Common Pitfalls

Pitfall 1: Forgetting await
```typescript
const cookieStore = cookies();          // Wrong -- Object is possibly 'Promise'
const cookieStore = await cookies();    // Correct
```

Pitfall 2: Caching user-specific data
```typescript
// WRONG: caches data that differs per user
export const revalidate = 3600;
export async function GET(request: Request) {
  const userId = request.headers.get('x-user-id');
  const data = await getUserData(userId); // Different per user!
  return Response.json(data);
}

// CORRECT
export const dynamic = 'force-dynamic';
```

Pitfall 3: App Router requires React 19
```bash
npm install next@latest react@latest react-dom@latest
```

### Migration Checklist: v14 to v15/v16

- Run: `npx @next/codemod@canary upgrade latest`
- Run: `npx @next/codemod@canary next-async-request-api`
- Audit GET Route Handlers: add explicit `revalidate` or `dynamic`
- Upgrade to Node.js 18.18+
- Test client router cache behavior (add `staleTimes` config if needed)
- Test with Turbopack: `next dev --turbo`
- Run production build: `next build && next start`
- Verify all dynamic routes resolve params correctly

## Tools & References

- [Next.js Official Docs](https://nextjs.org/docs)
- [Next.js 15 Release Blog](https://nextjs.org/blog/next-15)
- [Codemods Reference](https://nextjs.org/docs/app/building-your-application/upgrading/codemods)
- `npx @next/codemod@canary upgrade latest` -- automated version upgrade

---
*Published by [MidOS](https://midos.dev) — MCP Community Library*
