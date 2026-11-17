# Errors — SQLSTATE to Cause to Fix

Match on the five-character SQLSTATE, never on the message text: messages are localized and reworded between versions, codes are stable. The class (first two characters) tells you which subsystem is complaining. The nine most frequent codes are in SKILL.md (Error Codes); this is the working catalog.

## Class 23 — Integrity Constraint Violation

| Code | Name | Cause and fix |
|---|---|---|
| 23505 | unique_violation | A duplicate, or two concurrent inserts racing. Idempotent insert → `ON CONFLICT DO NOTHING/UPDATE`. If it fires on a sequence-backed key after a data load, the sequence is behind: `SELECT setval('t_id_seq', (SELECT max(id) FROM t))` |
| 23503 | foreign_key_violation | Parent missing, or a delete order problem. Check both directions: the message names the constraint, `\d+ table` names the columns |
| 23502 | not_null_violation | A column got NULL — often a rename or a default that was never applied during a migration |
| 23514 | check_violation | The CHECK is right and the data is wrong, or the CHECK was added `NOT VALID` and something new violates it |
| 23P01 | exclusion_violation | An exclusion constraint (overlapping ranges) rejected the row — this is the constraint working |

## Class 40 — Transaction Rollback

| Code | Name | Cause and fix |
|---|---|---|
| 40001 | serialization_failure | REPEATABLE READ/SERIALIZABLE conflict → retry the whole transaction with backoff. On a **replica** the same code means a recovery conflict (query cancelled by WAL replay) — a different fix entirely |
| 40P01 | deadlock_detected | A lock cycle; one transaction was chosen as victim. Retrying hides it — impose a consistent ordering (cycles and fixes in the locks guide) |
| 25P02 | in_failed_sql_transaction | An earlier statement in this transaction failed; everything is refused until `ROLLBACK`. In scripts, use savepoints or `ON_ERROR_STOP` |
| 25001 | active_sql_transaction | A statement that cannot run inside a transaction block (`CREATE INDEX CONCURRENTLY`, `VACUUM`) was wrapped by a framework |

## Class 53/57/58 — Resource and Operator Intervention

| Code | Name | Cause and fix |
|---|---|---|
| 53300 | too_many_connections | `max_connections` reached. Diagnose by state before raising anything (connections guide) |
| 53200 | out_of_memory | A backend could not allocate — usually `work_mem` × nodes × concurrency (SKILL.md Core Rules 5), or a runaway hash aggregate |
| 53100 | disk_full | Data or WAL filesystem full. Do not delete files in `pg_wal` by hand |
| 57014 | query_canceled | `statement_timeout`, a `pg_cancel_backend`, or a client-side cancel |
| 55P03 | lock_not_available | `lock_timeout` fired, or `NOWAIT` was requested. Working as designed — retry with backoff |
| 57P01 | admin_shutdown | The server or your backend was terminated (`pg_terminate_backend`, a restart, or the OOM killer) |
| 57P03 | cannot_connect_now | The server is starting up or in recovery — expected during failover, not an error to retry aggressively |
| 55006 | object_in_use | `DROP DATABASE` with sessions connected; terminate them first |
| 2BP01 | dependent_objects_still_exist | A drop blocked by dependents; `\d+` shows them. `CASCADE` only when you can name what it takes |

## Class 22/42 — Data and Syntax

| Code | Name | Cause and fix |
|---|---|---|
| 22P02 | invalid_text_representation | A string reached a typed column or parameter: empty string into an integer, an unknown enum label, malformed uuid or jsonb |
| 22001 | string_data_right_truncation | Value longer than `varchar(n)` — the argument for `TEXT` plus a CHECK (SKILL.md Core Rules 6) |
| 22003 | numeric_value_out_of_range | Integer overflow: an `int` primary key at 2.1 billion, or a `numeric(p,s)` too narrow |
| 22012 | division_by_zero | Guard with `nullif(denominator, 0)` |
| 22008 | datetime_field_overflow | An out-of-range or ambiguous timestamp, frequently a DST gap on `timestamp without time zone` |
| 42P01 | undefined_table | Wrong `search_path` more often than a wrong name — check with `SHOW search_path` |
| 42703 | undefined_column | Typo, a dropped column still referenced, or a quoted-identifier case mismatch (`"userId"` ≠ `userid`) |
| 42883 | undefined_function | No function with that argument *type* combination; usually a missing cast or a missing extension |
| 42501 | insufficient_privilege | Missing GRANT, missing schema `USAGE`, or RLS filtering the rows away (security guide) |
| 42P07 | duplicate_table | A migration ran twice; make DDL idempotent with `IF NOT EXISTS` where safe |
| 42804 | datatype_mismatch | Common in `UNION` branches and CASE arms with different types |

## Class 08/28/3D — Connection and Authentication

| Code / message | Cause and fix |
|---|---|
| 08006 connection_failure, 08003 connection_does_not_exist | The connection dropped: backend crash, network device timing out idle TCP, or the pooler recycling. Distinguish with the server log |
| 28P01 invalid_password | Wrong credentials, or `password_encryption` changed to scram without the user resetting their password |
| 28000 invalid_authorization_specification / "no pg_hba.conf entry" | The server is reachable and refusing on policy. Fix the rule and reload; first match wins (security guide) |
| 3D000 invalid_catalog_name | The database does not exist on this host — including "connected to the wrong environment" |
| "SSL SYSCALL error: EOF detected" | Not a Postgres-level error: the connection died mid-statement. OOM killer and idle-connection reapers are the usual suspects |

## Class 54 / XX — Limits and Corruption

| Code | Name | Cause and fix |
|---|---|---|
| 54000 | program_limit_exceeded | Most often an index row above ~2.7 kB (a third of an 8 kB page): index `md5(value)`, a prefix, or use a GIN/trigram index instead |
| 54001 | statement_too_complex | Generated SQL with thousands of `OR`s or a runaway recursive CTE — batch it or rewrite as a join against a VALUES list |
| 54011 | too_many_columns | The 1600-column ceiling; a schema telling you it wants a different shape |
| XX001 | data_corrupted | Stop. Take a file-level copy before anything else, check hardware, verify with `amcheck`, restore from backup (backup guide) |
| XX002 | index_corrupted | `REINDEX` the index; if it recurs, suspect a collation change from an OS upgrade (upgrades guide) |
| 58P01 | undefined_file | A file the catalog expects is missing — corruption, or someone deleted files under the data directory |

## Reading the Whole Error

An error is more than its code. `\errverbose` in psql (or `log_error_verbosity = verbose`) prints DETAIL, HINT, the constraint name, the schema and table, and the C source location. The DETAIL line usually contains the failing key value — enough to identify the row without any further query. Client libraries expose the same fields (`e.diag.constraint_name` in psycopg, `err.detail`/`err.constraint` in node-postgres, `PgError.ConstraintName` in Go drivers): logging only the message throws away most of the diagnosis.
