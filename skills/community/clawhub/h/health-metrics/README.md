# health-metrics

An **Agent Skill** for **Apple Health Auto Export** reporting and logging. It lets an agent
(OpenClaw, Claude Code, or any tool that reads the portable `SKILL.md` format) ingest Apple
Health Auto Export JSON feeds into a local DuckDB database and render offline, self-contained
HTML dashboards plus a Markdown daily digest — activity rings, training load, sleep, vitals,
and per-workout maps.

No web server, no scheduler, no Python packages beyond the stdlib + the `duckdb` CLI. Runs on
demand whenever new export files land.

## Quick start

```bash
python3 scripts/ingest.py && python3 scripts/report.py -o <OUT_DIR>
```

- `ingest.py` parses the Apple Health Auto Export daily JSON and upserts into DuckDB (idempotent).
- `report.py -o <OUT_DIR>` renders all dashboards into a directory you choose.

Or use the one-command runner, which ingests first and (on macOS/iCloud) force-downloads any
evicted placeholder files before reading them:

```bash
bash scripts/run.sh daily-md [YYYY-MM-DD] [OUT_DIR]   # Markdown daily summary (default: today)
bash scripts/run.sh html [OUT_DIR]                    # full HTML dashboard set
bash scripts/run.sh ingest                            # materialize + ingest only
```

> **macOS / iCloud note:** if the source folders live in iCloud Drive with "Optimize Mac
> Storage" on, reads can fail with `Resource deadlock avoided` until files are downloaded.
> `run.sh` handles this automatically; the permanent fix is Finder → right-click each source
> folder → **Keep Downloaded**. See [`SKILL.md`](SKILL.md) for details.

Source folders and the database location are configurable via environment variables
(`HEALTH_METRICS_DIR`, `HEALTH_WORKOUTS_DIR`, `HEALTH_DB_PATH`), with sensible defaults.

## Learn more

- **[`SKILL.md`](SKILL.md)** — the skill entry point: prerequisites, workflow, configuration, and
  every runnable stage.
- **[`references/architecture.md`](references/architecture.md)** — internals (data flow, ingestion
  pattern, report conventions, `scripts/lib/` helpers).
- **[`references/schema.md`](references/schema.md)** — the DuckDB table reference.

## Data & privacy

The DuckDB database is **personal, sensitive health data**. It is created on first ingest, lives
**outside** this repository (default `~/.local/state/health-metrics/health.duckdb`), and is never
committed, published, or bundled.

## License

[MIT No Attribution (MIT-0)](LICENSE).
