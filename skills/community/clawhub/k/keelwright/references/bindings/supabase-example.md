# Binding (example) — Supabase / Postgres stack

**Status: OPTIONAL EXAMPLE, not part of the engine.** The keelwright engine is stack-agnostic;
this file shows how to encode *one specific stack's* gates as a binding. It is a worked example
alongside `flutter-example.md` and `python.md` — copy and adapt it, or ignore it if you don't use
Supabase. Nothing here is required by the core skill.

Its purpose is to demonstrate that stack-specific risks (row-level-security holes, migration
drift, environment coupling) become *machine-checkable gates* the same way generic ones do.

---

## Stack-specific security greps (Gate 1, second layer)

Generic SAST (Semgrep) doesn't know your platform's footguns. Grep the **staged diff** on added
lines so these block the commit like any R1/R2 finding:

```bash
# RLS disabled or wide-open policy — the classic Supabase data-leak
git diff --cached | grep "^+" | grep -iE "using *\( *true *\)"          # USING (true) = every row public
git diff --cached | grep "^+" | grep -iE "disable row level security"    # RLS turned off

# Privileged key used where the client can see it (service_role bypasses RLS entirely)
git diff --cached | grep "^+" | grep -iE "service_role|SERVICE_ROLE_KEY"

# Direct table grant to anon/authenticated without a policy behind it
git diff --cached | grep "^+" | grep -iE "grant .* to (anon|authenticated)"
```

Any hit → **block the commit**, treat as CRITICAL (this is R1/R3 for data-access logic). A row-level
security policy of `USING (true)` is the SQL equivalent of `authorization: allow-all` — exactly the
business-logic hole R3 exists to catch.

## Schema-drift gate (maps to the "schema drift" failure mode)

- **All schema changes go through migration files only** (e.g. `supabase/migrations/*.sql`). A
  schema edit that is not a committed migration is drift — block it.
- Verification: the migration applies cleanly to a fresh/dev database AND is idempotent-safe. Never
  hand-edit the live schema outside a migration.
- This is the DB analogue of the verification gate: the migration file on disk is the artifact of
  record, not "I changed the table."

## Environment-coupling gate

- Never edit `.env` / secret files as part of a feature (that's R2 territory — secrets don't live in
  the repo, and an agent silently rewriting `.env` breaks the environment).
- Separate dev and prod projects; a migration proven on dev is promoted to prod deliberately, not
  auto-applied. This pairs with the **post-deploy validation loop** (`phases.md`): after promoting a
  migration to prod, compare error/latency metrics and auto-revert (a new migration that undoes it)
  if they regress.

## Quality / structural gates

Same as any stack — the structural-integrity gate (`writing-code.md`) applies unchanged: jscpd for
duplication, boundaries/cycle tools for your app language (madge/eslint-boundaries for a TS frontend,
import-linter for a Python backend). Postgres functions/triggers: keep them small and reviewed like
any other logic (R3).

## Why this is a binding, not core

RLS, migrations-only, dev/prod split, and no-local-Docker are **specific to a Supabase/Postgres
workflow**. Baking them into the engine would make keelwright less universal. Encoding them here —
as greppable, blocking checks — is exactly the intended extension pattern: the engine stays generic,
your stack's footguns become machine gates in your binding.
