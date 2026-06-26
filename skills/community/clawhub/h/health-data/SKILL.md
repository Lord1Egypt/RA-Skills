---
name: health-data
description: Analyze Apple Health exports (export.zip or the exported folder) using xmlstarlet/jq to summarize activity, steps, sleep, and source counts. Trigger this skill when users ask about "health data", "sleep analysis", "activity summary", "Apple Health export", "steps report", or other Apple Health record audits.
---

# Purpose
The `health-data` skill provides deterministic helpers to read and summarize Apple Health backup exports. The bundled `health-data.sh` script understands the zipped export Apple Health lets you download and can also work against the unzipped folder with `export.xml`. Use this skill when you need to inspect record types, compute totals (steps, distance, sleep), or extract JSON for further analysis without sending the sensitive XML off-box.

# Safety
- Apple Health exports contain PII/PHI (biometric, sleep, location, heart-rate, etc.). Never publish the raw XML, upload the zip, or paste any values into third-party services without explicit consent and legal review.
- The script only reads data locally and cleans up its temporary extraction. Keep the exported zip/folder on disk-free space you control and delete it when the analysis is done.
- Running `summary` or `export-json` now emits a runtime PHI warning banner to stderr; treat every derived artifact as PHI/PII unless you have an explicit legal/research justification.
- The `export-json` command streams records instead of slurping them, warns on stderr after emitting 100,000 records without `--limit`, and supports `--out <file>` so you can save the JSON to a file created with 600 permissions instead of dumping to stdout.
- Request explicit confirmation before writing any derived health reports if the values are later shared with others (medical, legal, or employment contexts).

# Quick start
```bash
# List which HealthKit record types appear most often
health-data/health-data.sh list-types ~/Downloads/export.zip

# Summarize range, totals, and common sources
health-data/health-data.sh summary ~/Downloads/export.zip

# Get JSON records for steps (use jq to filter further)
health-data/health-data.sh export-json HKQuantityTypeIdentifierStepCount ~/Downloads/export.zip --limit 20
# Or save to a restricted file (600-permission) instead of stdout
health-data/health-data.sh export-json HKQuantityTypeIdentifierStepCount ~/Downloads/export.zip --limit 20 --out ~/Documents/steps.json
```

# Commands

## list-types <export-path>
Prints every `<Record type="...">` identifier in the export, sorted by frequency. Use this to understand which categories (steps, workouts, heart rate, etc.) are available before you dig into payloads.

## summary <export-path>
Reports:
- total record count and date coverage
- step count and walking/running distance sums (meters by default)
- counts of sleep analysis categories (asleep/in-bed)
- top five data sources by record volume

This command relies on `xmlstarlet` to query the XML so it stays fast even on large exports.

## export-json <record-type> <export-path> [--limit N] [--out <file>]
Pulls the requested record type into JSON so you can pipe it to `jq`, Python, or other tools. The command emits a runtime PHI warning banner on stderr, streams records instead of slurping them, warns after 100,000 emitted records when `--limit` is omitted, and supports `--out <file>` to save the JSON to a file created with 600 permissions. Supply `--limit` to avoid overwhelming the reader (default: unlimited). Examples:

```bash
health-data/health-data.sh export-json HKCategoryTypeIdentifierSleepAnalysis ~/Downloads/export.zip --limit 5
```

```bash
health-data/health-data.sh export-json HKQuantityTypeIdentifierStepCount ~/Downloads/export.zip --limit 20 --out ~/Documents/step-records.json
```

# Advanced filtering
Because the output from `export-json` is valid JSON, use `jq` for additional insights:

```bash
health-data/health-data.sh export-json HKQuantityTypeIdentifierStepCount ~/Downloads/export.zip --limit 50 \
  | jq '[.[] | {value, startDate}]'
```

Combine `jq` selectors (like `map(select(.unit == "count"))`) to focus on specific fields without writing additional parsing logic.

# Examples
- "What record types did my Health export include?" → `health-data.sh list-types ~/path/to/export.zip`
- "Show me step totals and sleep breakdown for my export" → `health-data.sh summary ~/path/to/export.zip`
- "I want the raw step records for the last week" → `health-data.sh export-json HKQuantityTypeIdentifierStepCount ~/path/to/export.zip --limit 100` and pipe through `jq '.[].startDate | select(startswith("2026-03"))'`
- "Save a slice of the export to a local file" → `health-data.sh export-json HKQuantityTypeIdentifierStepCount ~/path/to/export.zip --limit 50 --out ~/Documents/step-records.json`

# Troubleshooting
- **`no such file or directory`**: Ensure the export path points to either apple_health_export/export.xml or the zipped export produced by Apple Health.
- **`zip ... does not contain export.xml`**: Re-export from the Health app—sometimes partial exports omit the XML if interrupted.
- **Missing dependencies**: Install `xmlstarlet`, `jq`, and `unzip` via Homebrew (`brew install xmlstarlet jq unzip`).
