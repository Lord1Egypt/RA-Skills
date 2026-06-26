# Workflow

## Goal
Create a repeatable health-record system where raw reports stay preserved, extracted findings become readable, trends become trackable, and important abnormalities are easy to review later.

## Core model
Keep four layers:

1. **Raw source layer**
   - untouched original files
   - examples: PDFs, scan photos, screenshots

2. **Readable extraction layer**
   - one Markdown note per report/scan
   - captures the key values in plain English

3. **Structured data layer**
   - CSV/JSON for tracking across time
   - easier for comparisons, filters, graphs, and future automations

4. **Summary layer**
   - dashboard, history, and abnormalities summary
   - optimized for quick human review

## Start with an interview
Do not assume every user wants the same health system.

Ask enough to shape the system:
- What are they trying to manage or improve?
- What kinds of files will they send?
- What categories should exist from day one?
- Which trends matter over time?
- Do they want simple storage, longitudinal tracking, or doctor-ready outputs?
- Should processing remain strictly local?
- Are any third-party OCR/API services allowed, or should external uploads be forbidden?
- What storage and retention expectations should the system follow?

If the user has already provided enough context, skip extra questions and start building.

## Privacy and processing defaults
Health data is sensitive.

Default behavior:
- keep processing local
- preserve raw files in the chosen local workspace
- do not send files or extracted health data to third-party OCR/API providers without explicit user approval
- if local extraction is insufficient, stop and ask before using any external service
- state clearly where files are stored and how long they will be retained if the user asks

## System design principle
Build the smallest useful system first.

Default structure:

```text
health/
  reports/
  scans/
  notes/
  data/
  history/
  dashboard/
```

Then extend only if the user needs it. Examples:
- prescriptions
- symptoms
- doctors
- medicines
- wearables
- nutrition

## Naming convention
Use date-first, type-second naming where possible.

Examples:
- `health/reports/blood-test-2026-03-24.pdf`
- `health/scans/tanita-body-composition-2026-03-05.jpg`
- `health/notes/diagnostic-report-2026-03-23.md`
- `health/data/blood-tests-combined.csv`

## Ingestion flow

### Step 1 — Preserve the raw file
Copy the original file into:
- `health/reports/` for PDFs
- `health/scans/` for images

Do not overwrite the source content.

### Step 2 — Create a Markdown extraction
Create one note in `health/notes/` that includes:
- source path
- date
- provider / test context if known
- key values
- abnormal flags
- short interpretation summary
- caveat that it is not medical advice

### Step 3 — Create structured data
Depending on the file type, add:
- one JSON record for the report
- one CSV row set for trend tracking

Examples:
- body composition → `body-composition.json` + `body-composition.csv`
- blood tests → per-report JSON + combined CSV/JSON

### Step 4 — Update summaries
Update:
- `health/dashboard/README.md`
- relevant `health/history/*.md`
- `health/dashboard/abnormal-markers-summary.md` if there are important flags

## Status conventions
Use simple labels:
- `in_range`
- `low`
- `high`
- `slightly_high`
- `upper_normal`
- `reactive`
- `pending`
- `not_found`

## Recheck rule
If a PDF extraction misses something but later screenshot/manual review confirms it:
- create or update a `*-recheck.md` note
- explicitly state what changed
- preserve the original extraction note
- record whether the missing item was due to OCR/extraction limits

## Good output behavior
A good run should leave the user with:
- preserved original files
- readable notes
- structured tracking files
- an updated dashboard/history layer
- a system that can grow with future records
