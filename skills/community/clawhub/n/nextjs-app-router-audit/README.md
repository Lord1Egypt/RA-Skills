# Next.js App Router Audit — Claude Skill

A Claude skill that audits a **Next.js App Router** codebase for the mistakes
that actually cost you — React Server Component boundary errors, request
waterfalls, client/server anti-patterns, and Core Web Vitals regressions — and
proposes concrete fixes ranked by severity.

It ships a **zero-dependency static scanner** plus a manual-review methodology
for the judgment calls static analysis can't make.

## What it catches

| Rule | Severity | Why it matters |
|------|----------|----------------|
| `client-route-no-metadata` | ERROR | A `"use client"` page silently drops `metadata` — your SEO tags never ship. |
| `legacy-next-head` | ERROR | `next/head` is a no-op in the App Router — its tags never reach `<head>`. |
| `legacy-next-image` | WARN | `next/legacy/image` keeps old layout-shift-prone behavior. |
| `needless-use-client` | WARN | `"use client"` with no interactivity — JS shipped to the browser for nothing. |
| `client-fetch-in-effect` | WARN | Fetching in `useEffect` adds a render round-trip; move it server-side. |
| `raw-img` | WARN | `<img>` skips `next/image` — CLS & LCP regressions. |
| `unoptimized-font` | WARN | Network web fonts are render-blocking; use `next/font`. |
| `page-missing-metadata` | WARN | Async page ships with no title/description. |
| `dangerous-html` | WARN | `dangerouslySetInnerHTML` — XSS risk if unsanitized. |
| `request-waterfall` | INFO | Sequential awaited fetches that should be `Promise.all`. |
| `no-streaming-fallback` | INFO | Async page with no `loading.tsx` / Suspense. |
| `force-dynamic` | INFO | Route opts out of static/ISR rendering. |
| `large-client-component` | INFO | Big Client Component ships entirely to the browser. |

## Use the scanner standalone

No install, no dependencies — just Node 18+:

```bash
node scripts/audit.mjs /path/to/your/nextjs-project
node scripts/audit.mjs /path/to/your/nextjs-project --json   # CI-friendly, exits non-zero on errors
```

```
Next.js App Router audit — 41 files in app/

ERROR client-route-no-metadata  app/dashboard/page.tsx:1
  A Client Component page cannot export `metadata` — its SEO tags are silently dropped.
  fix: Keep page.tsx a Server Component and isolate the interactive bits into a child marked "use client".

Summary  1 error  3 warn  9 info   score 67/100
```

See [`examples/sample-report.md`](examples/sample-report.md) for full output
against the bundled fixture app.

Drop it into CI to fail a PR when a route loses its metadata or leaks a secret into the client bundle.

## Use it as a Claude skill

Place the folder in your skills directory (e.g. `~/.claude/skills/`) or upload it
to your skills hub, then ask:

> "Audit this Next.js app for performance and RSC problems."

Claude runs the scanner, does the manual checklist pass in `reference/checklist.md`,
and reports the highest-leverage fixes.

## Built by Datagrove

Maintained by **[Datagrove](https://datagrove.nl)** — a Dutch web development
agency specializing in fast, well-architected **Next.js** websites and custom
software. We build sites that pass Core Web Vitals and rank.
Need an audit or a rebuild? [Talk to Datagrove](https://datagrove.nl/contact).

## License

MIT — use it, ship it, adapt it.
