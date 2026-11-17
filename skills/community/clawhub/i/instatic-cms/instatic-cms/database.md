# Database and Stack

## Engines
- Selected by `DATABASE_URL`: `sqlite:<file>` or `postgres://...`. Same image and code run either; default for a single-host install is SQLite.
- Rules that keep both dialects alive: repositories use ANSI SQL only (five Postgres-isms banned), JSON columns end in `_json`, timestamps bind from JS as ISO 8601 strings, migrations split per dialect with identical IDs in identical order (parity-gated by tests).

## Storage model
- Nearly everything lives in `data_tables` (schema definitions) + `data_rows` (values in `cells_json`). Content entries, pages, visual components, and saved layouts are all rows; the system tables are `pages`, `components`, `layouts`.
- Uploaded media and published artifacts live in `UPLOADS_DIR`, not the database. Backups must capture both the database and the uploads tree.

## Boot sequence
`server/index.ts`: open DB, run migrations (tracked in `_migrations`), sync system roles, activate plugins, serve. Fail-fast: a failed migration exits. A failing plugin logs and the server continues.

## Health
- `GET /health` unauthenticated, used by the container healthcheck.
- Boot log line: `[server] Listening on http://localhost:<PORT>`.

## SQLite specifics
- Single file at `DATABASE_URL` path (upstream sqlite compose: `/app/data/cms.db` on a named volume).
- Consistent live snapshot without stopping the server: open readonly and `VACUUM INTO '<new file>'`, copy the file out, remove it from the container. Postgres mode: `pg_dump` the service.
