# Data Fetching — NextJS

Default: fetch on the server, in the component that renders the data. Client fetching is the exception, not the pattern.

## Server-First

```typescript
// Direct in a Server Component — no API route in between
async function Page() {
  const posts = await db.post.findMany()
  return <PostList posts={posts} />
}
```

Never `fetch('/api/...')` from a Server Component to your own app: extra HTTP hop, lost types, and it can't share the render's request memoization. Call the function or query directly.

## Kill the Waterfall

Sequential awaits cost the sum; parallel cost the max (SKILL.md Rule 2):

```typescript
// ✅ 300ms total
const [user, posts, comments] = await Promise.all([getUser(), getPosts(), getComments()])

// ❌ 900ms total — each await blocks the next
const user = await getUser()
const posts = await getPosts()
const comments = await getComments()
```

**Cross-component waterfalls are the invisible kind**: a layout that awaits `getUser()` blocks the page that awaits `getPosts()`. Fix with the preload pattern — start the promise early, await late:

```typescript
export const preloadUser = (id: string) => { void getUser(id) }  // fire, don't await

export default function Layout({ children }) {
  preloadUser('123')          // starts now
  return <>{children}</>      // page's own fetches run concurrently
}
```

## Streaming with Suspense

TTFB equals the slowest await chain outside any Suspense boundary (SKILL.md Rule 9). Each boundary streams independently:

```typescript
export default function Page() {
  return (
    <main>
      <h1>Dashboard</h1>                          {/* paints immediately */}
      <Suspense fallback={<UserSkeleton />}>
        <UserProfile />                            {/* streams when its fetch resolves */}
      </Suspense>
      <Suspense fallback={<PostsSkeleton />}>
        <RecentPosts />                            {/* independent stream */}
      </Suspense>
    </main>
  )
}
```

`loading.tsx` wraps the whole page in one Suspense boundary — coarse. Prefer explicit boundaries around the slow parts so fast content isn't hostage to the slowest fetch.

**Streaming a promise to the client** — start the fetch on the server, resolve in the browser:

```typescript
// Server: don't await
export default function Page() {
  const postsPromise = getPosts()               // no await
  return (
    <Suspense fallback={<Skeleton />}>
      <Posts postsPromise={postsPromise} />
    </Suspense>
  )
}

// Client: unwrap with use()
'use client'
import { use } from 'react'
function Posts({ postsPromise }: { postsPromise: Promise<Post[]> }) {
  const posts = use(postsPromise)
  return <PostList posts={posts} />
}
```

## Deduplication

- Same-URL, same-options `fetch` calls within one render pass are memoized — layout and page can both call `getUser()` for one request.
- Non-fetch work needs `React.cache()`:

```typescript
import { cache } from 'react'
export const getUser = cache(async (id: string) => db.user.findUnique({ where: { id } }))
```

Dedup lasts one render pass only. Persistent caching is the Data Cache's job — `caching.md`.

## Server Actions for Mutations

```typescript
'use server'
export async function createPost(prevState: State, formData: FormData) {
  const session = await auth()                          // Rule 6: actions are public endpoints
  if (!session) return { error: 'Unauthorized' }

  const parsed = PostSchema.safeParse(Object.fromEntries(formData))
  if (!parsed.success) return { error: 'Invalid input' }

  await db.post.create({ data: { ...parsed.data, authorId: session.user.id } })
  revalidateTag('posts')                                // Rule 7: write, revalidate...
  redirect('/posts')                                    // ...then redirect (throws — keep last)
}
```

```typescript
'use client'
import { useActionState } from 'react'                  // next >=15 (React 19)

function NewPost() {
  const [state, formAction, pending] = useActionState(createPost, initialState)
  return (
    <form action={formAction}>
      <input name="title" />
      <button disabled={pending}>{pending ? 'Saving…' : 'Save'}</button>
      {state.error && <p>{state.error}</p>}
    </form>
  )
}
```

Forms with actions work before hydration (progressive enhancement). Use route handlers instead when external clients call you or you need explicit status codes (SKILL.md, Where Experts Disagree).

## Search Params as State

Filters, pagination, and tabs belong in the URL — shareable, back-button-friendly, server-renderable:

```typescript
// Server: read them (Promise since next 15)
export default async function Page({ searchParams }: {
  searchParams: Promise<{ q?: string; page?: string }>
}) {
  const { q, page } = await searchParams
  const results = await search(q, Number(page ?? 1))
  return <Results data={results} />
}

// Client: write them
'use client'
function SearchInput() {
  const searchParams = useSearchParams()
  const router = useRouter()
  function handleSearch(term: string) {
    const params = new URLSearchParams(searchParams)
    term ? params.set('q', term) : params.delete('q')
    router.replace(`?${params.toString()}`)   // replace: don't spam history per keystroke
  }
  return <input defaultValue={searchParams.get('q') ?? ''} onChange={e => handleSearch(e.target.value)} />
}
```

Reading `searchParams` in a page makes it dynamic (SKILL.md Rule 3) — expected for search results.

## Client-Side Fetching — When It's Right

Only for: polling/real-time, optimistic UI, infinite scroll, data that changes on user interaction without navigation. Combine with a server-rendered first paint:

```typescript
// Server fetches initial data...
async function Page() {
  const initialData = await getPosts()
  return <PostsClient initialData={initialData} />
}

// ...client keeps it live
'use client'
function PostsClient({ initialData }) {
  const { data } = useSWR('/api/posts', fetcher, {
    fallbackData: initialData,
    refreshInterval: 30_000,
  })
  return <PostList posts={data} />
}
```

Client fetches need a real endpoint — this is a legitimate use of route handlers.

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| Awaiting in layout what the page also awaits | cross-component waterfall | preload pattern, or move the await down |
| One giant `Promise.all` for the whole page | slowest fetch blocks all content | group per Suspense boundary; parallel within each |
| `use client` component fetching what the parent already had | duplicate request, loading flash | pass data (or the promise) down as props |
| Server Action without session/validation | callable by anyone with the action id | auth + schema-parse as first lines |
| `redirect()` inside try/catch in an action | `NEXT_REDIRECT` swallowed | redirect after the try block |
