---
name: internal-app-bootstrap
description: "Use when creating a new internal application from scratch, standardizing a 0-to-1 app build workflow, or helping teammates bootstrap a Next.js/FastAPI/Keycloak/PostgreSQL style product with a docs-first process. Keywords: build new app, bootstrap app, internal tool, requirements clarification, architecture proposal, MVP planning, docs first, full-stack app, standard workflow, delivery checklist."
---

# Internal App Bootstrap

## Purpose

Use this skill when a teammate wants to build a new internal application with a consistent, reviewable, documentation-first workflow instead of jumping straight into code.

This skill captures the workflow used to build i-skills from an empty workspace into a working full-stack application with:

- requirements discovery before implementation
- documented architecture and workflow decisions
- a monorepo-style frontend and backend split
- authentication planning
- database and schema planning
- implementation sequencing
- validation and operational readiness

## When To Use

Use this skill when the user asks for any of the following:

- build a new app from scratch
- create a standardized internal tool
- bootstrap a full-stack product with a clear process
- help a team follow a repeatable app delivery workflow
- turn an idea into an MVP with aligned frontend, backend, and docs

Do not use this skill for narrow bug fixes, isolated UI tweaks, or one-off backend endpoint changes.

## Core Principles

1. Requirements first
2. Architecture before implementation
3. Documentation before code
4. English and Chinese documentation stay aligned
5. Small, verifiable milestones
6. Validation is part of delivery, not an afterthought

## Reusable Standards To Apply

When using this skill, treat the repository standards under `docs/` as reusable baseline rules, not project-specific trivia.

### Documentation authority by domain

- `docs/api-development.md` and `docs/api-development.cn.md` define backend contract, route, schema, migration, authentication, and operational diagnostics expectations.
- `docs/ux-development.md` and `docs/ux-development.cn.md` define navigation, form, feedback, authentication UX, responsive behavior, and content rules.
- `docs/coding-standards.md` and `docs/coding-standards.cn.md` define repository-wide structure, tooling, naming, validation, and change-discipline rules.
- `docs/copilot-guide.md` and `docs/copilot-guide.cn.md` define the required docs-first workflow and the order in which work should happen.

### Common rules worth reusing in new app bootstraps

- Keep frontend, backend, and docs aligned around the same product vocabulary.
- Keep public contracts explicit and stable.
- Put business rules in backend services, not only in frontend behavior.
- Keep route handlers and page components thin.
- Use one JavaScript package manager consistently.
- Treat validation, health checks, and diagnostics as part of delivery.
- Prefer explicit auth, storage, and database boundaries over hidden side effects.
- If production uses PostgreSQL, use explicit schema management and migrations.
- If UI depends on backend data or permissions, design both fallback and error states intentionally.
- Do not call work complete if paired documentation and validation are missing.

## Standard Workflow

### 1. Clarify the business problem

Start by extracting the operational shape of the app.

Capture at minimum:

- who will use it
- what the primary jobs-to-be-done are
- whether the app is internal or external
- whether data is sensitive or regulated
- what the MVP must include
- what is explicitly out of scope

Use the requirements template in `templates/requirements-template.md` and `templates/requirements-template.cn.md`.

### 2. Identify non-negotiable constraints

Before proposing architecture, confirm constraints such as:

- authentication provider
- deployment environment
- database target
- storage strategy
- whether uploads are required
- access control and visibility rules
- whether the app executes user-provided artifacts or only stores/references them
- mobile adaptation expectations

### 3. Propose a concrete solution

After the requirements are clear, propose a solution that covers:

- frontend framework
- backend framework
- database
- auth integration
- storage approach
- recommended project structure
- MVP page map or workflow map
- major risks and tradeoffs

Do not start implementation until the solution is confirmed.

### 4. Create or update documentation first

Before code changes, write or update the relevant English and Chinese docs.

Always read the matching standards in `docs/` first and treat them as the authority for what needs to be documented and validated.

For a new product or workflow, document at least:

- API expectations
- UX expectations
- coding standards if new conventions are introduced
- workflow guidance if team process is affected

### 5. Establish the workspace and toolchain

Set up the project structure intentionally.

Typical baseline:

- frontend under `apps/web`
- backend under `apps/api`
- docs under `docs`
- shared workflow guidance under `.github`

Normalize the toolchain early:

- choose one JavaScript package manager
- define dev tasks
- define environment file conventions
- avoid mixed lockfiles or partial scaffolding state

### 6. Build the MVP in thin vertical slices

Prefer end-to-end slices over isolated piles of code.

A good slice order is:

1. app shell and navigation
2. backend models and core routes
3. frontend pages wired to documented contracts
4. upload or creation workflow
5. review or approval workflow
6. authentication integration
7. operational tooling

### 7. Integrate auth and identity deliberately

If authentication is required:

- separate browser and server auth concerns
- avoid hardcoding secrets
- document runtime configuration
- expose a minimal profile or debug view for identity inspection when needed
- derive sensitive identity fields on the server

### 8. Treat the database as a product concern

If production uses PostgreSQL:

- configure the target database and schema explicitly
- avoid relying on implicit defaults
- manage schema changes through Alembic migrations
- provide diagnostics for connectivity, schema, and revision state

### 9. Add operational affordances

Before calling the app usable, add:

- dev tasks for common operations
- health or diagnostics commands
- migration commands
- clear local startup instructions

### 10. Validate before handoff

Validation should include the touched surfaces.

Typical checks:

- frontend build
- backend import or startup sanity check
- representative endpoint checks
- auth flow validation when applicable
- migration or schema validation when applicable

Use the delivery checklist in `templates/delivery-checklist.md` and `templates/delivery-checklist.cn.md`.

## Expected Deliverables

A complete bootstrap task should usually produce:

- a documented requirements summary
- a confirmed architecture proposal
- updated English and Chinese docs
- runnable frontend and backend foundations
- clear environment and task configuration
- validated core flows
- a concise change summary and next steps

## Output Pattern

When using this skill, structure the work like this:

1. Requirements summary
2. Proposed architecture and MVP boundaries
3. Documentation updates
4. Implementation plan
5. Code and configuration changes
6. Validation results
7. Follow-up recommendations

## Common Failure Modes

Avoid these mistakes:

- coding before confirming requirements
- skipping the relevant `docs/` files and inferring rules only from existing code
- letting docs lag behind implementation
- using mock behavior as the contract
- mixing package managers
- wiring auth without a debug path
- relying on automatic database mutation in shared environments
- stopping at scaffolding without validating real workflows

## Skill Assets

- `templates/requirements-template.md`
- `templates/requirements-template.cn.md`
- `templates/delivery-checklist.md`
- `templates/delivery-checklist.cn.md`

Use the templates directly when preparing a new app kickoff or reviewing whether a build is truly complete.
