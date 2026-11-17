# IBD Companion

[English](README.md) | [简体中文](README.zh-CN.md)

IBD Companion is an AI-assisted, local-first OpenClaw skill for privately
organizing personal inflammatory bowel disease (IBD) records, including
Crohn's disease and ulcerative colitis. It uses AI as a natural-language layer
over a structured local SQLite database, making it easier to record and query
the disease history and to prepare clearer information for clinical visits.

It is a recordkeeping and planning aid. It is not a diagnostic, prescribing,
or emergency-care tool.

## Core capabilities

1. **AI-assisted local IBD record.** Organizes the personal disease profile,
   biologic infusions and their linked lab results, annual or large reviews,
   and daily symptoms. Users can record or retrieve information through natural
   conversation instead of manually navigating database tables.
2. **Low-friction daily logging.** Symptoms and possible factors can be logged
   on demand, for example what was eaten and what symptoms followed. An
   optional daily reminder mode is planned; reminder delivery currently
   requires separate configuration and remains off by default.
3. **Personal pattern exploration (in progress).** Long-term symptom, food,
   sleep, stress, and other factor records can support exploratory comparisons
   of possible personal triggers. These results do not establish medical
   causality.
4. **AI-assisted checkup organization and visit preparation.** Keeps lab
   values, endoscopy, imaging, pathology, source reports, and confirmed
   clinician conclusions connected to the appropriate infusion or review.
   This makes the history easier to query and summarize before a clinical
   conversation.
5. **Treatment and review planning.** Tracks infusion schedules, changes,
   completion status, linked monitoring, and annual or other large-review
   plans without silently changing the treatment cadence.
6. **Local privacy and medical safety.** Real health data stays in a local
   SQLite database outside Git. The system supports recording, organization,
   and descriptive review, but does not diagnose, prescribe, or replace a
   clinician's judgment.

## Quick start and practical use

On first use, either CLI creates an empty private database if the configured
path does not yet exist. When using OpenClaw, record or retrieve information in
natural language instead of navigating database tables directly. For example:

- “Record two bowel movements today, soft-formed stool, pain score 1, usual for me.”
- “I drank coffee today and felt bloated in the evening.”
- “When is my next infusion?”
- “Summarize my symptoms, infusions, and checkups from the last 30 days.”

External reminder delivery is optional and off by default. It must be
explicitly configured before it can send notifications.

## First-time setup (optional)

A new user may begin daily logging immediately, or set up information gradually:

1. stable disease profile;
2. current clinician-confirmed treatment plan;
3. clinician-confirmed large-review plan;
4. personal usual-state symptom baseline; and
5. optional external reminders.

Every step may be skipped and completed later. The disease profile contains only
stable disease context; treatment and review schedules are separate plans, and
must come from an explicitly confirmed clinician arrangement. The agent should
ask for one item at a time and must not infer missing schedules or medical facts.

### Recording from photos and reports

For report intake, a multimodal model with image and PDF understanding is
recommended. It can help read a lab report, endoscopy report, imaging report,
or discharge summary and prepare structured values for this local database.

Before saving, verify extracted values against the source report, including the
unit, report-specific reference range, and abnormal flag. Preserve source
wording for narrative findings, and leave uncertain information empty. The
included Python scripts do not perform OCR themselves; image/PDF understanding
depends on the agent platform and selected model.

### Built-in metrics

New databases initialize these six medicine-agnostic starter metrics:

| Metric | Default unit |
| --- | --- |
| C-reactive protein (CRP) | mg/L |
| Erythrocyte sedimentation rate (ESR) | mm/h |
| Hemoglobin (HGB) | g/L |
| White blood cell count (WBC) | 10^9/L |
| Platelet count (PLT) | 10^9/L |
| Albumin | g/L |

### Add your own metrics

The starter list is intentionally medicine-agnostic. When using an agent,
you can request a new metric in natural language, for example: “Please add
infliximab level to my long-term tracking; use a numeric value in μg/mL.” The
agent should confirm the definition from an actual report or care plan before
adding it. The equivalent CLI command is:

```bash
python3 scripts/ibd_db.py metric-add \
  --code infliximab_level \
  --name "Infliximab level" \
  --value-type numeric \
  --default-unit "μg/mL"
```

Use a stable lowercase `snake_case` code. Choose `numeric` for a measured
value and `qualitative` for a text result. The default unit is only a prompt:
each recorded result keeps the unit, reference range, and abnormal flag shown
on its source report. Existing metric definitions are never deleted; use
`metric-deactivate --code <code>` to stop new entries while keeping history.

## Privacy model

The SQLite database is the sole source of truth and lives outside this
repository by default:

```text
${IBD_DB_PATH:-${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/private/ibd/ibd.sqlite3}
```

