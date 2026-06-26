---
name: MySQL
slug: mysql
version: 1.0.1
description: Write correct MySQL queries with proper character sets, indexing, transactions, and production patterns.
metadata: {"clawdbot":{"emoji":"🐬","requires":{"bins":["mysql"]},"os":["linux","darwin","win32"]}}
---

## Quick Reference

| Topic | File |
|-------|------|
| Index design deep dive | `indexes.md` |
| Transactions and locking | `transactions.md` |
| Query optimization | `queries.md` |
| Production config | `production.md` |

## Character Set Traps

- `utf8` is broken—only 3 bytes, can't store emoji; always use `utf8mb4`
- `utf8mb4_unicode_ci` for case-insensitive sorting; `utf8mb4_bin` for exact byte comparison
- Collation mismatch in JOINs kills performance—ensure consistent collation across tables
- Connection charset must match: `SET NAMES utf8mb4` or connection string parameter
- Index on utf8mb4 column larger—may hit index size limits; consider prefix index

## Index Differences from PostgreSQL

- No partial indexes—can't `WHERE active = true` in index definition
- No expression indexes until MySQL 8.0.13—must use generated columns before that
- TEXT/BLOB needs prefix length: `INDEX (description(100))`—without length, error
- No INCLUDE for covering—add columns to index itself: `INDEX (a, b, c)` to cover c
- Foreign keys auto-indexed only in InnoDB—verify engine before assuming

## UPSERT Patterns

- `INSERT ... ON DUPLICATE KEY UPDATE`—not standard SQL; needs unique key conflict
- `LAST_INSERT_ID()` for auto-increment—no RETURNING clause like PostgreSQL
- `REPLACE INTO` deletes then inserts—changes auto-increment ID, triggers DELETE cascade
- Check affected rows: 1 = inserted, 2 = updated (counter-intuitive)

## Locking Traps

- `SELECT ... FOR UPDATE` locks rows—but gap locks may lock more than expected
- InnoDB uses next-key locking—prevents phantom reads but can cause deadlocks
- Lock wait timeout default 50s—`innodb_lock_wait_timeout` for adjustment
- `FOR UPDATE SKIP LOCKED` exists in MySQL 8+—queue pattern
- InnoDB default isolation is REPEATABLE READ, not READ COMMITTED like PostgreSQL
- Deadlocks are expected—code must catch and retry, not just fail

## GROUP BY Strictness

- `sql_mode` includes `ONLY_FULL_GROUP_BY` by default in MySQL 5.7+
- Non-aggregated columns must be in GROUP BY—unlike old MySQL permissive mode
- `ANY_VALUE(column)` to silence error when you know values are same
- Check sql_mode on legacy databases—may behave differently

## InnoDB vs MyISAM

- Always use InnoDB—transactions, row locking, foreign keys, crash recovery
- MyISAM still default for some system tables—don't use for application data
- Check engine: `SHOW TABLE STATUS`—convert with `ALTER TABLE ... ENGINE=InnoDB`
- Mixed engines in JOINs work but lose transaction guarantees

## Query Quirks

- `LIMIT offset, count` different order than PostgreSQL's `LIMIT count OFFSET offset`
- `!=` and `<>` both work; prefer `<>` for SQL standard
- No transactional DDL—`ALTER TABLE` commits immediately, can't rollback
- Boolean is `TINYINT(1)`—`TRUE`/`FALSE` are just 1/0
- `IFNULL(a, b)` instead of `COALESCE` for two args—though COALESCE works

## Connection Management

- `wait_timeout` kills idle connections—default 8 hours; pooler may not notice
- `max_connections` default 151—often too low; each uses memory
- Connection pools: don't exceed max_connections across all app instances
- `SHOW PROCESSLIST` to see active connections—kill long-running with `KILL <id>`

## Replication Awareness

- Statement-based replication can break with non-deterministic functions—UUID(), NOW()
- Row-based replication safer but more bandwidth—default in MySQL 8
- Read replicas have lag—check `Seconds_Behind_Master` before relying on replica reads
- Don't write to replica—usually read-only but verify

## Performance

- `EXPLAIN ANALYZE` only in MySQL 8.0.18+—older versions just EXPLAIN without actual times
- Query cache removed in MySQL 8—don't rely on it; cache at application level
- `OPTIMIZE TABLE` for fragmented tables—locks table; use pt-online-schema-change for big tables
- `innodb_buffer_pool_size`—set to 70-80% of RAM for dedicated DB server
