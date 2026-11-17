---
name: nextjs
slug: nextjs
version: 1.1.2
description: Builds Next.js apps with App Router — server components, caching, Server Actions, auth, deployment. Use for any Next.js routing, data, cache, or build issue.
homepage: https://clawic.com/skills/nextjs
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
metadata:
  clawdbot:
    emoji: ⚡
    requires:
      bins: []
    os:
    - linux
    - darwin
    - win32
    displayName: NextJS
---

## Setup

All persistent data for this skill lives in `~/Clawic/data/nextjs/`. On first use, read `setup.md` for project integration.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/nextjs/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| package_manager | npm \| pnpm \| yarn \| bun | npm | Selects install/run command syntax, lockfile references, and Docker `corepack`/cache-mount advice |
| deployment_target | vercel \| docker \| standalone \| static-export | vercel | Drives build config (`output` mode), env-var handling, and which parts of `deployment.md` apply; static-export disables SSR/ISR/Server Actions guidance |
| styling | tailwind \| css-modules \| styled-components \| vanilla-extract | tailwind | Shapes styling examples and the RSC-compatibility caveats (styled-components needs a client boundary/registry) |
| component_naming | PascalCase \| kebab-case | PascalCase | Sets filenames used in generated components and import examples |
| folder_convention | feature-folders \| type-folders | feature-folders | Governs where new routes, components, and colocated files are placed |

Preference areas to record as the user reveals them:

- **conventions** — component/file naming, folder organization, barrel-file usage
- **stack** — TypeScript, ORM (Prisma/Drizzle), auth library, state management
- **proactivity** — how eagerly to flag caching/boundary/performance issues vs only on request
- **safety posture** — how proactively to surface auth hardening (data-access layer, CVE-2025-29927) vs only when asked

## When To Use

- Building or debugging a Next.js App Router application — routing, rendering, data, deploy
- Boundary errors: "useState only works in Client Components", hydration mismatch, "functions cannot be passed to Client Components"
- Cache surprises: stale pages, data not updating, ISR behaving "randomly"
- Wiring auth: sessions, protected routes, role checks
- Shipping: Vercel, Docker, standalone server, static export
- Not for plain React questions (see `react` skill) or Pages Router deep-dives — App Router is assumed throughout

## Architecture

```
~/Clawic/data/nextjs/
├── memory.md          # Project conventions, patterns
└── projects/          # Per-project learnings
```

See `memory-template.md` for the file formats. If you have data at an old location (`~/nextjs/` or `~/clawic/nextjs/`), move it to `~/Clawic/data/nextjs/`.

## Quick Reference

| Situation | Go to |
|-----------|-------|
| First session with a user or project | `setup.md`, then `memory-template.md` |
| Page slow, sequential awaits, streaming, Server Actions | `data-fetching.md` |
| Stale or over-fresh data, revalidate, ISR, cache debugging | `caching.md` |
| Login, sessions, protected routes, roles | `auth.md` |
| Modals over pages, parallel routes, layouts, navigation | `routing.md` |
| Docker, self-hosting, env vars, static export | `deployment.md` |
| Anything else Next.js | Apply Core Rules below; open the closest file only if they don't settle it |

## Core Rules

### 1. Server by Default, Client at the Leaves
`'use client'` marks a boundary, not one component: everything imported below it ships to the browser. Put interactivity in leaf components; a `'use client'` layout de-RSCs its whole subtree.

### 2. Parallel Fetches or You Pay the Sum
Sequential awaits cost sum(t1..tn); `Promise.all` costs max(). Three 300ms fetches: 900ms sequential, 300ms parallel. Chain awaits only when one call genuinely needs the other's result.

### 3. One Dynamic Read Poisons the Whole Route
`cookies()`, `headers()`, or an uncached fetch anywhere in the tree — layouts included — forces the entire route to render per-request. Read them in the leaf that needs them, behind `<Suspense>`.

### 4. Dev Lies About Caching
`next dev` renders everything dynamically. Verify cache behavior only with `next build && next start`; debug headers and build-output symbols are in `caching.md`.

### 5. Middleware Redirects, the Data Layer Enforces
Middleware does optimistic cookie checks for UX; every Server Action, route handler, and query re-verifies the session. CVE-2025-29927 let a spoofed request header skip middleware entirely — patched versions and the data-access-layer pattern in `auth.md`.

