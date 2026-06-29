---
name: project-skeletonization
description: Collaborative workflow for converting a complete business project into a reusable base skeleton. Use when the user asks to remove business features, pages, or modules; keep base framework capabilities such as common components, authentication, and deployment; or turn Spring Boot, Vue, Node.js, Python, React, Django, FastAPI, Express, or similar projects into a starter, skeleton, or template. Before modifying code, inventory the project, propose keep/remove decisions, list uncertain items, and wait for user confirmation.
---

# Project Skeletonization

## Goal

Convert an existing complete business project into a reusable base skeleton. The skeleton should run independently, keep common engineering capabilities, remove concrete business features, and provide minimal placeholder pages, APIs, or tasks to prove that the framework path still works.

This skill is collaborative. Do not perform large deletions or refactors without confirmation. If module ownership, retention policy, or future reuse direction is unclear, ask the user first.

## Principles

- Understand first, design second, modify third.
- Keep common capabilities and remove business capabilities.
- Delete with evidence: explain why a module is business-specific before deleting it.
- Ask when uncertain.
- Prioritize a skeleton that can start, build, and integrate before polish.
- Do not introduce a new technology stack unless the user explicitly asks or the existing project cannot meet the skeleton goal.
- Preserve configurations, scripts, and deployment entry points that the user did not ask to remove. If they contain business content, propose a transformation plan first.
- Use the same workflow across technology stacks, but judge modules according to the actual project.

## Mandatory Confirmation Gate

Before any destructive transformation, output the following and wait for user confirmation:

1. Project inventory summary: frontend, backend, scripts, deployment, database, tests, documents, and other major areas.
2. Proposed keep list: common base capabilities such as authentication, routing, layout, configuration, logging, exception handling, health checks, CI/CD, Docker, base components, and scaffolding configuration.
3. Proposed remove list: business pages, APIs, models, migrations, documents, test data, and old build artifacts.
4. Uncertain items: file upload, audit logs, notifications, scheduled jobs, permission model, database/ORM, cache, message queue, object storage, monitoring, and similar modules.
5. Key options: ports, package names, project name, placeholder behavior, whether to keep the database, whether to keep authentication, and related choices.

Do not start the transformation until the user confirms. Previously confirmed items do not need repeated confirmation, but newly discovered boundary issues still require separate confirmation.

## Workflow

### 1. Inventory the Project

Read the project structure and key files:

- Root: README, build scripts, Docker, CI/CD, environment examples.
- Frontend: `package.json`, routes, entry files, API clients, state management, layouts, components, pages.
- Backend: build files, entry class or script, routes/controllers, services, models/entities, configuration, authentication middleware, tests.
- Python: `pyproject.toml`, `requirements.txt`, `setup.py`, `app/`, `src/`, routes, ORM, configuration.
- Node.js: `package.json`, `src/`, routes, middleware, services, models, tests, build scripts.
- Database: migrations, schema, seed data, ORM models, connection configuration.
- Deployment: Dockerfile, compose, nginx, Kubernetes, PM2, supervisor, systemd.

Use fast search to identify business traces: business names, table names, domain terms, page paths, API paths, old ports, old project names, and old image names.

### 2. Classify Modules

Classify modules into three groups.

**Keep**

- Authentication, login, sessions, and permission framework.
- Common layout, route guards, base components, request wrapper, state management.
- Unified response, exception handling, logging, health checks, configuration loading.
- OpenAPI/Swagger, test framework, build configuration.
- Docker, nginx, compose, CI/CD, and other deployment skeletons.

**Remove**

- Concrete business pages, menus, APIs, and services.
- Business entities, DTOs, repositories, ORM models, migrations, and seed data.
- Business reports, imports/exports, process sync, and business scheduled tasks.
- Old business documents, old build outputs, and old static outputs.

**Needs confirmation**

- Audit logs, file uploads, notifications, cache, message queue, database/ORM, multi-tenancy, permission menus, object storage, scheduled jobs, and monitoring.
- These may be common capabilities or may be deeply tied to business logic. Explain the tradeoff and ask the user.

