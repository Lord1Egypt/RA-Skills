#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <project-root> '<project brief>'" >&2
  exit 1
fi

root="$1"
brief="$2"

mkdir -p "$root/docs/notes" "$root/docs/decisions"

./skills/opengemini-nextjs-bestpractice-builder/scripts/generate_gemini_md.sh "$root/GEMINI.md"

gemini -p "Create docs/requirements.md in markdown for a solo-developer SaaS using this stack: Next.js App Router, Tailwind, shadcn/ui, Neon PostgreSQL, Prisma, Clerk, Resend, Stripe, Cloudflare R2, PostHog, Sentry, Vercel, FastAPI only for Python-required workloads. Brief: ${brief}. Include summary, target users, problem, goals, non-goals, MVP scope, monetization, user stories, functional requirements, non-functional requirements, risks, success metrics. Return markdown only." > "$root/docs/requirements.md"

gemini -p "Create docs/scope.md in markdown for this SaaS. Brief: ${brief}. Include in scope, out of scope, MVP milestones, deferred features. Return markdown only." > "$root/docs/scope.md"

gemini -p "Create docs/architecture.md in markdown for this SaaS. Brief: ${brief}. Respect this stack: Next.js App Router, Tailwind, shadcn/ui, Neon PostgreSQL, Prisma, Clerk, Resend, Stripe, Cloudflare R2, PostHog, Sentry, Vercel, FastAPI only for Python-required workloads. Include system overview, Mermaid diagram, frontend architecture, backend architecture, data architecture, auth and billing boundaries, integrations, deployment, open questions. Return markdown only." > "$root/docs/architecture.md"

gemini -p "Create docs/conventions.md in markdown for this SaaS. Brief: ${brief}. Include code style, folder structure, naming, server vs client rules, feature boundaries, testing rules, env var rules, error handling, logging and monitoring. Return markdown only." > "$root/docs/conventions.md"

gemini -p "Create docs/integrations.md in markdown for this SaaS. Brief: ${brief}. Cover Clerk, Stripe, Resend, Cloudflare R2, PostHog, Sentry, Neon, FastAPI, Vercel. Return markdown only." > "$root/docs/integrations.md"

gemini -p "Create docs/db-schema.md in markdown for this SaaS. Brief: ${brief}. Include core models, relationships, billing models, file metadata models, audit and event notes. Respect these rules: do not duplicate Clerk as full auth in Prisma, do not store uploaded files in PostgreSQL, use Stripe webhook state. Return markdown only." > "$root/docs/db-schema.md"

echo "Generated core docs under $root/docs"
