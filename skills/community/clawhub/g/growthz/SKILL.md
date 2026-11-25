---
name: growthz
description: Batch-compute CDC growth z-scores and percentiles for a CSV of child measurements (weight, length, height, head circumference, BMI) using the CDC 2000 LMS tables bundled with the tool. Use when asked to compute growth z-scores or percentiles for a measurements file, analyse growth-chart data for a cohort or survey, or run CDC LMS calculations across many rows at once. Not for eGFR calculation (use egfr-batch), lab-unit conversion (use labunits), de-identification checks (use safeharbor-check), or randomisation lists (use blockrandom). Research and educational tool only; not a medical device.
license: MIT
compatibility: Requires Python 3.10+, standard library only, no dependencies. Installing needs network access to GitHub; the tool itself runs fully offline (CDC tables bundled verbatim).
---

# growthz

## What this tool does

growthz computes CDC growth z-scores and percentiles for a whole CSV of
child measurements at once, using the CDC LMS method and the CDC's own
published LMS tables. For every measure a row has enough inputs for
(weight-, length-, stature-, head-circumference- and BMI-for-age,
weight-for-length/stature) it appends a z-score and a percentile.
Arithmetic against published tables only: no diagnosis, no assessment, no categories, no advice.

## Install

```bash
pip install git+https://github.com/RakTikoo/growthz
```

This provides the `growthz` command. Verify an install with
`growthz check` (reproduces the CDC's published worked example, PASS).

## Run

```bash
growthz convert measurements.csv --out measurements_growthz.csv
```

- Required columns: `sex` (`M`/`F`, `male`/`female`, or CDC codes
  `1`/`2`) and `age_months` (decimals fine). Optional: `weight_kg`,
  `length_cm` (recumbent length), `height_cm` (standing stature),
  `head_circ_cm`, `bmi`. Other columns pass through untouched.
- Length and stature are separate columns on purpose: different
  measurements, different tables; mixing them is a classic source of
  wrong z-scores. BMI is computed from weight + standing height when no `bmi` column is given, never from recumbent length.
- L, M and S are linearly interpolated between table rows for the
  exact age (or length/height); at exact grid points the published
  values are used verbatim. No extrapolation, ever.

## Reading the results

Exit code `0` means the file was processed. The output keeps every
input column and appends `<measure>_z` and `<measure>_percentile` per
computable measure, plus `data_quality_flags` and `notes`. An empty
z-score cell means that measure was not computable for that row; when
an input was present but out of the table's range, `notes` says so.
Rows with z-scores outside the WHO plausibility ranges are counted in
the summary and named in `data_quality_flags` (for example
`weight_for_age_z_outside_plausibility_range(-6..+5)`). A flag is a
statement about the data — check the measurement or its entry — not a judgement about the child, and no interpretation is attached.

A bad row (unrecognised sex, non-numeric age, non-positive
measurement) does not abort the run: the row is written out with the
problem in its `notes` column and a console warning. Exit code `2` is
a structurally broken file — missing `sex` or `age_months` columns, an
empty or missing file — one clean error, no output written.

## Limits

- **Research and educational tool only. Not a medical device.**
  growthz does arithmetic against published CDC tables; it does not
  diagnose, interpret, or recommend anything, and its output must be verified before any clinical use.
- CDC only in v1: the CDC 2000 charts for the United States. The WHO
  Child Growth Standards and WHO 2007 reference are a different reference, not in v1. Do not mix references.
- Age is taken as given: no age computed from dates, no correction for
  gestational age or prematurity, no WHO 0.7 cm length/height
  adjustment.
- Interpolation between grid points is a policy, not a CDC-published
  value; systems using the whole-month row will differ slightly
  between grid points.
- Extreme z-scores are the plain LMS formula's: unlike the WHO
  method, the calculation is not modified beyond ±3 SD, so very extreme measurements produce very extreme z-scores — that is what the plausibility flags are for.
- The reference is a reference: CDC 2000 describes the US reference
  population; a percentile is a position in that population, nothing
  more.
