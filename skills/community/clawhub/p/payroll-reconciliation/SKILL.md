---
name: Payroll GL Reconciliation
slug: payroll-reconciliation
version: 1.0.0
description: >
  Reconcile QuickBooks Online payroll GL accounts against payroll provider
  reports (Gusto, ADP, Paychex) across 12 categories. Produces an 8-tab Excel
  workbook covering discrepancies, 941 tax recon, W-2 box verification,
  headcount, per-employee cost, and CDC logging. Integrates with
  the Month-End Close pipeline.
tags:
  - payroll
  - accounting
  - reconciliation
  - qbo
  - excel
  - 941
  - w2
negative_boundaries:
  - Bank statement reconciliation → use bank-reconciliation-agent skill
  - Broad P&L variance analysis → use pl-deep-analysis skill
  - Payroll tax preparation or filing advice → requires CPA review
  - Multi-entity payroll consolidation → not supported
---

# Payroll GL Reconciliation Skill

## What This Skill Does

Reconciles QuickBooks Online payroll GL accounts against payroll provider reports
(Gusto, ADP, Paychex) to catch missed journal entries, manual adjustments, and
tax filing discrepancies before they become audit findings or payroll tax penalties.

**Use when:**
- Closing a period and payroll GL needs to match the payroll register
- Preparing for 941 filing — verify GL matches what was reported
- W-2 season — build per-employee annual totals for box verification
- Client has a new payroll provider — validate initial period's entries
- Controller flagged unexplained payroll variance in the P&L

**Do NOT use when:**
- You need bank statement reconciliation → use `bank-reconciliation-agent`
- You need broad P&L variance analysis → use `pl-deep-analysis`
- You need payroll tax preparation or filing advice → CPA review required
- You need multi-entity payroll consolidation (not supported)

---

## Script Location

```
scripts/pipelines/payroll-reconciliation.py
```

---

## Quick Usage

```bash
# Monthly reconciliation
python3 scripts/pipelines/payroll-reconciliation.py \
  --slug CLIENT_SLUG \
  --month 2026-03 \
  --payroll-file ~/Downloads/gusto-march-2026.csv

# Quarterly 941 reconciliation
python3 scripts/pipelines/payroll-reconciliation.py \
  --slug CLIENT_SLUG \
  --quarter 2026-Q1 \
  --payroll-file ~/Downloads/gusto-q1-2026.csv \
  --form-941-file ~/Downloads/941-q1.csv

# Annual W-2 helper
python3 scripts/pipelines/payroll-reconciliation.py \
  --slug CLIENT_SLUG \
  --year 2026 \
  --payroll-file ~/Downloads/gusto-annual-2026.csv \
  --w2-mode

# Custom date range
python3 scripts/pipelines/payroll-reconciliation.py \
  --slug CLIENT_SLUG \
  --start 2026-01-01 --end 2026-06-30 \
  --payroll-file ~/Downloads/h1-2026.csv

# Provider analysis only (no QBO connection needed)
python3 scripts/pipelines/payroll-reconciliation.py \
  --slug CLIENT_SLUG \
  --month 2026-03 \
  --payroll-file ~/Downloads/adp-report.csv \
  --skip-gl

# Custom output directory
python3 scripts/pipelines/payroll-reconciliation.py \
  --slug CLIENT_SLUG \
  --month 2026-03 \
  --payroll-file ~/Downloads/report.csv \
  --out ~/Desktop/reports
```

---

## Arguments

| Argument | Required | Description |
|---|---|---|
| `--slug` | Yes | Client QBO slug identifier |
| `--payroll-file` | Yes | Path to payroll provider CSV |
| `--month` | One of | YYYY-MM for single month |
| `--quarter` | One of | YYYY-Q1 through YYYY-Q4 |
| `--year` | One of | Full year (YYYY) for annual/W-2 |
| `--start` / `--end` | One of | Custom range (YYYY-MM-DD) |
| `--form-941-file` | No | Form 941 CSV for quarterly tax recon |
| `--w2-mode` | No | Enable full W-2 box verification output |
| `--skip-gl` | No | Skip QBO GL pull — provider analysis only |
| `--sandbox` | No | Use QBO sandbox environment |
| `--threshold` | No | Discrepancy threshold (default: $1.00) |
| `--out` | No | Output directory (default: current dir) |

---

## Provider Auto-Detection

The script auto-detects the payroll provider from CSV headers:

| Provider | Detection Signature |
|---|---|
| **Gusto** | Headers contain `Check Date` + `Gross Earnings` |
| **ADP** | Headers contain `Pay Date` + `Total Gross` |
| **Paychex** | Headers contain `Check Date` + `Regular Earnings` |
| **Generic** | Fallback — best-effort column matching |

For unsupported formats, rename CSV columns to match any of the above signatures,
or use the Generic fallback with standard column names (Gross, FIT, SIT, etc.).

---

## Reconciliation Categories

The pipeline reconciles **12 payroll categories** between GL and provider:

