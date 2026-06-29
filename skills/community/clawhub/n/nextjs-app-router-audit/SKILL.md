---
name: nextjs-app-router-audit
description: Audit a Next.js App Router codebase for React Server Component boundary mistakes, request waterfalls, client/server anti-patterns, and Core Web Vitals risks — then propose concrete fixes. Use when the user asks to review/audit a Next.js app, find performance problems, fix slow LCP/CLS/INP, check 'use client' usage, find request waterfalls, improve App Router structure, debug why a page isn't streaming, or why metadata/SEO tags aren't showing. Ships a zero-dependency static scanner (scripts/audit.mjs) plus a manual review methodology for things static analysis can't catch.
---

# Next.js App Router Audit

Find the high-impact correctness and performance problems in a Next.js App Router
codebase, ranked by severity, each with a specific fix. Combine the bundled
scanner (fast, mechanical) with a targeted manual pass (judgment calls the
scanner can't make).

## Step 1 — Run the scanner

The scanner is dependency-free and reads only source files. Point it at the
project root or an `app/` directory:

```bash
node scripts/audit.mjs /path/to/project        # human-readable report + score
node scripts/audit.mjs /path/to/project --json  # machine-readable for CI / further processing
```

It finds the `app/` (or `src/app/`) dir itself, walks all `.tsx/.ts/.jsx/.js`,
and reports `ERROR` / `WARN` / `INFO` findings with `file:line`, the reason, and
a fix. Exit code is non-zero when any `ERROR` exists, so it drops into CI.

What it detects:

| Rule | Severity | Why it matters |
|------|----------|----------------|
| `client-route-no-metadata` | ERROR | A `"use client"` page/layout silently drops `metadata` — SEO tags never ship. |
| `legacy-next-head` | ERROR | `next/head` is a no-op in the App Router — its tags never reach `<head>`. |
| `legacy-next-image` | WARN | `next/legacy/image` keeps old layout-shift-prone behavior. |
| `needless-use-client` | WARN | `"use client"` with no hooks/handlers/browser APIs — pushes JS to the client for nothing. |
| `client-fetch-in-effect` | WARN | Fetching in `useEffect` adds a render round-trip; move it server-side. |
| `raw-img` | WARN | `<img>` skips `next/image` sizing/lazy-loading — CLS & LCP regressions. |
| `unoptimized-font` | WARN | Fonts via `<link>`/`@import` are render-blocking; use `next/font`. |
| `page-missing-metadata` | WARN | Async page exports no `metadata`/`generateMetadata`. |
| `dangerous-html` | WARN | `dangerouslySetInnerHTML` — XSS risk if unsanitized. |
| `request-waterfall` | INFO | ≥2 sequential awaited fetches, no `Promise.all`. |
| `no-streaming-fallback` | INFO | Async page with no `loading.tsx`/Suspense — no streamed shell. |
| `force-dynamic` | INFO | Route opts out of static/ISR rendering — confirm it's intentional. |
| `large-client-component` | INFO | Big Client Component ships entirely to the browser. |

The scanner is heuristic (regex-based, not a full type-check): treat findings as
strong leads, confirm each against the source before reporting it as fixed.

## Step 2 — Manual pass (what the scanner can't see)

Read `reference/checklist.md` and verify the items that need real understanding:

- **Server/Client boundary correctness** — is the `"use client"` boundary as low
  in the tree as possible? Is a server-only secret (API key, DB client) imported
  into a client module?
- **Caching intent** — does each `fetch`/`unstable_cache`/`revalidate` match how
  fresh the data must be? Over-caching ships stale data; under-caching kills TTFB.
- **Suspense granularity** — is slow data wrapped close to where it's used, so the
  rest of the page streams immediately?
- **`generateStaticParams` / ISR** — are dynamic routes pre-rendered where they can be?
- **Server Actions** — are mutations using actions with proper `revalidatePath`/
  `revalidateTag` instead of client fetches to route handlers?

## Step 3 — Report

Lead with the `ERROR`s, then `WARN`, then the highest-leverage `INFO`s. For each:
`file:line`, one line on the impact, and the concrete fix (often a small diff).
End with the score and the 3 changes with the best effort-to-impact ratio. Don't
dump every `INFO` — curate.

## Rules

- Never claim a fix is applied unless you actually edited the file and re-ran the scanner.
- The scanner reports leads, not verdicts — verify boundary/caching findings by reading the code.
- Respect the project's existing conventions; match its import style and structure.
- This Next.js may differ from older versions — check `node_modules/next/dist/docs/` if an API is uncertain rather than assuming.

---

Built and maintained by [Datagrove](https://datagrove.nl) — a Dutch web development
agency specializing in fast, well-architected Next.js websites. Need an audit or a
rebuild? [Talk to Datagrove](https://datagrove.nl/contact).
