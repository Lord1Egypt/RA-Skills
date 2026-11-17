# Routing — NextJS

## Special Files

| File | Purpose | Gotcha |
|------|---------|--------|
| `page.tsx` | Route UI; makes the route public | A folder without one is just a path segment |
| `layout.tsx` | Shared UI, preserves state across navigation | Does NOT re-render on navigation within it — never put auth or per-page data here |
| `template.tsx` | Like layout but remounts per navigation | Use for enter animations or state that must reset per page |
| `loading.tsx` | Suspense fallback for the whole segment | Coarse — prefer explicit `<Suspense>` around slow parts (`data-fetching.md`) |
| `error.tsx` | Error boundary (must be `'use client'`) | Doesn't catch errors in the layout of the SAME segment — that needs the parent's boundary |
| `not-found.tsx` | 404 UI; triggered by `notFound()` | `notFound()` throws, like `redirect()` — don't catch it |
| `default.tsx` | Parallel-route fallback | Missing one → hard navigation 404s the whole page |
| `route.ts` | API endpoint | Cannot coexist with `page.tsx` in the same folder |

## Dynamic Routes

```typescript
// app/blog/[slug]/page.tsx — params is a Promise since next 15
export default async function Page({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  return <h1>Post: {slug}</h1>
}

export async function generateStaticParams() {
  const posts = await getPosts()
  return posts.map((post) => ({ slug: post.slug }))
}

export const dynamicParams = true   // unlisted slugs render on demand, then cache (default)
// dynamicParams = false → unlisted slugs 404
```

Without `generateStaticParams`, every slug renders on first request. With it, listed slugs build ahead of time — for large catalogs, return only the top N (best-sellers, recent posts) and let the long tail generate on demand.

Catch-all: `[...categories]` matches `/shop/a`, `/shop/a/b`, … (`categories: string[]`). Optional catch-all `[[...categories]]` also matches `/shop` (undefined).

## Route Groups

```
app/
├── (marketing)/         # No URL impact — layout separation only
│   ├── page.tsx         # /
│   └── layout.tsx
├── (shop)/
│   ├── products/page.tsx  # /products
│   └── layout.tsx
└── layout.tsx           # Root
```

Traps:
- Two pages resolving to the same URL across groups (`(a)/about` and `(b)/about`) → build error.
- Putting separate root layouts inside groups (no top-level `layout.tsx`) works, but navigating between groups becomes a full page load.

## Parallel Routes

Slots (`@name`) render simultaneously in the parent layout — each gets its own loading and error boundary, which is the actual reason to use them (independent failure/streaming per dashboard panel):

```
app/
├── @analytics/page.tsx
├── @analytics/default.tsx    # REQUIRED: fallback on hard navigation
├── @team/page.tsx
├── @team/default.tsx
├── layout.tsx                # receives slots as props
└── page.tsx
```

```typescript
export default function Layout({ children, analytics, team }: {
  children: React.ReactNode
  analytics: React.ReactNode
  team: React.ReactNode
}) {
  return (<>{children}<aside>{analytics}{team}</aside></>)
}
```

Second use: conditional slots — `return session ? dashboard : login` in the layout swaps entire subtrees without URL change.

## Intercepting Routes (the Modal Pattern)

| Convention | Intercepts from |
|------------|-----------------|
| `(.)folder` | Same level |
| `(..)folder` | One level up |
| `(...)folder` | Root |

```
app/
├── feed/page.tsx
├── photo/[id]/page.tsx           # Full page: direct visit, refresh, shared link
├── @modal/(.)photo/[id]/page.tsx # Modal: soft navigation from the feed
└── @modal/default.tsx            # return null — or every other route 404s
```

Why it works: soft navigation renders the interceptor (modal over the feed); hard navigation (refresh, external link) renders the real page. Both must exist and both must render the content — the modal is not a substitute for the page. Close the modal with `router.back()`.

## Navigation

```typescript
import Link from 'next/link'
<Link href="/dashboard" prefetch={false}>Dashboard</Link>

// Client Components only
const router = useRouter()   // from 'next/navigation', NOT 'next/router'
router.push('/x')  router.replace('/x')  router.refresh()  router.back()

// Server Components / Actions / Route Handlers
redirect('/login')            // 307; 303 when called in a Server Action — throws, keep out of try/catch
permanentRedirect('/new-url') // 308
```

Prefetch behavior in production: static routes prefetch fully on viewport entry; dynamic routes prefetch only down to the nearest `loading.tsx`. A list of hundreds of `<Link>`s to dynamic pages = hundreds of prefetch requests — `prefetch={false}` for long lists.

`useRouter` from `next/router` in App Router code is the classic migration error — the import path is `next/navigation`.

## Route Segment Config

Common per-route exports (cache-related ones are canonical in `caching.md`):

```typescript
export const runtime = 'nodejs'        // or 'edge' — see SKILL.md, Where Experts Disagree
export const maxDuration = 30          // seconds; platform caps still apply
export const preferredRegion = 'iad1'  // pin near your database, not near users
```

Pin compute near the database: a page making 5 sequential queries at 80ms cross-region RTT spends 400ms on network alone; same region ≈ under 10ms total.
