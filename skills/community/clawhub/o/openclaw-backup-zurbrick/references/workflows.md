# Workflows

Use these after the basic backup / verify / restore flow is understood.

## Weekly verify

```bash
bash {baseDir}/scripts/weekly-verify.sh
```

Verifies all backup sets, prunes by daily/weekly/monthly retention, and cleans orphaned files.

## Monthly drill

```bash
bash {baseDir}/scripts/monthly-drill.sh
```

Runs a dry-run restore against the newest backup set and reports pass/fail.

## Pre-change snapshot

```bash
bash {baseDir}/scripts/pre-change-snapshot.sh
```

Creates a fast operational-only snapshot before config edits or gateway restarts.

## CI verification

- `.github/workflows/verify-backup.yml` builds a fixture backup, validates manifest checksums, extracts the archive, and checks critical files.

Use these workflows only after the core backup / restore path is working.
