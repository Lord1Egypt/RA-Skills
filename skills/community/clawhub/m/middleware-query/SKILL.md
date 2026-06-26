---
name: middleware-query
description: Natural-language read-only querying for MySQL, Redis, and MongoDB with explicit connection configuration (host, port, username, password), guarded query planning, and deterministic script executors. Use when users ask to query local databases/middleware in natural language, inspect Redis keys/values, run Mongo filters/aggregations, or retrieve SQL data safely.
---

# Middleware Query Skill

Implement natural-language query workflows with strict safety controls.

## 1) Collect required inputs

Require all connection parameters explicitly for each datasource:

- `host`
- `port`
- `username`
- `password`
- optional: `database` (MySQL/Mongo), `db` (Redis logical DB)

Store connection profiles in `scripts/connections.json` (or provide env vars) before execution.

Use `scripts/connections.example.json` as a template and keep real `connections.json` local-only (gitignored).

Prefer middleware-list config with env/alias entries, e.g. `{"redis":[{"env":"local","alias":"main",...}]}` and use profiles like `redis.local` or `redis.main`.

## 2) Enforce read-only safety

Always keep operations read-only:

- SQL: `SELECT`, `WITH`, `EXPLAIN SELECT` only
- Redis: `GET`, `MGET`, `HGET`, `HGETALL`, `SMEMBERS`, `ZRANGE`, `SCAN`, `TTL`, `TYPE`
- Mongo: `find`, `count_documents`, `aggregate` with read-only stages

Reject write/dangerous operations.

## 3) Prefer deterministic executors

Use scripts under `scripts/`:

- `nl_query.py` (single command entry: NL -> plan -> guard -> execute)
- `planner_llm.py` (LLM NL -> plan JSON with retry repair)
- `plan_schema.py` + `references/plan-schema.json` (JSON Schema validation)
- `router_nl.py` (rule-based fallback)
- `planner_guard.py` (semantic guard)
- `execute_plan.py` (validated plan execution)
- `query_sql.py`
- `query_redis.py`
- `query_mongo.py`

Pass validated parameters; never execute free-form shell commands for database access.

## 4) Output format

Return:

1. Datasource + profile used
2. Executed query/operation (sanitized)
3. Row/document/key count
4. Tabular/JSON preview (truncated)
5. Short interpretation in Chinese

## 5) Configuration sources

Priority order:

1. Explicit CLI args
2. Env vars (see `references/config.md`)
3. `scripts/connections.json`

Fail with clear error if any required field is missing.

## 6) Reference docs

Read when needed:

- `references/config.md`: connection and env conventions
- `references/safety-policy.md`: guardrails and denylist
- `references/examples.md`: common command examples
