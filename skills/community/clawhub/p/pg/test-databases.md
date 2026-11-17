# Test and Development Databases — Realistic Data, Fast Resets

Two goals in tension: tests must be fast and isolated, and rehearsals must run against production-shaped data. Use different mechanisms for each instead of one compromise that serves neither.

## Fast Isolation Between Tests

| Strategy | Reset cost | Trade-off |
|---|---|---|
| Transaction per test, rolled back at teardown | Microseconds | Fastest and cleanest — breaks for code that commits, uses multiple connections, or tests transaction behaviour itself |
| `TRUNCATE ... RESTART IDENTITY CASCADE` on the touched tables | Milliseconds | Works with committing code; must enumerate tables, and cascade order matters |
| `CREATE DATABASE test_x TEMPLATE test_seed` per worker | Tens to hundreds of ms | Real isolation for parallel test workers; the template must have no open connections |
| Restore a dump per test | Seconds | Only for a suite whose whole point is the restore path |
| Anything else | — | Start with transaction rollback; add template databases when parallelism arrives |

Template databases are the underused one: seed a database once, then `CREATE DATABASE t1 TEMPLATE seed` per worker. It copies files rather than replaying SQL, so it is far faster than re-running migrations, and each worker gets a genuinely separate database.

Speed knobs that only belong on a throwaway test cluster, never anywhere else: `fsync = off`, `full_page_writes = off`, `synchronous_commit = off`, data directory on tmpfs. Together they cut a suite's database time substantially; any of them on real data is a corrupted cluster after one power loss.

## Building a Seed That Finds Bugs

- Row counts should hit the shapes that break code: zero rows, one row, a row with every nullable column null, unicode and emoji in text, a very long string, negative and zero amounts, and a duplicate that should be rejected.
- Fixed IDs and fixed timestamps make failures reproducible; `now()` in a fixture makes a test that fails once a year at a DST boundary.
- Seed through the same migrations the application uses. A hand-maintained `schema.sql` drifts, and the drift is discovered in production.
- Volume matters for plan-shaped bugs: a query that seq-scans 50 rows happily will seq-scan 50 million the same way, and no test catches it. Keep a separate, larger dataset for plan rehearsals (below).

## Production-Shaped Data Without the Risk

A copy of production in a development environment is a breach waiting for a laptop. Anonymize at the point of copy, never afterwards:

- Restore into a scratch instance, run an anonymization script inside it, then dump the anonymized result. The un-anonymized copy never leaves that instance.
- Deterministic pseudonyms (`md5(email || salt)`) preserve join cardinality and uniqueness; random values destroy the distribution that makes the copy worth having.
- Keep the distribution, change the values: same row counts, same NULL ratios, same skew in `tenant_id`, same text lengths. Those are what drive plans.
- Drop what you cannot anonymize: payment details, tokens, session data, free-text fields that may contain anything.
- Where a copy is not permissible at all, `pg_dump --schema-only` plus generated data with the right distribution is second best — and enough for most plan work.

## Rehearsing Migrations and Plans

The number that matters for a migration is how long it holds a lock on real data volume, and you can only get it from real volume (migrations guide). Two practical routes:

- Restore the latest backup into a scratch instance and run the migration there, timed. This doubles as the restore drill (backup guide).
- On a platform with copy-on-write branching, branch production and run it on the branch — the same rehearsal at near-zero cost (managed guide).

For plan work, copying only the statistics is enough and much cheaper than copying data: `pg_dump --schema-only` plus the source's `pg_statistic` content (or `ANALYZE` on a representative sample) lets the planner produce production-like plans on a small database. Confirm the plan you get matches the production plan before trusting the experiment.

## CI

- One Postgres per CI job (a service container or an ephemeral instance), on the **same major version** as production — a suite green on 16 and deployed to 14 tests nothing about the version you run.
- Wait for readiness with `pg_isready`, not with a sleep. The most common flaky CI database failure is a connection made a second before the server is accepting.
- Run migrations from scratch on every CI run: that is the only place "migrations apply cleanly to an empty database" is verified. Separately, apply migrations to a restored copy at least before each release — clean-database success says nothing about a table with 50 million rows.
- Add a schema drift check: apply migrations, dump the schema, diff against the committed schema file. It catches the console-applied change nobody wrote a migration for.

## Assertions Inside the Database

`pgTAP` runs assertions as SQL (`has_table`, `col_is_pk`, `results_eq`), which is the right tool for testing constraints, triggers, RLS policies, and functions — the logic that lives in the database and is invisible to application tests. RLS in particular must be tested as the restricted role (`SET ROLE app_user`), because the owner bypasses policies by default (security guide) and every test will pass while production leaks.
