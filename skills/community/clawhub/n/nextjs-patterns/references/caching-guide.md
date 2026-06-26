# Next.js 15 Caching Deep Dive

## The Four Caching Layers

### 1. Request Memoization (in-memory, per request)
Automatically deduplicates identical `fetch()` calls within a single render tree.

```tsx
// Both components call fetchUser(id) — only ONE network request is made
async function Avatar({ id }) { const u = await fetchUser(id); return <img src={u.avatar} /> }
async function Name({ id }) { const u = await fetchUser(id); return <span>{u.name}</span> }
```

### 2. Data Cache (persistent, cross-request)
`fetch()` responses are stored on the server and reused across requests and deployments.

```tsx
// Static — cached indefinitely
fetch(url)
fetch(url, { cache: "force-cache" })

// Time-based revalidation (ISR)
fetch(url, { next: { revalidate: 3600 } }) // revalidate every hour

// Always fresh — no caching
fetch(url, { cache: "no-store" })
fetch(url, { next: { revalidate: 0 } })
```

### 3. Full Route Cache (build-time static rendering)
Pages rendered at build time are stored as static HTML+RSC payload.

```tsx
// Force dynamic rendering for this route
export const dynamic = "force-dynamic"

// Custom revalidation period for the whole route
export const revalidate = 60
```

### 4. Router Cache (client-side, per session)
Browser caches RSC payloads for instant back/forward navigation.
- Static routes: cached for 5 minutes
- Dynamic routes: cached for 30 seconds

## On-Demand Revalidation

```ts
// Revalidate by path
import { revalidatePath } from "next/cache"
revalidatePath("/blog")
revalidatePath("/blog/[slug]", "page")

// Revalidate by cache tag
import { revalidateTag } from "next/cache"
revalidateTag("posts")

// Tagging fetches
fetch(url, { next: { tags: ["posts"] } })
```

## unstable_cache for Non-Fetch Data

```ts
import { unstable_cache } from "next/cache"

const getCachedUser = unstable_cache(
  async (id: string) => db.user.findUnique({ where: { id } }),
  ["user"],
  { revalidate: 300, tags: ["users"] }
)
```

## Common Pitfalls

| Mistake | Fix |
|---------|-----|
| Using `fetch` inside `useEffect` | Move to Server Component or use React Query |
| Forgetting `revalidatePath` after mutations | Call in Server Action after every write |
| Over-caching user-specific data | Add `cache: "no-store"` or check `cookies()`/`headers()` |
| Sequential awaits | Use `Promise.all()` for parallel fetching |