### 6. Server Actions Are Public Endpoints
Anyone can POST to an action with its id; a hidden button protects nothing. First lines of every action: session check, then input validation.

### 7. Write, Revalidate, Then Redirect
Every mutating action ends with `revalidatePath`/`revalidateTag`, or the UI keeps serving stale cache. `redirect()` throws — call it after the try/catch, never inside one.

### 8. `NEXT_PUBLIC_` Is Baked at Build Time
Inlined into the bundle during `next build`; changing it at runtime does nothing. Unprefixed vars stay server-only — and any differing public var means one Docker image per environment (`deployment.md`).

### 9. Suspense Converts Blocking Into Streaming
TTFB = the slowest await chain outside any Suspense boundary. Wrap each independent slow fetch in its own `<Suspense>` so the shell paints immediately.

## Server vs Client

| Server Component | Client Component |
|------------------|------------------|
| Default in App Router | Requires `'use client'` |
| Can be async | Cannot be async |
| Access backend, env vars | Access hooks, browser APIs |
| Zero JS shipped | JS shipped to browser |

**Decision:** Start Server. Add `'use client'` only for: useState, useEffect, event handlers, browser APIs.

**The boundary is a serialization boundary.** Props crossing server→client must serialize: plain objects, arrays, Date, Map, Set — yes; functions and class instances — no (exceptions: Server Actions passed as props, and Promises, which the client unwraps with `use()`). A Server Component can't be imported into a Client Component — pass it as `children`.

## Version Gates

- `next >=13.4` — App Router stable; everything here assumes it
- `next 14` — `fetch` cached by default (the version where the default flips)
- `next >=15` — `fetch` and GET route handlers uncached by default; `params`/`searchParams` are Promises, `await` them; React 19 (`useActionState`)
- `next >=16` — Turbopack is the default bundler; synchronous `params` access removed; `middleware.ts` renamed `proxy.ts` (old name deprecated)

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| `try/catch` around `redirect()` | it throws `NEXT_REDIRECT`; your catch swallows it | redirect after the try, or rethrow |
| Fetching your own API route from a Server Component | extra HTTP round-trip, lost types | call the DB/function directly |
| `useEffect` for initial data | double round-trip (HTML, then JSON), no streaming | fetch in a Server Component |
| `cookies()` in root layout | whole app goes dynamic (Rule 3) | read in the consuming leaf |
| `new PrismaClient()` at module top level | dev hot-reload piles up connections until the DB refuses | `globalThis` singleton |
| `Date.now()`/`Math.random()` in render | server and client HTML differ → hydration error | compute in `useEffect`, or pass from server as prop |
| Secrets imported into client code | bundled into public JS | `import 'server-only'` in server modules — build fails on misuse |
| `next/image` with `fill` but no `sizes` | srcset assumes 100vw; phones download desktop-size images | set `sizes` to the actual rendered width |
| Heavy work or DB calls in middleware | runs on every matched request, before any cache | optimistic checks only; real work in the route |
| `router.push` in a Server Component | no client router on the server | `redirect()` |

## Where Experts Disagree

| Question | Camps | The boundary |
|----------|-------|--------------|
| Server Actions vs route handlers for mutations | actions-everywhere vs REST | Actions for your own app's forms (progressive enhancement, typed); handlers for webhooks, external clients, explicit status codes |
| Edge vs Node runtime | edge-first vs Node-default | Node unless the route is latency-critical AND every dependency runs on edge; a single native module decides it for you |
| Still need SWR/React Query? | server-only vs client cache | Server fetch for read-mostly pages; reach for a client library only for polling, optimistic UI, or infinite scroll |
| Vercel vs self-host | DX vs cost/control | Vercel to validate; revisit when ISR/image bills grow or compliance demands your infra — the move is covered in `deployment.md` |

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/nextjs (install if the user confirms):
- `react` — React fundamentals and patterns
- `typescript` — Type safety for better DX
- `prisma` — Database ORM for Next.js apps
- `tailwindcss` — Styling with utility classes
- `nodejs` — Server runtime knowledge

## Feedback
- If useful, star it: https://clawic.com/skills/nextjs
- Latest version: https://clawic.com/skills/nextjs

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/nextjs.
