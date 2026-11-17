# Publishing

## Draft to published
- POST /publish (step-up) snapshots the whole draft: every fully static page bakes to `uploads/published/current/<route>.html`, 404 page also bakes to `404.html` (static-host convention), swap is an atomic pointer-file rename.
- GET /publish/status reports draft-vs-published freshness.
- Concurrent publishes serialize under a publish lock; runtime script build errors return 422.

## Three serving layers
1. Layer A: disk artifacts for static routes.
2. Layer B: in-memory LRU for request-dependent renders keyed by (urlPath, canonicalQuery); publish-version bumps evict.
3. Layer C: holes. Nodes auto-classified request-dependent (loop bodies above all) publish as `<instatic-hole>` placeholders inside otherwise baked HTML. A ~1.1 KB IntersectionObserver runtime fills each via `/_instatic/hole/<nodeId>?v=<publishVersion>&u=<pageUrl>`.

Consequence: pages containing holes need this server reachable at view time. A deploy to a pure static host only works if the page set is hole-free or holes are pre-resolved. Test by fetching a published page and counting `instatic-hole` occurrences before promising any static export.

## Scheduled and per-row publishing
- postType rows move draft -> published independently; schedule a publish with `scheduled_publish_at`, a boot-running scheduler ticks and publishes due rows (a failure drops the row back to draft).
- Published copies keep version history; restore any version as a new draft copy.

## Export bundle vs deploy output
GET/POST /export produces a site-bundle zip (site shell, tables, rows, media bytes, redirects) for instance-to-instance transfer. It is not a static deploy artifact. Import strategies: replace | merge-add | merge-overwrite; preview first.

## Imports
- CMS bundles: /import (JSON) or /import/archive (ZIP), /import/preview to validate.
- Static-site Super Import (HTML/CSS/fonts/images zip): admin modal, plan -> commit as a single undo.

## Origins and TLS
- `PUBLIC_ORIGIN` must list canonical origins whenever a proxy or domain fronts the container (CSRF and preview links key off it).
- Upstream ships a Caddy layer (compose.tls.yml): real domain, Let's Encrypt via 80/443. On an overlay network (already-encrypted transport) a plaintext bind may be acceptable; that call is the operator's, not routine.

## Forms
Native form primitives render on pages; submissions POST to `/_instatic/form/submit` behind a challenge endpoint and land in data tables.
