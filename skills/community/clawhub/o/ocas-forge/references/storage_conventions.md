# OCAS Storage Conventions

Spec Version: 1.0.3
Author: Indigo Karasu

Changes from 1.0: replaced workspace dot-folder convention with centralized storage under {agent_root}/commons/; defined separate roots for data, journals, and databases; added LadybugDB database convention; added intake directory convention; clarified cross-skill access rules; updated initialization and validation sections.

---

## Purpose

This document defines the standard storage conventions for OCAS skills. All skills that persist state must follow these conventions to ensure consistency, auditability, and interoperability across the suite.

---

## Storage Roots

All persistent OCAS data lives under a single central root: `{agent_root}/commons/`.

Three sub-roots, one per data class:

```
{agent_root}/commons/
  data/       — skill state, configuration, and JSONL logs
  journals/   — journal files (telemetry, OKR evaluation)
  db/         — LadybugDB graph databases (Elephas and Weave only)
```

No skill writes outside `{agent_root}/commons/`. No skill writes inside the skill package directory. No skill writes into another skill's data or journal directory.

---

## Data Directory

### Location

```
{agent_root}/commons/data/{skill-name}/
```

The `{skill-name}` must match the skill's hyphenated identifier exactly: `ocas-scout`, `ocas-elephas`, `ocas-weave`.

### Required Structure

```
{agent_root}/commons/data/{skill-name}/
  config.json
```

### Typical Full Structure

```
{agent_root}/commons/data/{skill-name}/
  config.json
  {primary_log}.jsonl
  decisions.jsonl
  reports/
  artifacts/
  staging/       — temporary import/export files (for skills that bulk-process data)
```

---

## Journal Directory

### Location

```
{agent_root}/commons/journals/{skill-name}/YYYY-MM-DD/{run_id}.json
```

One file per run. Date directory created automatically. File named by `run_id`.

### Structure

```
{agent_root}/commons/journals/ocas-scout/
  2026-03-17/
    r_a7f2c1.json
    r_b3e8d2.json
  2026-03-18/
    r_c91f4a.json
```

Champion and challenger runs for the same comparison group live in the same date directory:

```
{agent_root}/commons/journals/ocas-rally/
  2026-03-17/
    cg_5cfa2c1/
      champion.json
      challenger.json
```

### Conventions

- Journal files are written atomically (write to `.tmp`, then rename).
- Journal files are immutable after write. Never edit.
- Runs missing journal files are invalid per `spec-ocas-journal.md`.

---

## Database Directory

### Location

```
{agent_root}/commons/db/{skill-name}/
```

Only for skills that maintain LadybugDB graph databases. Currently: `ocas-elephas` and `ocas-weave`.

### Structure

```
{agent_root}/commons/db/ocas-elephas/
  chronicle.lbug
  config.json
  staging/
  intake/
    {signal_id}.signal.json
    processed/

{agent_root}/commons/db/ocas-weave/
  weave.lbug
  config.json
  staging/
```

The `.lbug` file is managed exclusively by LadybugDB. Never read or modify `.lbug`, `.wal`, `.shadow`, or `.tmp` files directly.

---

## Intake Directories

Skills that accept signals from other skills use intake directories under their data root.

```
{agent_root}/commons/data/{skill-name}/intake/
  {signal_id}.json      — incoming signal files
  processed/            — moved here after consumption
```

See `spec-ocas-interfaces.md` for which skills publish to which intake directories and what file formats they use.

---

## File Types and Conventions

### config.json

Every skill's configuration file. Must include `ConfigBase` fields from `spec-ocas-shared-schemas.md`: `skill_id`, `skill_version`, `config_version`, `created_at`, `updated_at`.

Config is the only mutable JSON file in the data directory. All other data files are append-only.

### JSONL Files (Append-Only Logs)

Primary data storage uses JSON Lines format: one complete JSON object per line.

Conventions:
- Extension: `.jsonl`
- Append-only. Lines must not be edited or deleted after write.
- Each record includes a unique `id` field and a `timestamp` field in ISO 8601 format.
- Records are ordered chronologically.

Common files:
- `decisions.jsonl` — DecisionRecord entries
- `events.jsonl` or `{domain}_events.jsonl` — log events
- `signals.jsonl` — emitted signals
- `candidates.jsonl` — proposed Chronicle candidates

### reports/ Directory

Human-readable output artifacts. Any format (Markdown, JSON, PDF). Generated artifacts, not source-of-truth data.

### artifacts/ Directory (Optional)

Stored evidence, drafts, or intermediate outputs supporting decision traceability.

### staging/ Directory (Optional)

Temporary files for bulk operations (CSV imports, export buffers). Contents are transient and may be deleted after the operation completes.

---

## Naming Conventions

Files: `snake_case`. Descriptive names indicating content: `research_events.jsonl` not `data.jsonl`.

Directories: `snake_case`.

Record IDs: short prefix indicating record type, underscore, unique hash or UUID. Examples: `sig_a7f2c1`, `dec_91d28e1`, `r_5cfa2c1`.

Skill names: hyphenated, matching the skill's declared identifier. `ocas-scout` not `scout` or `ocas.scout`.

---

## Retention and Cleanup

Skills define retention policies in `config.json`.

Standard retention fields:
- `retention.days` — days to retain log entries (0 = indefinite)
- `retention.max_records` — maximum records per JSONL file before rotation

When a JSONL file exceeds `max_records`, rotate it:
1. Rename current file with date suffix: `events.jsonl` → `events.2026-03-10.jsonl`
2. Create new empty `events.jsonl` for new records
3. Archived files remain until retention period expires

Skills must not silently delete data. Expired data is removed by explicit maintenance operations only.

---

## Cross-Skill Access

Skills must not read or write another skill's data or journal directory.

Cross-skill data sharing uses only:
- Chronicle queries (via `elephas.query`)
- Weave queries (read-only)
- Defined intake directory drops (see `spec-ocas-interfaces.md`)
- Journal emission and Elephas ingestion

---

## Initialization

When a skill's data root does not exist on first run:
1. Create `{agent_root}/commons/data/{skill-name}/`
2. Write default `config.json` with ConfigBase fields and skill-specific defaults
3. Create required empty JSONL files
4. Create `{agent_root}/commons/journals/{skill-name}/` directory
5. Create intake directories if the skill accepts signals
6. Log initialization as a DecisionRecord

Skills initialize automatically rather than failing on missing storage.

---

## Validation

Skills with validation scripts check:
- Data root exists at `{agent_root}/commons/data/{skill-name}/`
- Journal root exists at `{agent_root}/commons/journals/{skill-name}/`
- `config.json` is valid JSON with required ConfigBase fields
- JSONL files contain valid JSON on every line
- No orphaned references
- Retention policies are being respected
- No data written outside the skill's own directories