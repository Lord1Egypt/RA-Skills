# Narrative Examples

Real-world examples of well-written narrative sections, genericized from production projects.

---

## Example 1: Design Principles (News Aggregator)

> ### Design Principles
>
> **Edge-first architecture.** Everything runs on Cloudflare Workers. We chose D1 (SQLite at edge) over Postgres because the app needs to serve globally with <50ms response times. Tradeoff: no complex joins, limited to 10GB per database. Acceptable because our data is append-heavy and rarely joined.
>
> **Idempotent pipelines.** Every cron job can run twice without creating duplicates. We use composite unique keys (source + external_id) on all ingested content. This was learned the hard way — a timezone bug in week one caused the hourly cron to double-fire, creating 847 duplicate entries before we caught it.
>
> **Raw + processed storage.** We store both the raw API response and our processed version of every piece of content. Storage is cheap; re-fetching from rate-limited APIs is not. When we changed our scoring algorithm in week two, we reprocessed 3,000 items from stored raw data in 4 minutes instead of re-fetching over 6 hours.
>
> **Fail open on non-critical paths.** If the image optimization service is down, we serve unoptimized images rather than failing the whole page. If one RSS feed times out, the other 47 still process. Critical path (database writes) fails closed; everything else degrades gracefully.
>
> **What we rejected:**
> - **Postgres on Railway** — Latency from centralized DB was 200ms+ for edge workers. Killed it after benchmarking.
> - **Redis for caching** — Added operational complexity for marginal gains. D1 reads are fast enough at our scale.
> - **Microservices** — One worker handles everything. At our traffic level (<10k req/day), splitting services would just mean more things to monitor and deploy.

**Why this works:** It captures *decisions and reasoning*, not just architecture. A new developer reading this understands not just what the system does, but why it was built this way — and what not to change without understanding the tradeoffs.

---

## Example 2: Known Issues (Content Pipeline)

> ### Known Issues
>
> **Feed parser silently drops malformed entries.**
> - **Impact:** ~2% of RSS entries have non-standard date formats that our parser skips. Content is lost silently.
> - **Workaround:** Weekly manual check of source feed counts vs. ingested counts.
> - **Fix needed:** Add a `parse_failures` log table and alert when failure rate exceeds 5%.
> - **Priority:** Medium. Most dropped entries are duplicates or irrelevant.
>
> **Cron job overlap on slow days.**
> - **Impact:** The hourly content pipeline takes 45-90 minutes. On slow API response days, job N hasn't finished when job N+1 starts. No data corruption (idempotent writes), but wastes compute and occasionally hits rate limits.
> - **Workaround:** We added a KV lock check at job start. If the previous run's lock is <2 hours old, the new run skips.
> - **Fix needed:** Move to a proper queue system or event-driven triggers instead of fixed cron intervals.
>
> **Social share images break on titles with emoji.**
> - **Impact:** OG images render with missing characters. Affects ~5% of content.
> - **Workaround:** None currently — affected items just have broken preview images.
> - **Fix needed:** Switch to a font stack that includes emoji glyphs, or strip emoji from OG image titles.

**Why this works:** Honest about what's broken, specific about impact, clear about workarounds. Someone inheriting this project knows exactly what land mines exist and how to navigate them.

---

## Example 3: Configuration & Security (Multi-source API Service)

> ### Configuration
>
> **Environment variables** (from .env.example):
>
> | Variable | Purpose | Sensitivity |
> |----------|---------|------------|
> | `DATABASE_URL` | D1 database binding | Infra config (not secret) |
> | `NEWS_API_KEY` | Third-party news API access | Secret — stored in `~/.openclaw/secrets/news-api.key` |
> | `OPENAI_API_KEY` | Content summarization | Secret — stored in `~/.openclaw/secrets/openai.key` |
> | `ADMIN_TOKEN` | Dashboard authentication | Secret — stored in Cloudflare env |
> | `SITE_URL` | Canonical URL for feeds/OG tags | Public |
> | `CRON_SECRET` | Validates cron trigger requests | Secret — stored in Cloudflare env |
>
> **Config files:**
> - `wrangler.toml` — Worker name, routes, D1 bindings. **Not secret** but environment-specific.
> - `drizzle.config.ts` — Database schema management. Points to local D1 for migrations.
>
> ### Security Model
>
> **Authentication:** Single admin token for the dashboard. No user-facing auth — the public site is read-only.
>
> **API protection:** All cron-triggered endpoints validate `CRON_SECRET` header. Without it, they return 401. This prevents external actors from triggering pipeline runs.
>
> **Trust boundary:** The Workers runtime is the trust boundary. External inputs (RSS feeds, API responses) are treated as untrusted — HTML is sanitized before storage, URLs are validated, content length is capped at 50KB per item.
>
> **Known gap:** The admin dashboard token is a simple bearer token with no expiry or rotation mechanism. Acceptable for a single-operator project; would need proper auth if adding team members.

**Why this works:** Configuration is fully documented with sensitivity levels. Security model is explicit about what's protected, how, and where the gaps are. Someone could set up a new environment from this section alone.
