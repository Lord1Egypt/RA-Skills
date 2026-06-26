---
name: health-records-ingest
description: "Interview a user and build a personalized health-record system around their goals, reports, and tracking needs. Use when someone wants to organize their health data, create a reusable health workspace, ingest PDFs/screenshots/scans, define what to track over time, and maintain a durable system with raw files, readable notes, structured data, and summaries."
---

# Health Records Ingest

Build a personal health knowledge system around the user, not just around files.

## Workflow

1. Interview the user first.
2. Confirm privacy, processing, and storage boundaries before touching files.
3. Define the health workspace structure around their goals.
4. Preserve incoming raw files.
5. Create readable extractions.
6. Add or update structured tracking files.
7. Maintain dashboard/history summaries.
8. Recheck unclear extractions without overwriting the original note.

## Interview first

Before building the system, ask only the minimum useful questions needed to shape it.

Default interview topics:
- What is the goal: baseline tracking, fitness transformation, disease management, annual records, or lab organization?
- What file types will arrive: blood tests, scans, prescriptions, DEXA, wearables, Apple Health exports, doctor notes?
- What should be tracked over time?
- What summaries matter most: abnormalities, trends, doctor-ready summaries, supplements, symptoms, activity?
- Does the user want a simple structure or a more detailed longitudinal system?
- Should processing be strictly local? Default to **local-only** unless the user explicitly approves another path.
- Are third-party OCR, cloud extraction, or web APIs allowed? Default to **no external upload without explicit consent**.
- Where should files live, and what retention/deletion expectations does the user want?

If the user already provided enough context, do not over-interview. Start building.

## Build the system around the user

Create the smallest useful system first, then expand.

Default folder layout:

```text
health/
  reports/      # original PDFs
  scans/        # original images / photos
  notes/        # one extracted Markdown note per report
  data/         # JSON and CSV tracking files
  history/      # chronological summaries
  dashboard/    # latest snapshot + abnormalities summary
```

Adapt this when needed. Example additions:
- `health/prescriptions/`
- `health/symptoms/`
- `health/medicines/`
- `health/doctors/`
- `health/wearables/`

## Rules

- Preserve raw sources.
- Default to **local-only processing**.
- Do **not** upload health files, screenshots, or extracted data to third-party OCR/API services unless the user explicitly approves it for this workflow.
- If local extraction is incomplete, ask before using any cloud or external processing path.
- Use date-first filenames where possible.
- Keep one Markdown note per source report, plus `*-recheck.md` only when needed.
- Use simple status labels such as `in_range`, `low`, `high`, `reactive`, `pending`.
- Keep summaries traceable back to the original file path.
- Be explicit about storage location and retention when setting up a new system.
- Do not present extracted content as medical advice.
- Prefer incremental updates over reorganizing everything repeatedly.

## What to capture

### Lab reports
- test name
- value
- units
- reference range if visible
- status

### Body composition
- weight
- body fat %
- fat mass
- muscle mass
- BMI
- visceral fat
- water metrics if present
- segmental breakdown if present

### Imaging / ECG / scans
- study type
- impression / conclusion
- notable numeric values
- normal vs abnormal summary

## Recheck behavior

If a PDF pass misses something but later screenshot/manual review confirms it:
- create or update a `*-recheck.md` note
- say exactly what changed
- preserve the earlier extraction note

## References

Read `references/workflow.md` for the full four-layer method, interview guidance, naming conventions, and update process.
Read `references/examples.md` for concrete file examples and summary patterns.
