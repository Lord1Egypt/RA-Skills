#!/usr/bin/env bash
set -euo pipefail

out="${1:-GEMINI.md}"
cat > "$out" <<'EOF'
# Source of truth
1. docs/requirements.md
2. docs/scope.md
3. docs/architecture.md
4. docs/conventions.md
5. docs/decisions/*.md
6. docs/notes/brainstorming.md is reference only

# Stack policy
- Frontend: Next.js App Router
- UI: Tailwind + shadcn/ui
- DB: Neon PostgreSQL
- ORM: Prisma
- Auth: Clerk
- Email: Resend
- Payments: Stripe
- Storage: Cloudflare R2
- Analytics: PostHog
- Error Monitoring: Sentry
- Deploy: Vercel
- Backend: FastAPI only for Python-required workloads

# Backend boundary
- Default backend logic lives in Next.js route handlers or server actions
- FastAPI is only for AI, batch, heavy processing, or Python-specific integrations

# Never do
- Do not duplicate Clerk auth state into Prisma as a full auth system
- Do not treat Stripe success redirect as source of truth; use webhook state
- Do not store uploaded files in PostgreSQL
- Do not add FastAPI endpoints for simple CRUD unless explicitly required
EOF

echo "Wrote $out"
