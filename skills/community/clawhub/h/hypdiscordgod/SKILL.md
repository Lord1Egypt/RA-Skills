---
name: hypdiscordgod
description: Build, extend, debug, scaffold, and package Discord bots and bot systems. Use when asked to create a Discord bot, scaffold a new bot project, add slash commands, prefix commands, event handlers, moderation systems, ticket systems, role tools, embeds, buttons, select menus, modals, webhooks, persistence, deployment setup, Bun support, Docker setup, dashboard/API integration, Discord OAuth dashboard auth, frontend dashboard scaffolding, queue/worker processing, Postgres/Prisma/Drizzle database variants, moderation dashboards, mono-repo service layouts, or troubleshoot Discord API behavior in Node.js/TypeScript or Python projects.
---

# HypDiscordGOD

## Overview

Use this skill to turn Discord bot requests into shippable systems with clean architecture, minimal privileged intents, clear configuration, and production-ready command, API, worker, and dashboard structure.

Prefer acting over theorizing: if the repository exists, inspect it and implement directly; if no project exists, scaffold a minimal runnable system immediately.

Default to modern Discord patterns:
- Prefer slash commands over legacy prefix commands unless the user asks otherwise.
- Prefer `discord.js` for Node/TypeScript projects and `discord.py` for Python projects unless the repo already uses another library.
- Keep tokens and secrets in environment variables; never hardcode them.
- Request only the intents and permissions the feature actually needs.

## Workflow

1. Inspect the repository and detect the stack.
2. Decide whether this is:
   - a new bot,
   - a new feature in an existing bot,
   - a refactor/migration,
   - a dashboard/API integration task,
   - a webhook integration task,
   - a worker/queue task,
   - a moderation dashboard task,
   - a mono-repo starter task,
   - or a debugging task.
3. Confirm the runtime, package manager, storage model, and bot library already in use.
4. Implement the smallest clean change that satisfies the request.
5. Add or update configuration examples, command registration, startup instructions, API route notes, auth notes, and worker notes if needed.
6. Validate with available tests, type checks, or a dry run when possible.
7. If creating a new bot or companion service from scratch, prefer bundled scaffolds and templates before hand-rolling files.

## Core Rules

- Match the existing repository style when one already exists.
- Prefer least privilege for intents, permissions, routes, and secrets.
- Keep Discord snowflakes as strings in JavaScript/TypeScript systems.
- Separate bot runtime, HTTP API, dashboard frontend, and worker concerns when complexity justifies it.
- Treat in-memory sessions as development-grade unless explicitly hardened.
- Call out production gaps clearly: CSRF, durable sessions, refresh token storage, HTTPS, audit logging, and permission enforcement.

## Mono-repo Systems

For bot + API + dashboard + worker systems:
- separate apps clearly
- share schema, config, and type helpers through packages or documented conventions
- leave behind runnable service start points and compose orchestration when possible
- prefer wiring the mono-repo starter to real bundled patterns instead of leaving empty placeholders
- when asked for a full transplant or deep merge, align monorepo app shapes with the richer bundled starters so another agent can upgrade them in place without re-scaffolding

## Output Expectations

When completing Discord bot work:
- Modify the existing project instead of inventing a parallel architecture.
- Include any required environment variables.
- Mention command registration steps if commands changed.
- Mention portal-side steps if intents or permissions must be enabled.
- Keep examples realistic and directly runnable.
- When adding persistence, define schema shape or migration expectations.
- When adding deployment, leave behind runnable deploy artifacts if appropriate.
- When adding transcript support, mention limitations around embeds, edited/deleted messages, and retention unless fully handled.
- When adding dashboard/API integration, identify which auth parts are development-grade versus production-ready.
- When adding OAuth, mention redirect URI requirements, secure session storage expectations, refresh-token handling expectations, and logout behavior.
- When adding queue/worker patterns, explain the responsibility split between API, worker, and bot.
- When adding Prisma or Drizzle, include enough starter assets that another agent can actually use them without rebuilding from scratch.
- When preparing for public release, keep wording generic, remove private assumptions, and ensure the packaged skill stands on its own.

## Bundled Assets

Use these when they save time:
- `assets/discord-js-ts-template/` for a modern slash-command bot starter.
- `assets/bun-template/` for a Bun-oriented starter.
- `assets/ticket-bot-starter/` for a SQLite-backed ticket bot with claim, archive/reopen, and transcript support.
- `assets/dashboard-api-starter/` for an Express + SQLite companion API starter with OAuth starter auth, guild permission checks, real OAuth guild listing, logout/session handling, CSRF protection, webhook route, shared guild-config access, and queue/worker patterns.
- `assets/dashboard-frontend-starter/` for a React/Vite dashboard frontend starter with multi-guild UX.
- `assets/moderation-dashboard-starter/` for a moderation dashboard API starter with audit logging.
- `assets/prisma-starter/` for a Prisma + Postgres starter with guild config and ticket schema.
- `assets/drizzle-starter/` for a Drizzle + Postgres starter with guild config and ticket schema.
- `assets/monorepo-starter/` for a multi-service layout starter combining bot, API, dashboard, worker, env template, and Docker Compose.
- `assets/docker/` for basic container deployment artifacts.

## References

Read these only if needed:
- `references/discord-bot-planning.md`
- `references/discord-js-patterns.md`
- `references/discord-py-patterns.md`
- `references/persistence-patterns.md`
- `references/postgres-prisma-drizzle-patterns.md`
- `references/deployment-patterns.md`
- `references/dashboard-api-patterns.md`
- `references/oauth-dashboard-patterns.md`
- `references/csrf-session-patterns.md`
- `references/webhook-patterns.md`
- `references/worker-queue-patterns.md`
- `references/moderation-dashboard-patterns.md`
- `references/monorepo-starter-patterns.md`
- `references/ticket-system-patterns.md`
- `references/ticket-advanced-patterns.md`
- `references/ticket-bot-starter-notes.md`
- `references/troubleshooting.md`
