```

Next.js App Router audit — 2 files in app/

ERROR client-route-no-metadata  app/dashboard/page.tsx:1
  A Client Component page cannot export `metadata` / `generateMetadata` — its SEO tags are silently dropped.
  fix: Keep page.tsx a Server Component and isolate the interactive bits into a child marked "use client".

WARN raw-img  app/dashboard/page.tsx:15
  Raw <img> skips automatic sizing, lazy-loading and AVIF/WebP — a common CLS/LCP regression.
  fix: Use `next/image` with explicit width/height (or fill).

WARN page-missing-metadata  app/feed/page.tsx:4
  Async page exports no `metadata`/`generateMetadata` — the route ships without title/description.
  fix: Add `export const metadata` or `generateMetadata()` for SEO and social previews.

INFO no-streaming-fallback  app/feed/page.tsx:4
  Async page with no `loading.tsx` — users wait for the whole tree instead of seeing a streamed shell.
  fix: Add a `loading.tsx` beside this page, or wrap slow parts in `<Suspense>`.

INFO request-waterfall  app/feed/page.tsx:5
  2 sequential awaited fetches without Promise.all — likely a request waterfall.
  fix: Kick off independent requests together: `const [a, b] = await Promise.all([...])`.

Summary  1 error  2 warn  2 info   score 73/100

```
