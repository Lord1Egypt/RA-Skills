# {{PROJECT_NAME}} — Technical Documentation

> **For:** Developer onboarding and reference
> **Repo:** {{REPO_URL}}
> **Production:** {{PRODUCTION_URL}}

This is the developer-onboarding contract — the document a new contributor reads to understand how the system is built. It's intentionally summary-style and links into `docs/` for deep dives. The two layers stay in sync as part of finishing a feature (see CLAUDE.md "Housekeeping protocol").

When a feature ships, update both the relevant `docs/` file (operational reference) **and** the matching section here (summary contract). The recap workflow prompts for both.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [Architecture](#3-architecture)
4. [Database Schema](#4-database-schema)
5. [API Reference](#5-api-reference)
6. [Authentication & Authorization](#6-authentication--authorization)
7. [Frontend Structure](#7-frontend-structure)
8. [Background Jobs / Pipelines](#8-background-jobs--pipelines)
9. [Deployment & Environments](#9-deployment--environments)
10. [Development Workflow](#10-development-workflow)
11. [Scripts Reference](#11-scripts-reference)
12. [Observability](#12-observability)

---

## 1. Project Overview

{{ONE_LINE_DESCRIPTION}}

<add-when-implemented>
- What this product does in 2-3 sentences
- Who it's for (target users)
- Key differentiators from alternatives
</add-when-implemented>

## 2. Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | <add> |
| Language | <add> |
| Database | <add> |
| Cache | <add> |
| Auth | <add> |
| Hosting | <add> |
| CI/CD | <add> |

For the full tech stack rationale, see [`docs/architecture/overview.md`](docs/architecture/overview.md).

## 3. Architecture

<add-when-implemented>
- High-level system diagram or description
- Major components and how they communicate
- Data flow for the most common request type
</add-when-implemented>

Detailed architecture: [`docs/architecture/overview.md`](docs/architecture/overview.md)

## 4. Database Schema

<add-when-implemented>
- Number of tables / models
- Core entities and their relationships (1-2 sentences each)
- Migration strategy
</add-when-implemented>

Schema source of truth: `prisma/schema.prisma` (or equivalent for your stack). If the project is stateless (no DB — e.g., file-upload dashboards, static sites), write "N/A — stateless; data comes from [source]" instead.
Detailed model documentation: [`docs/architecture/database.md`](docs/architecture/database.md)

## 5. API Reference

<add-when-implemented>
- Style: REST / tRPC / GraphQL / gRPC
- Auth model
- Routers / endpoints (one-line list)
- Versioning strategy
</add-when-implemented>

Detailed API docs: [`docs/architecture/api.md`](docs/architecture/api.md)

## 6. Authentication & Authorization

<add-when-implemented>
- Auth provider / strategy
- Session model
- Role hierarchy
- Public vs protected routes
</add-when-implemented>

Detailed auth documentation: [`docs/architecture/auth.md`](docs/architecture/auth.md)

## 7. Frontend Structure

<add-when-implemented>
- Routing approach
- Component organization
- State management
- Styling system
</add-when-implemented>

## 8. Background Jobs / Pipelines

<add-when-implemented>
- Job runner / queue system
- Scheduled jobs and their cadences
- Pipeline phases
</add-when-implemented>

Pipeline details: [`docs/pipeline/README.md`](docs/pipeline/README.md) (if applicable)

## 9. Deployment & Environments

| Branch | Environment | Auto-deploy | Notes |
|--------|-------------|-------------|-------|
{{#BRANCHES}}
| `{{branch}}` | {{env}} | {{auto_deploy}} | {{notes}} |
{{/BRANCHES}}

Connection strings live in `CLAUDE.local.md` (gitignored).

## 10. Development Workflow

The plan-build-recap-document cycle:

1. **Plan** — draft a plan at `docs/plans/YYYY-MM-DD-<slug>.md` with acceptance criteria. See [`docs/plans/README.md`](docs/plans/README.md).
2. **Build** — implement on `develop`, validate locally first.
3. **Recap** — write a session recap at `docs/recaps/SESSION-RECAP-YYYY-MM-DD.md` with criteria status.
4. **Document** — update this file and `FUNCTIONAL-SPECIFICATIONS.md` for the affected feature area. The recap workflow prompts for this.

The cycle compresses for trivial work — typos and one-line fixes don't need a plan or doc updates.

## 11. Scripts Reference

<add-when-implemented>
- Most-used scripts (top 10)
- Common flags
</add-when-implemented>

Full catalog: [`docs/scripts/README.md`](docs/scripts/README.md) (if applicable)

## 12. Observability

<add-when-implemented>
- Logging system
- Error tracking
- Metrics / dashboards
- On-call / paging
</add-when-implemented>
