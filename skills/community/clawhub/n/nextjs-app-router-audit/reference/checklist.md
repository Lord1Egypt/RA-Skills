# App Router review checklist

Items that need human judgment — the scanner can't decide these for you.

## Server / Client boundary
- [ ] `"use client"` sits as low in the tree as possible (leaf islands, not whole pages).
- [ ] No server-only module (DB client, secret env var, `fs`, large SDK) is imported into a `"use client"` file — it gets bundled to the browser.
- [ ] Components that only render props/children stay Server Components.
- [ ] Context providers that wrap the app are thin client wrappers, not whole layouts.

## Data fetching & caching
- [ ] Each `fetch` has an intentional cache mode: `force-cache` (default, static), `no-store` (per request), or `{ next: { revalidate: N } }` (ISR).
- [ ] Independent requests run with `Promise.all`, not awaited one after another.
- [ ] No data fetching in `useEffect` when it could be fetched on the server.
- [ ] `unstable_cache` / `revalidateTag` used for expensive shared queries.

## Rendering & streaming
- [ ] Slow data is wrapped in `<Suspense>` near its use, so the shell streams immediately.
- [ ] Routes have `loading.tsx` where a meaningful skeleton helps perceived performance.
- [ ] `dynamic = 'force-dynamic'` / `export const revalidate` are deliberate, not copy-paste.
- [ ] Dynamic routes use `generateStaticParams` where the set is known at build time.

## Mutations
- [ ] Writes use Server Actions with `revalidatePath`/`revalidateTag`, not client `fetch` to a route handler.
- [ ] Actions validate input and never trust client-supplied IDs without an auth check.

## Assets & Core Web Vitals
- [ ] Images use `next/image` with correct `sizes`; the LCP image has `priority`.
- [ ] Fonts use `next/font` (self-hosted, preloaded, no layout shift).
- [ ] Third-party scripts use `next/script` with the right `strategy`.
- [ ] No large client bundles from importing a whole UI/icon library — import per-component.

## SEO & metadata
- [ ] Every indexable route exports `metadata` or `generateMetadata`.
- [ ] Client pages/layouts do NOT try to export metadata (it's dropped silently).
- [ ] `metadataBase`, canonical, and OpenGraph are set at the root layout.