| # | Category | GL Keywords | 941 Line |
|---|---|---|---|
| 1 | Gross Wages | wages, salaries, payroll-salaries | Line 2 |
| 2 | Federal Income Tax (FIT) | federal withholding, fit, federal tax | Line 3 |
| 3 | State Income Tax (SIT) | state withholding, sit, state tax | — |
| 4 | SS Employer (FICA-SS ER) | social security employer, ss er | Line 5a |
| 5 | SS Employee (FICA-SS EE) | social security employee, ss ee | Line 5a |
| 6 | Medicare Employer (FICA-Med ER) | medicare employer, med er | Line 5c |
| 7 | Medicare Employee (FICA-Med EE) | medicare employee, med ee | Line 5c |
| 8 | FUTA / SUTA | futa, suta, unemployment tax | — |
| 9 | Health Insurance | health insurance, medical, dental | W-2 Box 12C |
| 10 | 401k / Retirement | 401k, retirement, pension | W-2 Box 12D |
| 11 | Workers Compensation | workers comp, wc premium | — |
| 12 | PTO Accrual | pto, vacation accrual, leave accrual | — |

**Discrepancy threshold:** ±$1.00 per category (configurable via `--threshold`).

---

## Excel Output (8 Tabs)

### Tab 1: Reconciliation Summary
- All 12 categories: GL amount vs provider amount vs difference
- MATCH / DISCREPANCY status per category
- Net difference and overall balance status
- Auto-suggested action for each discrepancy

### Tab 2: Category Detail
- GL transactions filtered and grouped by category
- Running total per category
- Full memo, account, and transaction type

### Tab 3: ⚠ Discrepancies
Three sections:
1. **Category discrepancies** — GL vs provider gaps with priority and action
2. **Missed journal entries** — payroll checks with no GL match
3. **Manual GL adjustments** — GL journal entries with no provider match

### Tab 4: Quarterly 941
- Compares provider totals to Form 941 line items
- Line 2 (wages), Line 3 (FIT), Lines 5a/5c (FICA), Line 6 (total taxes)
- Works with or without Form 941 upload (shows provider-only when no form)

### Tab 5: W-2 Helper
- Annual totals per employee in W-2 box format:
  - Box 1 (wages), Box 2 (FIT), Box 3/4 (SS), Box 5/6 (Medicare)
  - Box 12D (401k), Box 12C (health), Box 16/17 (state)
- Grand totals row for easy cross-check against W-3

### Tab 6: Headcount
- Active employee count per month
- New hire names and termination names per period
- Net headcount change month-over-month

### Tab 7: Per-Employee Cost
- Total employer cost per employee (wages + all taxes + benefits)
- Effective tax rate and total cost/wage ratio
- Sorted by highest total cost

### Tab 8: CDC Log
- Month-over-month changes in payroll cost by category
- New hire / termination events
- Discrepancy count changes (new or resolved)
- Flags material swings ≥10%

---

## Output File Naming

```
payroll-recon_{slug}_{period}.xlsx
```

Examples:
- `payroll-recon_sb-paulson_2026-03.xlsx`
- `payroll-recon_willo-salons_2026-Q1.xlsx`
- `payroll-recon_glowlabs_2026.xlsx`

---

## Dependencies

```bash
pip install openpyxl
```

Node.js QBO client (auth token required for GL pull).

---

## CDC Cache

Change data is persisted at:
```
.cache/payroll-reconciliation/{slug}.json
```

Keeps last 24 periods. Delete to reset baseline.

---

## Workflow: Monthly Close Integration

This pipeline integrates with the Month-End Close checklist
(`scripts/pipelines/month-end-close.py`). Run sequence:

1. Get payroll provider report (CSV export from Gusto/ADP/Paychex)
2. Run `payroll-reconciliation.py` for the closed month
3. Review Tab 3 (Discrepancies) — post any missed JEs before closing
4. File Form 941 (quarterly) — use Tab 4 to verify GL matches before filing
5. W-2 season (January) — run with `--year` + `--w2-mode` for Box verification

---

## Form 941 CSV Format

If providing a 941 CSV (`--form-941-file`), the pipeline expects columns:

```
line, amount
```

Example rows:
```
Line 2 - Total wages,  125000.00
Line 3 - Federal income tax withheld,  18750.00
Line 5a - Social security wages,  15500.00
Line 5c - Medicare wages,  3625.00
Line 6 - Total taxes,  37875.00
```

Column names are matched case-insensitively. Extra columns are ignored.

---

## Common Issues

**"QBO CLI error (exit 1)"**
→ Refresh the QBO auth token for this client slug.

**"Payroll file not found"**
→ Verify the path in `--payroll-file`. Use absolute path if needed.

**"Provider detected: Generic"**
→ Column headers didn't match Gusto/ADP/Paychex signatures. Results are best-effort.
→ Rename columns or use the Generic field names listed in the parser section.

**All categories show $0 for GL**
→ GL pull succeeded but no accounts matched payroll keywords.
→ Check QBO account names — they may use custom names. Add keywords to `PAYROLL_ACCOUNT_KEYWORDS`.

**Discrepancy threshold too sensitive**
→ Use `--threshold 5.00` to allow up to $5 variance (useful for rounding-heavy providers).

---

## Architecture Notes

- **All financial math uses `Decimal`** — no float arithmetic anywhere.
- **Provider detection is header-based** — no reliance on file naming conventions.
- **GL categorization is keyword-based** — matches account name + memo combined.
- **Missed JE detection** matches net pay amounts within ±$1 threshold.
- **Manual adjustment detection** flags GL journal entries with no provider counterpart.
- **CDC is cumulative** — each run appends to the slug's JSON cache file.
- **W-2 Box 1** = gross wages minus pre-tax deductions (401k + Section 125 health).
- **W-2 Box 3/5** = gross wages (simplified — doesn't cap SS wage base per check).
  For exact SS wage base cap ($176,100 in 2026), verify high-earner employees manually.
