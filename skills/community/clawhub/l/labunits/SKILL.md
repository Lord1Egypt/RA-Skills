---
name: labunits
description: Batch-convert columns of a lab-results CSV between conventional (US) and SI units (glucose mg/dL to mmol/L, creatinine mg/dL to umol/L, HbA1c percent to mmol/mol, BUN to urea; 60 verified analytes), writing the exact factor used next to every converted column. Analytes with no single verified factor are refused with the reason. Use when asked to convert lab values or a lab CSV between conventional and SI units, or convert one lab value. Not for eGFR calculation (use egfr-batch), child growth z-scores (use growthz), de-identification checks (use safeharbor-check), or randomisation lists (use blockrandom).
license: MIT
compatibility: Requires Python 3.10+, standard library only, no dependencies. Installing needs network access to GitHub; the tool itself runs fully offline.
---

# labunits

## What this tool does

labunits converts whole columns of a lab-results CSV between conventional
(US) and SI units, analyte by analyte — the conversion depends on the
molecule, so a generic unit library cannot do it. Every shipped factor
was verified against two independent authorities, and the factor used is
written next to every converted column so each number can be checked by
hand. Analytes with no fixed factor are refused, with the reason
printed. Conversion only: no reference ranges, no flagging, no interpretation.

## Install

```bash
pip install git+https://github.com/RakTikoo/labunits
```

This provides the `labunits` command. `labunits list` shows the shipped
analytes with units and factors; verify an install with `labunits check`
(12 published worked pairs, PASS/FAIL).

## Run

```bash
labunits convert labs.csv --columns glucose,cholesterol_total,creatinine,hba1c,bun --from conventional --to si --out labs_si.csv
labunits convert-one --analyte glucose --value 100 --from conventional --to si
```

- `--columns` takes comma-separated analyte keys; each key must also be
  a column in the file. If the file's column names differ, use
  `--spec spec.csv` (a CSV with header `analyte,column`) instead.
- `--from` and `--to` are required, must differ, and are never guessed:
  `conventional` or `si`. You state which system your file is in.

## Reading the results

Exit code `0` means the conversion ran. The output file keeps the input
columns unchanged and adds, per converted column, a `<column>__<target
unit>` column and a `<column>__factor` column stating the exact factor
or formula used. The printed summary lists each analyte's formula and
target column. Empty cells stay empty. `convert-one` prints the
converted value, the formula, and the factor's source and verification.

Exit code `2` means nothing was converted and no output file was
written: a refused analyte (the error prints why — for example insulin,
whose published factors disagree), an unknown analyte key, a missing
direction or column, or a non-numeric, negative or non-finite cell,
which aborts the run with the row and column named. Nothing is silently
skipped or silently converted.

## Limits

- **Research / educational tool. Not a medical device.** Verify every
  converted value against your laboratory's own reporting before any
  clinical use. No reference ranges are applied, no result interpreted.
- Factors are the published, rounded ones (cholesterol × 0.0259, not the
  unrounded molar value), so a converted value can differ in the last
  digit from a molar-mass-exact calculation; round-tripping is not
  bit-exact.
- Unit systems are stated, not detected. If the file is actually in SI
  and you say `--from conventional`, the tool converts it wrongly and
  the factor column faithfully documents the mistake — check one known
  value by hand first.
- Only 60 analytes ship — each verified twice. Everything else is
  refused by name with the reason, or fails as an unknown analyte.
- HbA1c is converted with the NGSP–IFCC master equation, not a factor.
  BUN and urea are different analytes with different keys: converting
  `bun` produces a deliberately renamed `bun__mmol_L_urea` column, and
  using the BUN factor on a urea column (or the reverse) is the silent
  error this separation exists to prevent.
- One analyte per column, one unit system per file; mixed-unit files
  need one run per system.
