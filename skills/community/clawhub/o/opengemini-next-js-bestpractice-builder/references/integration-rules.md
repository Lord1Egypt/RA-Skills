# Integration Rules

## Clerk
- Use Clerk as the auth source of truth
- Store only the app-level user profile fields you actually need in Prisma
- Reference Clerk user IDs instead of recreating auth tables

## Stripe
- Billing state comes from webhook-driven persistence
- Success and cancel redirects are UX only
- Record subscription and checkout state in app-domain tables

## Resend
- Use for transactional emails
- Document trigger points and templates
- Keep email logic server-side

## Cloudflare R2
- Store files in R2, not PostgreSQL
- Save file metadata and ownership in Prisma
- Define access rules clearly

## PostHog
- Track core activation and revenue events
- Do not spray random events everywhere
- Decide event naming up front

## Sentry
- Capture server and client errors intentionally
- Tag critical flows like auth, billing, upload, and AI jobs

## FastAPI
- Use only for Python-required workloads
- Keep API boundaries explicit
- Avoid mirror CRUD APIs when Next.js can already handle it

## Vercel
- Treat it as the default frontend deploy target
- Document env vars and preview vs production behavior