### 3. Propose the Skeleton Design

Before confirmation, provide a concise design:

- Skeleton name, package/module name, and port.
- Common capabilities to keep.
- Business scope to remove.
- Placeholder capability to add: page, API, CLI command, or test task.
- Verification method: build, test, startup, or integration check.
- Risks: external SSO dependency, missing local runtime, missing Maven wrapper, npm audit findings, and similar issues.

Recommended placeholders:

- Web frontend: a post-login home or placeholder page that calls a backend placeholder API.
- Backend API: public `/health` plus `/placeholder/status` or an equivalent endpoint to verify authentication and API wiring.
- CLI/library project: a minimal `hello/status` command or function with tests.
- Python web: FastAPI/Django/Flask health check and protected placeholder route.
- Node.js web: Express/Nest/Koa health check and protected placeholder route.

### 4. Transform in Stages

Proceed from low risk to high risk:

1. Add placeholder tests or minimal verification first.
2. Clean business routes and menus.
3. Clean business services, models, database artifacts, DTOs, and test data.
4. Clean business dependencies and configuration.
5. Update project name, port, Docker, README, and environment examples.
6. Add placeholder pages, APIs, or commands.
7. Scan for old business keywords and old port remnants.
8. Run tests, builds, and startup verification.

Follow the active agent's file editing and safety rules when deleting files. Do not use dangerous bulk deletes against unconfirmed paths. Handle build outputs, caches, `dist`, `target`, and `node_modules` according to the user's goal and the project's conventions.

## Stack-Specific Notes

**Spring Boot / Java**

- Remove business controllers, services, entities, repositories, and DTOs.
- If the user chooses a no-database skeleton, remove JPA, database drivers, datasource configuration, and migrations.
- Keep unified response, exception handling, configuration, authentication, OpenAPI, and health checks.

**Node.js / TypeScript**

- Remove business routes, controllers, services, and models.
- Keep or remove ORM tools such as Prisma, TypeORM, Sequelize, or Mongoose according to user choice.
- Keep middleware, configuration, logging, tests, and base request/response conventions.

**Python**

- Remove business apps, routers, schemas, models, migrations, and tasks.
- Keep or remove SQLAlchemy, Django ORM, Alembic, or Celery according to user choice.
- Keep configuration, logging, exception handling, health checks, and test framework.

**Frontend**

- Remove business pages, menus, API modules, business stores, and business constants.
- Keep entry files, routing, layout, base components, request wrapper, authentication guards, and theme styles.
- Add a placeholder page that shows login state and API connectivity.

## Confirmation Questions

When confirmation is needed, ask only a few key questions first:

- Should the database/ORM be removed, kept as configuration only, or kept with common tables?
- Should authentication be kept, and should the placeholder API require login?
- Are file upload, audit logs, notifications, and scheduled jobs common capabilities or business features to remove?
- Are the port, project name, package name, and Docker image name specified?
- Should the skeleton keep the multi-module structure or converge to a minimal structure?

Avoid asking too many questions at once. Ask questions that affect the overall direction first, then ask about new boundary issues as they appear.

## Verification Checklist

Before completion, verify and report:

- Whether the build command passed.
- Whether the test command passed.
- Whether the local service can start.
- Whether the health check succeeds.
- Whether the protected placeholder API requires login or returns 401 as designed.
- Whether the frontend placeholder page loads and triggers login guard when unauthenticated.
- Whether old business keywords, old ports, and old project names remain.

If something cannot be verified, explain why and provide alternative evidence. Do not describe unverified items as completed.

## Final Delivery

The final response should include:

- Transformation scope summary.
- Common capabilities kept.
- Business capabilities removed.
- New ports and startup method.
- Placeholder page/API locations.
- Verification commands and results.
- Remaining user concerns, such as external login systems, secrets, audit warnings, or missing wrappers.

Do not output a long file list unless the user asks for it.
