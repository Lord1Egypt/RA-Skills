# Doc Templates

Use these templates as the minimum structure.

## GEMINI.md

```md
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
```

## requirements.md

```md
# Requirements
## Summary
## Target Users
## Problem
## Goals
## Non-Goals
## MVP Scope
## Monetization
## User Stories
## Functional Requirements
## Non-Functional Requirements
## Risks
## Success Metrics
```

## scope.md

```md
# Scope
## In Scope
## Out of Scope
## MVP Milestones
## Deferred Features
```

## architecture.md

```md
# Architecture
## System Overview
## Mermaid Diagram
## Frontend Architecture
## Backend Architecture
## Data Architecture
## Auth and Billing Boundaries
## Integrations
## Deployment
## Open Questions
```

## conventions.md

```md
# Conventions
## Code Style
## Folder Structure
## Naming
## Server vs Client Rules
## Feature Boundaries
## Testing Rules
## Env Var Rules
## Error Handling
## Logging and Monitoring
```

## integrations.md

```md
# Integrations
## Clerk
## Stripe
## Resend
## Cloudflare R2
## PostHog
## Sentry
## Neon
## FastAPI
## Vercel
```

## db-schema.md

```md
# DB Schema
## Core Models
## Relationships
## Billing Models
## File Metadata Models
## Audit and Event Notes
```
