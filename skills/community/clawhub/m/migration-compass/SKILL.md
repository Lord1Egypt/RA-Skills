---
name: migration-compass
version: 1.0.0
description: >
  Universal migration planner for any swap — framework to framework,
  library to library, language to language, database to database. Generates
  a step-by-step migration path with rollback points, parallel-run strategies,
  and the exact order to change things so nothing breaks in the middle.
  Because "we'll migrate gradually" is not a plan.
author: J. DeVere Cooley
category: everyday-tools
tags:
  - migration
  - planning
  - upgrades
  - transitions
metadata:
  openclaw:
    emoji: "🧭"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - architecture
---

# Migration Compass

> "Every failed migration has the same obituary: 'We started replacing everything at once, got halfway, ran out of time, and now we have two systems.'"

## What It Does

You need to migrate. Maybe it's Express → Fastify. Maybe it's JavaScript → TypeScript. Maybe it's MySQL → PostgreSQL. Maybe it's React class components → hooks. Maybe it's a monolith → microservices.

You know where you are. You know where you want to be. You don't know the **safe path between them** — the order that lets you change incrementally, validate at each step, and roll back if something goes wrong, all while keeping production running.

Migration Compass generates that path.

## The Migration Model

Every migration follows the same fundamental structure, regardless of what's being migrated:

```
STATE A (current) ────── TRANSITION ────── STATE B (target)
                    │
                    ├── Parallel Run Zone (both states coexist)
                    ├── Rollback Points (safe places to reverse)
                    ├── Validation Gates (proof each step worked)
                    └── Strangler Boundary (old → new interface)
```

### The Three Migration Laws

**Law 1: Never Big-Bang**
Change one thing at a time. Validate. Proceed or roll back. A migration that requires changing everything simultaneously is not a migration — it's a rewrite disguised as a migration.

**Law 2: Parallel Before Replace**
The new system must run alongside the old system before it replaces it. You need proof it works in production before you remove the old one.

**Law 3: Every Step Must Be Deployable**
At no point during the migration should the codebase be in a state that can't be deployed to production. Every commit is a valid checkpoint.

## Migration Types

### Type 1: Library Swap
*Replace one library with another (same language, same purpose)*

Example: `moment.js` → `date-fns`

```
COMPASS ROUTE:
├── Step 1: AUDIT
│   ├── Find every import of moment (grep analysis)
│   ├── Catalog every moment function you use
│   ├── Map each moment function → date-fns equivalent
│   └── Identify any moment features with no date-fns equivalent
│
├── Step 2: INSTALL PARALLEL
│   ├── npm install date-fns (alongside moment, not replacing)
│   ├── Create adapter module: src/utils/date-adapter.ts
│   │   └── Exports your date operations, internally calls moment OR date-fns
│   └── ✅ Deploy. Both libraries installed. Only moment used.
│
├── Step 3: MIGRATE CONSUMERS (one at a time)
│   ├── Change import from 'moment' → import from 'date-adapter'
│   ├── Do NOT change behavior — adapter calls moment internally
│   ├── ✅ Deploy after each file. Rollback = revert one file.
│   └── Repeat until all consumers use adapter
│
├── Step 4: SWAP INTERNALS
│   ├── Inside date-adapter, change implementation from moment → date-fns
│   ├── Run tests. Compare outputs.
│   ├── ✅ Deploy. If issues, revert adapter internals only (one file).
│   └── Monitor for edge cases (timezone, locale, formatting)
│
├── Step 5: CLEANUP
│   ├── Remove moment from package.json
│   ├── Optionally inline adapter (or keep for future flexibility)
│   ├── ✅ Deploy.
│   └── Total migration: N small PRs, zero downtime, full rollback at each step
│
└── ROLLBACK POINTS: Every step. Maximum rollback cost: 1 file revert.
```

### Type 2: Framework Migration
*Replace one framework with another (same language)*

Example: `Express` → `Fastify`

```
COMPASS ROUTE:
├── Step 1: AUDIT
│   ├── Catalog all routes (count, complexity, middleware usage)
│   ├── Catalog all middleware (auth, logging, CORS, etc.)
│   ├── Identify Express-specific patterns (req/res augmentation, etc.)
│   └── Map Express concepts → Fastify equivalents
│
├── Step 2: STRANGLER FACADE
│   ├── Introduce a reverse proxy (or route splitter) in front of Express
│   ├── All traffic → Express (no change in behavior)
│   ├── ✅ Deploy. Verify no change.
│   └── This proxy will later split traffic between Express and Fastify
│
├── Step 3: PARALLEL INSTANCE
│   ├── Stand up Fastify instance alongside Express
│   ├── Migrate ONE low-risk route (health check, static asset, etc.)
│   ├── Route proxy: /health → Fastify, everything else → Express
│   ├── ✅ Deploy. Verify Fastify serves /health correctly.
│   └── Rollback: Route /health back to Express
│
├── Step 4: INCREMENTAL ROUTE MIGRATION
│   ├── Migrate routes one at a time (or in small batches)
│   ├── Order: lowest risk → highest risk
│   │   ├── Static routes (no state, no auth)
│   │   ├── Read-only authenticated routes
│   │   ├── Write routes (mutations)
│   │   └── Complex routes (multi-step, transactional)
│   ├── For each route:
│   │   ├── Implement in Fastify
│   │   ├── Validate with parallel run (same request → both systems → compare)
│   │   ├── Switch proxy to Fastify
│   │   ├── ✅ Deploy. Monitor.
│   │   └── Rollback: Switch proxy back to Express
│   └── Repeat until all routes are on Fastify
│
├── Step 5: DECOMMISSION
│   ├── Remove Express from package.json
│   ├── Remove proxy (Fastify serves directly)
│   ├── ✅ Deploy.
│   └── Clean up any compatibility shims
│
└── ROLLBACK POINTS: Per-route. Maximum rollback: re-route one endpoint.
```

