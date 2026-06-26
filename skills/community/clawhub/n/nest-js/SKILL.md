---
name: NestJS
slug: nestjs
version: 1.0.0
description: Build production-grade NestJS applications with correct module architecture, dependency injection, decorators, guards, pipes, interceptors, middleware, microservices, and testing patterns. Use this skill whenever the user mentions NestJS, Nest.js, Nest framework, or is building a Node.js API with decorators, modules, providers, controllers, or TypeScript-first backend patterns that follow NestJS conventions. Also trigger when the user references NestJS concepts like guards, pipes, interceptors, custom decorators, DTOs with class-validator, TypeORM/Prisma/Mongoose integration in Nest, GraphQL resolvers in Nest, or CQRS. This skill covers NestJS-specific patterns — for general Node.js traps (event loop, streams, async pitfalls), see the NodeJS skill.
metadata: {"clawdbot":{"emoji":"🐈","requires":{"bins":["node","npx"]},"os":["linux","darwin","win32"]}}
---

## Quick Reference

| Topic | File |
|-------|------|
| Module system, circular deps, dynamic modules | `modules.md` |
| DI, providers, injection scopes, custom providers | `dependency-injection.md` |
| Controllers, routing, request lifecycle | `controllers.md` |
| Guards, pipes, interceptors, middleware, filters | `lifecycle.md` |
| DTOs, validation, transformation | `validation.md` |
| Database integration (TypeORM, Prisma, Mongoose) | `database.md` |
| Testing: unit, integration, e2e | `testing.md` |
| Microservices, queues, events, WebSockets | `microservices.md` |
| Config, environment, secrets management | `config.md` |
| Performance, caching, serialization | `performance.md` |

## NestJS vs Plain Node.js — Key Differences

NestJS builds on Node.js/Express (or Fastify) but introduces an opinionated architecture. The main things that catch people:

- **Everything is a class with decorators** — `@Module`, `@Controller`, `@Injectable` are not optional annotations, they drive the DI container and module graph.
- **Module boundaries matter** — a provider is NOT globally available unless explicitly exported and imported. This is the #1 source of "Nest can't resolve dependency" errors.
- **Request lifecycle is layered** — Middleware → Guards → Interceptors (before) → Pipes → Handler → Interceptors (after) → Exception Filters. Order matters and each layer has a distinct job.
- **TypeScript is assumed** — decorators, metadata reflection (`reflect-metadata`), and `emitDecoratorMetadata` are load-bearing. Misconfigured `tsconfig.json` breaks DI silently.

## Critical Traps

- `@Injectable()` missing — class won't be in DI container, cryptic "resolve dependency" error
- Provider not in module's `providers` array — same error, different cause
- Provider not `exports`ed — importing module can't see it, even though the module is imported
- Circular module dependency — use `forwardRef(() => ModuleClass)` on BOTH sides
- Circular provider injection — use `forwardRef(() => ServiceClass)` + `@Inject(forwardRef(...))`
- `@Body()` empty — missing `Content-Type: application/json` header or body-parser not configured
- Validation not firing — forgot `app.useGlobalPipes(new ValidationPipe())` or missing `class-transformer`
- Guard returning `false` silently → 403 — no error message by default, must throw specific exception
- `@Res()` used → Nest loses response control — use `@Res({ passthrough: true })` or avoid `@Res()`
- Exception filter not catching — filter bound to wrong scope (method vs controller vs global)
- `onModuleInit` / `onModuleDestroy` — lifecycle hooks only fire if class is `@Injectable()` AND in providers
- `ConfigService.get()` returns `undefined` — env var not in `.env` or `ConfigModule` not imported in that module
- Fastify adapter — Express middleware won't work, must use Fastify equivalents
