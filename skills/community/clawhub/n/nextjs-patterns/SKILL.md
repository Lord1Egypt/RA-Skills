---
name: nextjs-patterns
description: >
  Apply Next.js 15 best practices and modern patterns including App Router,
  Server Components, Server Actions, caching strategies, and performance
  optimization. Use when building or reviewing Next.js 15 applications to
  ensure idiomatic, production-ready code.
---

# Next.js 15 Best Practices

## Core Principles

1. **Default to Server Components** — only add `"use client"` when you need interactivity or browser APIs
2. **Colocate by feature** — keep components, hooks, and utils near the routes that use them
3. **Type everything** — leverage TypeScript with strict mode enabled
4. **Cache deliberately** — understand the four caching layers and opt in/out explicitly

## Project Structure

```
app/
  (marketing)/        # route group: no URL segment
    page.tsx
  (dashboard)/
    layout.tsx
    [id]/
      page.tsx
  api/
    route.ts
components/
  ui/                 # shared, "dumb" UI components
  features/           # feature-specific components
lib/
  db.ts               # database client (singleton)
  auth.ts             # auth helpers
  utils.ts
```

## Server vs. Client Components

```tsx
// ✅ Server Component (default) — runs on server, no JS sent to client
export default async function ProductList() {
  const products = await db.product.findMany()
  return <ul>{products.map(p => <li key={p.id}>{p.name}</li>)}</ul>
}

// ✅ Client Component — only when needed
"use client"
import { useState } from "react"
export function Counter() {
  const [n, setN] = useState(0)
  return <button onClick={() => setN(n + 1)}>{n}</button>
}
```

## Data Fetching Patterns

```tsx
// Parallel fetching (avoid sequential waterfalls)
export default async function Dashboard() {
  const [user, stats] = await Promise.all([
    fetchUser(),
    fetchStats(),
  ])
  return <View user={user} stats={stats} />
}

// fetch with cache control
const data = await fetch("https://api.example.com/data", {
  next: { revalidate: 60 },   // ISR: revalidate every 60s
  // cache: "no-store"         // always fresh
  // cache: "force-cache"      // static, until manual revalidation
})
```

## Server Actions

```tsx
// app/actions.ts
"use server"
import { revalidatePath } from "next/cache"

export async function createPost(formData: FormData) {
  const title = formData.get("title") as string
  await db.post.create({ data: { title } })
  revalidatePath("/posts")
}

// app/posts/new/page.tsx
import { createPost } from "../actions"
export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" />
      <button type="submit">Create</button>
    </form>
  )
}
```

## Metadata & SEO

```tsx
// Static metadata
export const metadata = {
  title: "My App",
  description: "...",
}

// Dynamic metadata
export async function generateMetadata({ params }) {
  const post = await fetchPost(params.slug)
  return { title: post.title, description: post.excerpt }
}
```

## Error & Loading States

```tsx
// app/posts/loading.tsx  — automatic Suspense boundary
export default function Loading() {
  return <Skeleton />
}

// app/posts/error.tsx  — automatic error boundary
"use client"
export default function Error({ error, reset }) {
  return <button onClick={reset}>Retry: {error.message}</button>
}
```

## Performance Checklist

- [ ] Images use `next/image` with explicit `width`/`height`
- [ ] Fonts use `next/font` (zero layout shift)
- [ ] Dynamic imports for heavy client components: `dynamic(() => import(...))`
- [ ] `generateStaticParams` for known dynamic routes
- [ ] Bundle analyzer run: `ANALYZE=true next build`
- [ ] Partial Prerendering (PPR) considered for mixed static/dynamic pages

## References

See `references/` folder for routing patterns, caching deep-dive, and migration guide.