### Type 3: Language Migration
*Convert codebase from one language to another*

Example: `JavaScript` → `TypeScript`

```
COMPASS ROUTE:
├── Step 1: CONFIGURE
│   ├── Add tsconfig.json with strict: false (permissive start)
│   ├── Enable allowJs: true (JS and TS coexist)
│   ├── ✅ Deploy. Zero behavior change.
│
├── Step 2: RENAME (leaf nodes first)
│   ├── Dependency graph: find files with NO importers (leaf nodes)
│   ├── Rename .js → .ts (one file at a time)
│   ├── Add minimal types (any where needed to compile)
│   ├── ✅ Deploy after each batch.
│   └── Work inward: leaves → branches → trunk
│
├── Step 3: TIGHTEN
│   ├── Replace `any` with real types (one module at a time)
│   ├── Enable stricter tsconfig rules incrementally:
│   │   ├── noImplicitAny
│   │   ├── strictNullChecks
│   │   ├── strictFunctionTypes
│   │   └── strict: true (final)
│   ├── ✅ Deploy after each rule change.
│   └── Rollback: Disable the rule, fix later
│
├── Step 4: CLEANUP
│   ├── Remove allowJs when all files are .ts
│   ├── Remove any remaining @ts-ignore comments
│   └── ✅ Deploy.
│
└── ROLLBACK POINTS: Per-file during rename. Per-rule during tightening.
```

### Type 4: Database Migration
*Move from one database to another*

### Type 5: Architecture Migration
*Monolith to microservices, MVC to event-driven, etc.*

### Type 6: Version Migration
*Major version upgrade of a framework or library*

## The Compass Process

```
INPUT: What are you migrating from? What to? What's the current usage?

Phase 1: SURVEY
├── Analyze current usage of the source (what features, what patterns)
├── Map source concepts → target equivalents
├── Identify gaps (source features with no target equivalent)
├── Estimate per-component migration effort
└── Identify the riskiest components (most complex, most critical)

Phase 2: ROUTE PLANNING
├── Determine migration type (library, framework, language, DB, architecture)
├── Select migration strategy:
│   ├── Strangler Fig: Route-by-route replacement (best for services)
│   ├── Branch by Abstraction: Adapter layer swaps (best for libraries)
│   ├── Parallel Run: Both systems simultaneously (best for data stores)
│   └── Incremental Rewrite: File-by-file conversion (best for language)
├── Order components: lowest risk first → highest risk last
├── Define rollback points for each step
└── Estimate total duration and effort

Phase 3: VALIDATION GATES
├── For each step, define how to verify success:
│   ├── Tests that must pass
│   ├── Metrics that must be maintained (latency, error rate, throughput)
│   ├── Comparison criteria (old output == new output)
│   └── Monitoring alerts to watch
└── Define go/no-go criteria for each step

Phase 4: COMPASS OUTPUT
├── Ordered step-by-step plan
├── Per-step: what to do, how to verify, how to roll back
├── Risk assessment per step
├── Total effort estimate
├── Dependencies between steps
└── Parallel work opportunities (what can be done simultaneously)
```

## Output Format

```
╔══════════════════════════════════════════════════════════════╗
║                   MIGRATION COMPASS                         ║
║        From: moment.js → To: date-fns                       ║
║        Scope: 47 files, 126 usages                          ║
║        Estimated effort: 12 dev-hours                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ROUTE (5 steps, 0 downtime, full rollback at each step):   ║
║                                                              ║
║  [1] AUDIT (1h)                              ✅ deployable   ║
║  └── Map 126 usages across 47 files                         ║
║                                                              ║
║  [2] INSTALL + ADAPTER (2h)                  ✅ deployable   ║
║  └── date-adapter.ts wrapping moment → date-fns             ║
║  └── Rollback: delete adapter, keep moment                  ║
║                                                              ║
║  [3] REWIRE CONSUMERS (4h)                   ✅ deployable   ║
║  └── 47 files: import moment → import date-adapter          ║
║  └── Rollback: revert individual file imports               ║
║                                                              ║
║  [4] SWAP INTERNALS (3h)                     ✅ deployable   ║
║  └── Adapter: moment calls → date-fns calls                 ║
║  └── Rollback: revert adapter (1 file)                      ║
║                                                              ║
║  [5] CLEANUP (2h)                            ✅ deployable   ║
║  └── npm remove moment, inline adapter                      ║
║                                                              ║
║  RISK AREAS:                                                 ║
║  ├── Timezone handling differs (3 usages need manual review) ║
║  ├── Locale formatting differs for zh-CN and ar-SA           ║
║  └── moment.duration() has no exact date-fns equivalent      ║
║                                                              ║
║  PARALLEL OPPORTUNITIES:                                     ║
║  Steps 3 can be split across developers (per-directory)      ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- When someone says "let's just swap it out" (it's never "just")
- When planning any library, framework, or language migration
- When upgrading a major version with breaking changes
- When evaluating whether a migration is worth the cost
- When a migration is "halfway done" and stalled (Compass can re-route from current state)

## Why It Matters

80% of failed migrations fail for the same reason: they tried to change too much at once, had no rollback plan, and ended up with two half-working systems. The remaining 20% fail because they underestimated the scope.

Migration Compass eliminates both failure modes. Every step is small. Every step is deployable. Every step has a rollback. And the full scope is visible before you start.

Zero external dependencies. Zero API calls. Pure codebase analysis and planning.
