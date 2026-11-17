# Caching — NextJS

Four caches, four clearing mechanisms. Most "Next.js cache bugs" are someone reasoning about the wrong layer.

## The Four Caches

| Cache | Where | Holds | Cleared by |
|-------|-------|-------|------------|
| Request memoization | Server, per render pass | Identical `fetch`/`cache()` calls | Automatically at end of render |
| Data Cache | Server, persistent | `fetch` results, `unstable_cache` | `revalidate` window, `revalidateTag`/`revalidatePath` |
| Full Route Cache | Server, persistent | HTML + RSC payload of static routes | Revalidating its data; invalidated on deploy |
| Router Cache | Client memory | Visited/prefetched RSC payloads | `router.refresh()`, revalidate inside a Server Action, session end |

On Vercel, the Data Cache survives deployments; the Full Route Cache does not. A deploy that "didn't update the page" usually means a cached `fetch` inside it — tag it and revalidate.

## Choosing a Strategy

| Content | Strategy |
|---------|----------|
| Marketing, blog, docs — updates via deploy or CMS webhook | Static + `revalidateTag` from a webhook handler |
| Listings your own app writes to | Cached fetches with tags; every mutating action revalidates its tags |
| Per-user or personalized | Dynamic route; cache the shared parts with `unstable_cache`; stream user parts behind `<Suspense>` |
| Dashboards where 1–5 min staleness is acceptable | `revalidate: 60`–`300` |
| Payments, auth, anything wrong-if-stale | `cache: 'no-store'` and/or `dynamic = 'force-dynamic'` |
| **Default when unsure** | Uncached (the 15+ default) — correctness first; add caching where measured latency hurts |

## Revalidate Semantics — the Part Everyone Gets Wrong

- **ISR is stale-while-revalidate, not a timer.** Nothing regenerates until a request arrives after the window. Worked example: `revalidate: 300`, regeneration takes 2s → a visitor at t=310 still gets the t=0 page and triggers background regen; the *next* visitor gets fresh. Max staleness ≈ revalidate + gap-to-next-request + regen time.
- **Pick revalidate = maximum staleness you can defend**, not "how often data changes". If your own app performs the writes, use tags + on-demand revalidation and a long (or no) time window.
- **Shortest revalidate wins per route**: fetch with 30s + fetch with 60s → the whole page regenerates at 30s.

```typescript
const data = await fetch(url)                              // uncached (15+ default)
const data = await fetch(url, { cache: 'force-cache' })    // cached until revalidated
const data = await fetch(url, { next: { revalidate: 60 } })// time-based
const data = await fetch(url, { next: { tags: ['posts'] } })// on-demand via tag
```

## On-Demand Revalidation

Tag by entity AND collection — invalidate both on mutation:

```typescript
fetch(url, { next: { tags: ['posts', `post-${id}`] } })

// Server Action
export async function updatePost(id: string, data: PostInput) {
  await db.post.update({ where: { id }, data })
  revalidateTag(`post-${id}`)
  revalidateTag('posts')
}
```

`revalidatePath` scopes:

```typescript
revalidatePath('/blog')                 // one page
revalidatePath('/blog/[slug]', 'page')  // all pages of a dynamic route
revalidatePath('/blog', 'layout')       // layout and everything under it
revalidatePath('/', 'layout')           // entire site
```

**Invisible distinction:** called inside a **Server Action**, `revalidatePath`/`revalidateTag` also purge the client Router Cache — the user sees fresh data immediately. Called inside a **route handler** (e.g. a webhook), they only invalidate the server caches; open browser tabs keep their cached payload until refresh or next navigation.

Webhook handler:

```typescript
export async function POST(request: Request) {
  const secret = request.headers.get('x-revalidate-secret')
  if (secret !== process.env.REVALIDATE_SECRET) {
    return Response.json({ error: 'Invalid secret' }, { status: 401 })
  }
  revalidateTag('posts')
  return Response.json({ revalidated: true })
}
```

## Caching Non-Fetch Work

`fetch` is the only thing the Data Cache sees automatically. Database queries need explicit wrapping:

```typescript
import { unstable_cache } from 'next/cache'

const getCachedUser = unstable_cache(
  async (id: string) => db.user.findUnique({ where: { id } }),
  ['user'],                       // cache key parts (args are appended)
  { tags: ['users'], revalidate: 60 }
)
```

Successor: the `'use cache'` directive (experimental in 15, behind `cacheComponents` in 16). Prefer `unstable_cache` until your version stabilizes it.

**Trap:** `unstable_cache` cannot read `cookies()`/`headers()` inside the wrapped function — pass user-specific inputs as arguments so they become part of the key.

## Router Cache (Client)

Prefetched and visited routes are served from browser memory:

- `next 14` defaults: dynamic segments reused for 30s, static for 5min
- `next >=15` defaults: dynamic 0 (always refetched on navigation), static 5min
- Tune with `experimental.staleTimes` in `next.config`
- `router.refresh()` refetches the current route's server payload without losing client state
- `<Link prefetch={false}>` when a list of hundreds of links would flood a dynamic backend

## Route Segment Config (canonical home)

```typescript
export const dynamic = 'force-dynamic'   // per-request; also: 'force-static', 'error'
export const revalidate = 60             // seconds; false = never, 0 = always
export const fetchCache = 'force-no-store' // override every fetch in the segment
export const dynamicParams = false       // 404 for params not in generateStaticParams
```

## Debugging

- **Trust only production behavior**: `next build && next start` (SKILL.md Rule 4).
- **Read the build output symbols**: `○` static, `●` SSG/ISR, `ƒ` dynamic. A route you expected static showing `ƒ` means something poisoned it — hunt the `cookies()`, `headers()`, or uncached fetch (SKILL.md Rule 3).
- Response headers: `x-nextjs-cache: HIT | MISS | STALE`; on Vercel `x-vercel-cache: HIT | MISS | STALE | PRERENDER`.

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| Expecting `revalidate` to regenerate on a schedule | ISR only regenerates on request after expiry | If you need clock-driven freshness, hit the page or a revalidation webhook from a cron |
| Revalidating from a webhook, users still see old page | Route handlers don't purge the client Router Cache | Accept eventual freshness, or trigger `router.refresh()` on focus client-side |
| Caching a fetch that varies per user | Data Cache is shared across all users | Never `force-cache` anything keyed to a session; cache the shared layer only |
| Testing static/ISR in `next dev` | dev renders everything dynamically | `next build && next start` |
