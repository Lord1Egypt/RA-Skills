# Setup — Prisma

Read this on first use to load user preferences. Do not interview the user.

## Your Attitude

Prisma is pleasant until a migration meets real data or a serverless deploy meets a connection limit. Work from the schema and the emitted SQL, not from the API surface: name what the client will actually send before recommending a change. Be direct about what Prisma cannot express, and hand the user the raw-SQL or migration escape hatch instead of contorting the client.

## How To Load Preferences

1. Read `~/Clawic/data/prisma/config.yaml` if it exists. Apply its values.
2. For anything absent, use the defaults in the Configuration table of `SKILL.md` — do not ask.
   - `provider: postgresql`, `prisma_major: 6`, `pooler: none`, `deploy_target: node-server`, `migration_workflow: migrate`, `id_style: cuid`, `naming_convention: camel-with-map`, `default_take: 50`, `destructive_confirm: true`.
3. Read `~/Clawic/data/prisma/memory.md` for prior context (their schema shape, hosting, recurring pain points). Absence is fine; proceed without comment.
4. Prefer evidence over stored values when both exist: an open `schema.prisma`, a `DATABASE_URL` scheme, or a lock file names the real provider and version. Update the stored value when the project contradicts it.

Work from defaults immediately. Never open with questions about the stack, priorities, or how proactive to be.

## Recording Preferences (only when the user declares one)

Write to config or memory **only** when the user states a preference in the course of the work — never as a preflight questionnaire.

- User names a provider, hosting target, pooler, ID style, or naming convention → update the matching key in `~/Clawic/data/prisma/config.yaml`.
- User expresses a stance (migrations applied directly vs handed back as SQL, whether raw SQL is allowed, page size, transaction timeouts) → record it under the relevant preference area in `~/Clawic/data/prisma/memory.md`.
- User corrects earlier guidance → update the stored value so it is not repeated.

If the user has said nothing, store nothing.

## What Memory Holds

See `memory-template.md` for the file format. Track their schema domain and size, hosting and pooling topology, migration workflow, the failures they have already hit, and how much explanation they want — but only from what they actually reveal.
