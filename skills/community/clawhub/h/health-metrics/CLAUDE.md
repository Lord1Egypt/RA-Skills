# CLAUDE.md

This repository **is** an Agent Skill named `health-metrics` (portable SKILL.md format, usable by
OpenClaw, Claude Code, and other agents). The skill ingests Apple Health Auto Export JSON into a
local DuckDB database and renders offline HTML dashboards + a Markdown daily summary.

Start here:

- **`SKILL.md`** — what the skill does, prerequisites, the normal workflow, configuration
  (`HEALTH_METRICS_DIR` / `HEALTH_WORKOUTS_DIR` / `HEALTH_DB_PATH`), and every runnable stage.
- **`references/architecture.md`** — internals: data flow, ingestion pattern, report conventions,
  the `scripts/lib/` helpers, and the CSS `.replace()` convention.
- **`references/schema.md`** — the DuckDB table reference (the full analysis surface).

Executable code lives in `scripts/` (with shared helpers in `scripts/lib/`). The DuckDB file is
per-person sensitive data — it lives outside this tree (default
`~/.local/state/health-metrics/health.duckdb`) and is never committed or bundled (see
`.gitignore` / `.clawhubignore`).

Normal workflow:

```bash
python3 scripts/ingest.py && python3 scripts/report.py -o <OUT_DIR>
```
