# Workforce Data Spec

## Workbook Structure

Each uploaded Excel workbook follows a structured layout determined by its file type.
File type is always identified from **row 1 content** (report name), never from the filename.

### Active Files (在职明细)

1. **Rows 1-6 = metadata rows**
   - Row 1: report name, fixed value `Overseas Active Employee Report`
   - Row 4: `Effective Date | <date>` → used as `snapshot_date`
   - Rows 2-3, 5, 6 are ignored
2. **Row 7 = header row**
3. **Row 8+ = data rows**

### Termination Files (离职明细)

1. **Rows 1-7 = metadata rows**
   - Row 1: report name, fixed value `Overseas Terminated Employee Report`
   - Row 4: `Termination Date From | <start_date>` → used as `period_start`
   - Row 5: `Termination Date To | <end_date>` → used as `period_end`
   - Rows 2-3, 6, 7 are ignored
2. **Row 8 = header row**
3. **Row 9+ = data rows**

### Contingent Worker Files (外包人员明细)

1. **Row 1 = report name** containing `Contingent Worker` (e.g. `Overseas Contingent Worker Report`)
2. **Row 2 = header row**
3. **Row 3+ = data rows**
4. Data is always the latest snapshot; no snapshot_date metadata needed

Determine file type only from row-1 content.
Do not infer active / termination / contingent from the filename.

## Supported dataset_type Values

Normalize row-1 report name into one of these logical types:

- `active`
  - accepted keywords: `active`, `在职`, `headcount`
- `termination`
  - accepted keywords: `terminat`, `attrition`, `离职`
- `contingent`
  - accepted keywords: `contingent`, `contractor`, `partner`, `外包`

If `dataset_type` cannot be mapped, stop and report the bad metadata.

## Required Business Fields

### Active Files
- `Employee Type`
- `Region`
- `WD Employee ID`
- `Country/Territory`
- `BG`

### Termination Files
- `Employee Type`
- `Region`
- `WD Employee ID`
- `Country/Territory`
- `BG`
- `Termination Date`
- `Termination Category`

### Contingent Worker Files
- `HQ Employee ID` (or any column containing "Employee" and "ID")
- `WeCom Name` (used to classify worker type by prefix)
- `Country/Territory` (Chinese country names, auto-mapped to English)
- `BG`

## Fixed Enumerations

### Employee Type
- `Regular`
- `Intern`

### Termination Category
- `Terminate Employee > Voluntary`
- `Terminate Employee > Involuntary`
- `Terminate Employee > Others`
- `Terminate Employee > Statutory Termination`

Dashboard 4 displays `Voluntary / Involuntary` as fixed columns. `Others / Statutory` columns are conditional — shown only when data is non-empty.

### Worker Type (Contingent)
Determined by `WeCom Name` prefix:
- `v_` prefix → `Contractor`
- `p_` prefix → `Partner`
- Default (no matching prefix) → `Contractor`

## Regional Scope

### Dashboards 1, 2, 4, 5
Only include:
- `Americas`
- `APAC`
- `EMEA`

Exclude `Mainland China`.

### Dashboard 3
Display in this fixed order:
- `Americas`
- `APAC`
- `EMEA`
- `海外合计`
- `Greater China`
- `海外合计（含试点国内）`

Use `Greater China` as a dedicated block after overseas subtotal.

## BG Mapping

Map raw `BG` values to fixed display columns:

- `IEG` ← `IEG - Interactive Entertainment Group`
- `CSIG` ← `CSIG - Cloud & Smart Industries Group`
- `WXG` ← prefix match `WXG - Weixin Group`
- `TEG` ← `TEG - Technology & Engineering Group`
- `CDG` ← `CDG - Corporate Development Group`
- `PCG` ← `PCG - Platform & Content Group`
- `OFS` ← `Overseas Functional System`
- `S1` ← `S1 - Functional Line`
- `S2` ← `S2 - Finance Line`
- `S3` ← `S3 - HR & Management Line`

If an unknown BG appears:
- continue generating
- record the unknown value in `summary.md`
- keep the fixed layout unchanged

## Contingent Worker Country Mapping

The script has a built-in mapping of 40+ Chinese country names to (English name, Region).
Examples:
- `美国` → `United States of America`, `Americas`
- `日本` → `Japan`, `APAC`
- `英国` → `United Kingdom`, `EMEA`

If an unmapped Chinese country name appears, the original value is preserved.

## Time Rules

- Latest month = max active `snapshot_date`
- Dashboard 1 YoY = latest month vs same month last year
- Dashboard 1 MoM = latest month and previous two months
- Missing comparison months do not block output; mark `数据不完整`

## Attrition Rules

- Subject = `Employee Type = Regular`
- Scope = overseas only, excluding `Mainland China`
- Terminations = rows whose `Termination Date` falls within the selected period
- Attrition rate formula:

\[
Attrition\ Rate = \frac{Terminations}{(Start\ HC + End\ HC)/2} \times 100\%
\]

Use the nearest valid active snapshots to anchor start and end headcount when the exact dates do not align perfectly with the termination date range.
