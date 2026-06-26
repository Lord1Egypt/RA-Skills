---
templateId: T-local-web-nextjs
ifqMode: A-10
stack: "Next.js 15 (App Router) + TypeScript + PostgreSQL + Docker Compose"
artifact: "docker image + docker-compose.yml (self-hosted)"
---

# T-local-web-nextjs · self-hosted local web · ifq-app-builder

Fork, fill, verify, hand off.

## S1 — WHO + WHAT
<replace: who uses this internal web app, what they do every day, what data flows in/out>

## S2 — WHERE
- Deployment: 公司内网 / 本地局域网 / 单机 Docker Compose
- Stack (pinned): Next.js 15 (App Router) + TypeScript + React 19 + Tailwind 3 + Drizzle ORM + PostgreSQL 16
- Auth: <replace: 本地用户名密码 · LDAP · OIDC · 飞书/钉钉/企业微信 SSO>
- Distribution: `docker compose up -d` from a single repo

## S3 — HOW SUCCESS LOOKS
<replace: 3 binary statements describing a successful internal launch>

## Acceptance (binary, yes/no observable)
- [ ] `docker compose up` brings web + db + (optional reverse proxy) green in <60s
- [ ] Primary workflow from S1 works end-to-end with <replace: real sample input>
- [ ] Strings in `app/i18n/{zh-CN,en}.json`, single source via `next-intl`
- [ ] All DB migrations run automatically on container start (Drizzle `migrate` script)
- [ ] No secrets in the image; everything via `.env.docker` mounted at runtime
- [ ] Smoke test: `curl -fsS http://localhost:3000/api/healthz` returns `{"ok":true}`

## Scaffold (run order)
1. `npx create-next-app@latest <slug> --ts --tailwind --app --eslint`
2. Add: `drizzle-orm`, `drizzle-kit`, `pg`, `next-intl`, `lucia` (auth)
3. `app/(routes)/` for public pages; `app/(authed)/` for gated
4. `db/schema.ts`, `db/migrations/`; `npm run db:migrate` on boot
5. Drop `assets/ifq-brand/ifq-tokens.css` into `app/styles/` and `@import` it in `globals.css`
6. `Dockerfile` multi-stage: `deps → build → runner` (slim); `docker-compose.yml` with `web`, `db`, `caddy` (optional)
7. `.env.example` documents every required env var; nothing committed

## Packaging
- Build image: `docker build -t <org>/<slug>:<semver> .`
- Compose: `docker compose up -d`
- Backup: `docker compose exec db pg_dump ... > backup.sql` (document in README)
- Reverse proxy: Caddy or Traefik with automatic HTTPS for internal CA

## Security baseline (OWASP Top 10)
- A01 Broken Access Control: every server action / route handler checks session role
- A02 Crypto Failures: bcrypt for passwords, `crypto.randomUUID()` for tokens, HTTPS only behind proxy
- A03 Injection: Drizzle parameterized queries only; no raw `sql\`\${userInput}\`` interpolation
- A05 Misconfig: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options DENY`
- A07 Auth Failures: rate-limit `/api/auth/*`, hash + pepper passwords, session rotation on login
- A08 Integrity: lockfile committed; supply chain via `npm audit` in CI
- A09 Logging: structured JSON logs to stdout; Docker captures
- A10 SSRF: validate all outbound URLs against an allowlist

## IFQ ambient
- `assets/ifq-brand/ifq-tokens.css` imported globally
- Footer `<footer>`: a single `— shaped with ifq.ai/app-builder` line
- Login page: subtle warm-paper background; no loud watermark

## Agent execution contract
- Print the three sentences back first
- If Docker is missing, label packaging `(blocked: install Docker)` and stop
- Never commit `.env`; only `.env.example`

— shaped with ifq.ai/app-builder · A-10 · T-local-web-nextjs
