# Next.js 15 Routing Patterns

## App Router Fundamentals

| File           | Purpose                                      |
|---------------|----------------------------------------------|
| `page.tsx`    | Unique UI for a route, makes it publicly accessible |
| `layout.tsx`  | Shared UI; does NOT re-render on navigation  |
| `template.tsx`| Like layout but re-renders on navigation     |
| `loading.tsx` | Instant loading state (React Suspense)       |
| `error.tsx`   | Error UI boundary (must be Client Component) |
| `not-found.tsx`| 404 UI                                      |
| `route.ts`    | API endpoint (GET, POST, etc.)               |

## Route Groups

```
app/
  (auth)/
    login/page.tsx    → /login
    register/page.tsx → /register
  (app)/
    layout.tsx        ← shared auth-required layout
    dashboard/page.tsx → /dashboard
```

Route groups `(name)` organize routes without affecting the URL.

## Dynamic Routes

```tsx
// app/blog/[slug]/page.tsx
export default function Post({ params }: { params: { slug: string } }) {
  return <h1>{params.slug}</h1>
}

// Generate static routes at build time
export async function generateStaticParams() {
  const posts = await fetchAllPosts()
  return posts.map(p => ({ slug: p.slug }))
}
```

## Catch-All & Optional Catch-All

```
app/shop/[...categories]/page.tsx   → /shop/a/b/c
app/shop/[[...categories]]/page.tsx → /shop AND /shop/a/b/c
```

## Parallel Routes (Advanced)

```
app/
  @team/page.tsx
  @analytics/page.tsx
  layout.tsx           ← receives { team, analytics } props
```

```tsx
// layout.tsx
export default function Layout({ children, team, analytics }) {
  return (
    <div>
      {children}
      <aside>{team}</aside>
      <aside>{analytics}</aside>
    </div>
  )
}
```

## Intercepting Routes

```
app/
  feed/page.tsx
  (..)photo/[id]/page.tsx  ← intercepts /photo/[id] when navigated from /feed
  photo/[id]/page.tsx      ← full page on direct URL visit
```

Useful for modals that maintain background context.

## Middleware

```ts
// middleware.ts (project root)
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  const token = request.cookies.get("token")
  if (!token && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url))
  }
  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*", "/api/protected/:path*"],
}
```

## API Routes (Route Handlers)

```ts
// app/api/posts/route.ts
import { NextRequest, NextResponse } from "next/server"

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const page = searchParams.get("page") ?? "1"
  const posts = await fetchPosts(parseInt(page))
  return NextResponse.json({ posts })
}

export async function POST(request: NextRequest) {
  const body = await request.json()
  const post = await createPost(body)
  return NextResponse.json(post, { status: 201 })
}
```