Do not commit databases, attachments, exported reports, real medical records,
or identifying health information. The included `.gitignore` blocks common
database and private-data paths, but it is not a substitute for reviewing every
commit.

### Storage safeguards and execution scope

The supported storage platform is POSIX (Linux/macOS). Use a dedicated directory
owned by your account with mode `0700`. Every open enforces mode `0600` on the
database and existing WAL, SHM, and rollback-journal files; unsafe ownership,
symbolic/hard links, non-regular files, and permission failures stop the command.
An existing directory with broader permissions is rejected, not automatically
modified. Choose a private directory; do not point the tracker at a shared folder.
Only the database directory is checked, not all ancestor ACLs or remote-filesystem
policies. Use trusted local storage. Permissions are not encryption and do not
protect against administrators or programs running as your account.

Both CLIs print a storage disclosure on stderr before opening the database;
stdout remains JSON. Even a summary command can initialize or migrate storage.
Agent-driven writes still require the confirmations in `SKILL.md`.

The workflow needs local execution of the two bundled Python CLIs and reading
its bundled text guides only, not network, messaging, package installation, or
access to unrelated files. The `allowed-tools` declaration is not an OS sandbox;
configure host-level command restrictions where available. The scripts themselves
do not transmit records. Any health text given to an AI model is subject to that
platform/model's data handling; local database storage does not imply offline AI.

Interaction follows the user's preferred language. Chinese prompts are examples,
and bilingual documentation, Unicode units, and Chinese test fixtures are
intentional. The CLI's seeded labels and legacy `Asia/Shanghai` setting are
Chinese-oriented defaults; event timestamps require explicit timezone offsets.
Existing stored labels and dates are not silently translated or reinterpreted.

### Backup and recovery

The database is one private SQLite file. Before an upgrade and at regular
intervals, make an encrypted or otherwise access-controlled copy outside the
repository. Avoid copying while another command is writing; a simple local
example after commands have finished is:

```bash
cp ~/.openclaw/private/ibd/ibd.sqlite3 ~/PrivateBackups/ibd-YYYY-MM-DD.sqlite3
```

To recover, keep the backup private and point `IBD_DB_PATH` at that copy, or
replace the active database only after making a separate safety copy. Never
attach a real database to an issue, commit, or public release.

## Requirements

- Python 3.10 or newer
- SQLite support from the Python standard library
- OpenClaw for skill-driven use; the command-line scripts also run directly

No third-party Python packages are required.

Repository releases (for example, `v0.1.0`) identify published code snapshots.
The private database is initialized and maintained with the current schema.

## Install

Clone the repository into the OpenClaw workspace skills directory:

```bash
git clone https://github.com/denniscriss/ibd-companion.git \
  ~/.openclaw/workspace/skills/ibd-companion
```

Initialize or migrate the private database. This is the recommended first step:

```bash
python3 scripts/ibd_care.py init
```

That creates the current private database structure. The database is also
created automatically on first use of either CLI if the configured path does
not yet exist.

To use a different database location, set `IBD_DB_PATH` for the command:

```bash
IBD_DB_PATH=/path/to/private/ibd.sqlite3 python3 scripts/ibd_care.py init
```

## Command overview

The base tracker handles symptoms, factors, metric definitions, injections,
checkups, results, and internal reminder rows:

```bash
python3 scripts/ibd_db.py --help
```

The care-context extension handles the disease profile, treatment and review
plans, review hierarchy, reports, confirmed assessments, and symptom baselines:

```bash
python3 scripts/ibd_care.py --help
```

Read `SKILL.md` before using the commands. It contains the safety boundaries,
source-of-truth rules, and explicit-confirmation requirements that keep unlike
medical meanings from being mixed together.

For the relational data-entry workflow and rules for mapping facts to tables,
read [references/data-entry.md](references/data-entry.md).

## Test

Tests use temporary databases and do not touch the default private database:

```bash
python3 -m unittest discover -s scripts -p 'test_ibd_*.py' -v
```

## Repository layout

```text
SKILL.md                 OpenClaw workflow and safety rules
references/schema.md     Data-model and migration documentation
references/data-entry.md Data-entry workflow and custom-metric rules
scripts/ibd_db.py        Base SQLite tracker and CLI
scripts/ibd_care.py      Care-context extension and CLI
scripts/test_ibd_*.py    Automated tests using temporary databases
```

## Safety boundaries

- Preserve source wording and unknown values; do not invent medical facts.
- Never infer disease activity or causality from symptoms, metrics, or factor
  comparisons.
- Never change medication or treatment cadence from generated analysis.
- Record a clinician assessment only from an explicit confirmed source.
- Treat urgent or red-flag symptoms as a reason to seek professional care, not
  as a routine trend-analysis task.
- External notifications require separate user approval and configuration.

## License

MIT. See `LICENSE`.
