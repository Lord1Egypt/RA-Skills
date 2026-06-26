# memory_consolidate

Incremental memory consolidation for OpenClaw. Reads daily logs and session transcripts, extracts structured facts/events/decisions/solutions, manages temperature-based lifecycle, and generates a compact `MEMORY_SNAPSHOT.md` for agent context injection.

## What it does

- Parses `memory/*.md` daily logs and OpenClaw session logs
- Classifies lines into facts, beliefs, events (issue/solution/decision/artifact/progress), and summaries
- Bilingual classification (Chinese + English)
- Temperature-based lifecycle: hot → warm → cold → archived
- Generates `MEMORY_SNAPSHOT.md` with high-signal items
- Health monitoring with SNR, archive ratio, and temperature distribution

## Install

1. Copy the `memory_consolidate/` directory to your workspace `scripts/` folder.

2. Add the snapshot hook to `openclaw.json` so the agent reads it each session:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "bootstrap-extra-files": {
          "enabled": true,
          "paths": ["MEMORY_SNAPSHOT.md"]
        }
      }
    }
  }
}
```

3. Add a daily cron job:

```bash
openclaw cron add \
  --name "Memory Consolidation" \
  --schedule '{"kind":"cron","expr":"0 19 * * *","tz":"UTC"}' \
  --payload '{"kind":"agentTurn","message":"python3 scripts/memory_consolidate.py","thinking":"off","timeoutSeconds":180}' \
  --session-target isolated
```

4. (Optional) Edit `memory_consolidate/config.yaml` to tune parameters.

## Identity

Identity is auto-detected from workspace files:
- `IDENTITY.md` → assistant name
- `USER.md` → owner name, timezone, language

No manual identity config needed if these files exist.

## Configuration

Edit `memory_consolidate/config.yaml`:

```yaml
# Session log ingestion
ingest:
  session_logs: true
  session_hours: 24
  agent_ids: "main"  # or ["main", "worker"]

# Tag rules (project-specific keywords → tags)
tag_rules:
  myproject: ["myproject", "My Project"]

# Temperature, decay, snapshot limits — see config.yaml for all options
```

## Usage

```bash
# Run consolidation
python3 scripts/memory_consolidate.py

# Run with options
python3 -m memory_consolidate --verbose --dry-run --workspace /path/to/workspace

# Check health
python3 scripts/memory_consolidate_observe.py

# Full report
bash scripts/memory_consolidate_report.sh
```

## Module structure

```
memory_consolidate/
  config.py       — Config loading, identity parsing
  core.py         — Data structures, JSONL I/O, merge/upsert
  ingest.py       — Log parsing, bilingual classification patterns
  temperature.py  — Temperature scoring, decay, reinforcement
  archive.py      — Archiving, distillation, purge
  snapshot.py     — MEMORY_SNAPSHOT.md rendering
  health.py       — Health metrics (SNR, archive ratio)
  observe.py      — Health monitoring and reporting
  pipeline.py     — Semantic pipeline runner
  main.py         — Orchestration
  config.yaml     — User configuration
```
