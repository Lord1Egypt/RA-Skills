---
name: month-end-close
description: "Orchestrate and validate the full month-end close for a QBO client. Reads client SOP, runs automated close checks, scores each item, proposes journal entries, tracks CDC progress, and outputs a controller-ready Excel workbook. Use when running monthly close for any QBO-connected client. NOT for P&L variance analysis, bank reconciliation only, or budget vs. actual comparisons."
license: MIT
metadata:
  openclaw:
    emoji: "📅"
---

# Month-End Close Checklist — SKILL.md

Orchestrates and validates the full month-end close for a QBO client.
Reads `clients/{slug}/sop.md` to determine which checks apply,
runs automated close checks against QBO, scores each item,
proposes journal entries for missing items, tracks progress with CDC,
and outputs a controller-ready Excel workbook.

---

## Trigger

Use this skill when:
- User says "run close", "month-end close", "close checklist", or "close [client] for [month]"
- Monthly close workflow is needed for any QBO-connected client
- Re-running close to check if open items have been resolved

Do NOT use for:
- P&L variance analysis → use `pl-quick-compare` or `pl-deep-analysis`
- Bank reconciliation only → use `bank-reconciliation`
- Budget vs. actual → use `budget-vs-actual`

---

## Script Location

```
scripts/pipelines/month-end-close.py
```

---

## Usage

```bash
# Standard close run
python3 scripts/pipelines/month-end-close.py --slug sb-paulson --month 2026-03

# Skip GL drill (faster; prepaid/depr/payroll checks have limited data)
python3 scripts/pipelines/month-end-close.py --slug willo-salons --month 2026-02 --skip-gl

# Re-run as items get resolved (CDC tracks progress between runs)
python3 scripts/pipelines/month-end-close.py --slug glowlabs --month 2026-03

# Force fresh QBO pulls (ignore CDC cache)
python3 scripts/pipelines/month-end-close.py --slug sb-paulson --month 2026-03 --rerun

# Custom output directory
python3 scripts/pipelines/month-end-close.py --slug sb-paulson --month 2026-03 --out ~/Desktop/close

# QBO Sandbox
python3 scripts/pipelines/month-end-close.py --slug sb-paulson --month 2026-03 --sandbox
```

---

## Arguments

| Argument | Required | Description |
|---|---|---|
| `--slug` | ✅ | Company slug (must match qbo-client connection) |
| `--month` | ✅ | Close period in YYYY-MM format (e.g. `2026-03`) |
| `--skip-gl` | ❌ | Skip GL pull — faster but prepaid/depr/payroll checks limited |
| `--rerun` | ❌ | Force all checks fresh — ignores CDC state for check selection |
| `--out` | ❌ | Output directory (default: `~/Desktop`) |
| `--sandbox` | ❌ | Use QBO sandbox environment |

---

## Close Checks

| Check | ID | Default | SOP Override |
|---|---|---|---|
| Bank Reconciliation | `bank_recon` | ✅ | Disable: `bank reconciliation: ❌` |
| Trial Balance (D=C) | `trial_balance` | ✅ | Always enabled |
| AP Aging | `ap_aging` | ✅ | Disable: `ap aging: ❌` |
| AR Aging | `ar_aging` | ✅ | **Auto-disabled if SOP says no AR/POS** |
| Prepaid Amortization | `prepaid_amortization` | ✅ | Disable: `prepaid: ❌` |
| Depreciation | `depreciation` | ✅ | Disable: `no fixed assets` |
| Payroll Reconciliation | `payroll_recon` | ✅ | Disable: `payroll: ❌` |
| Revenue Recognition | `revenue_recognition` | ✅ | Disable: `deferred revenue: ❌` |
| Accrued Expenses | `accrued_expenses` | ✅ | Disable: `accruals: ❌` |
| Intercompany Eliminations | `intercompany` | **❌ OFF** | Enable: `multi-entity` or `intercompany: ✅` |

---

## SOP Integration

The pipeline reads `clients/{slug}/sop.md` and parses it for:

- **AR Aging** — auto-disabled if SOP contains: `no accounts receivable`, `POS collection`,
  `AR aging: ❌`, or `AR: Not applicable`
- **Intercompany** — disabled by default; enabled if SOP contains: `multi-entity`,
  `intercompany: ✅`, or `consolidated`
- **Watch notes** — special SOP signals become tab notes in Excel
  (e.g. `interest expense`, `cash burn`, `deferred revenue`, `SAFE`)

### Client SOP Quick Reference

| Client | AR? | Interco? | Notes |
|---|---|---|---|
| `willo-salons` | ❌ No | ❌ No | POS/cash — no AR |
| `glowlabs` | ❌ No | ❌ No | Gaming/Web3; high burn |
| `sb-paulson` | ✅ Verify | ❌ No | Advisory; watch interest expense |
| `opdo` | Check SOP | ❌ No | Review SOP |

---

## Outputs

### Excel Workbook
Saved to `~/Desktop/MonthEndClose_{slug}_{YYYY-MM}_Run{N}.xlsx`

| Tab | Contents |
|---|---|
| **Close Checklist** | Dashboard — PASS/FAIL/ACTION per item + completion % + proposed JE count |
| **Trial Balance** | Full TB with debit/credit validation, per-account rows, totals |
| **Proposed Entries** | All JEs needed for missing/flagged items, sorted HIGH→MEDIUM→LOW |
| **CDC Log** | Status changes between runs — tracks close progress over time |

### Completion Score
```
Completion % = (PASS + N/A) / Total × 100
Close is "READY" when FAIL = 0 and ACTION = 0
```

### Proposed JE Format
Each proposed entry has:
- Debit Account
- Credit Account
- Amount (Decimal; "TBD" if unknown)
- Memo / basis
- Urgency: HIGH | MEDIUM | LOW

---

## CDC (Change Data Capture)

Cache file: `.cache/month-end-close/{slug}-{YYYY-MM}.json`

- First run: full snapshot saved, no delta
- Subsequent runs: shows status changes (FAIL→PASS = "Resolved ✅", PASS→FAIL = "Regressed ⚠️")
- Re-run the pipeline as items are resolved — CDC tracks progress automatically
- Use `--rerun` to force fresh QBO pulls without clearing CDC history

---

## Check Logic Summary

### Bank Recon
Checks `.cache/bank-reconciliation/{slug}.json` for a completed reconciliation matching the
close period end date. If found and `is_reconciled: true` → PASS. If different period or
missing → ACTION NEEDED with command to run.

### Trial Balance
Pulls QBO TB report via `qbo report tb`, sums all debit and credit columns, validates
`|debits - credits| < $0.02`. OUT OF BALANCE → FAIL with proposed suspense entry.

### AP / AR Aging
Scans QBO Balance Sheet for AP/AR account balances. Flags material balances ≥ $500 as
ACTION NEEDED. Proposes accrual entry for largest outstanding item > $2,500.

### Prepaid Amortization
Compares prior-month BS prepaid balances to current. If prior balance > $0 and no GL
activity or balance reduction → ACTION NEEDED with estimated monthly amort entry
(straight-line over 12 months as placeholder).

### Depreciation
Checks fixed asset accounts on BS + scans GL for depreciation/journal entries to
accumulated depreciation accounts. No activity on period with known fixed assets → ACTION NEEDED.

### Payroll Reconciliation
Sums payroll GL accounts for current period, compares to prior P&L payroll total.
Flags if variance > $500 or > 15% month-over-month.

### Revenue Recognition
Checks deferred revenue BS balance for movement. No change with known balance → ACTION NEEDED
with estimated recognition entry (straight-line over 12 months as placeholder).

### Accrued Expenses
Compares accrual account balances prior-vs-current. Flags individual account changes ≥ $1,000
or near-zero reversal from significant balance.

### Intercompany
Only runs if enabled by SOP. Checks for non-zero intercompany/due-to/due-from balances.
Net balance ≠ $0.02 → ACTION NEEDED with elimination entry.

---

## Dependencies

- Python 3.10+ with `openpyxl` (`pip install openpyxl`)
- Node.js QBO client with valid auth tokens
- Client SOP at `clients/{slug}/sop.md` (optional but recommended)
- Completed bank-recon run for `bank_recon` check to PASS

---

## Related Pipelines

| Pipeline | Script | Use |
|---|---|---|
| P&L Quick Compare | `pl-quick-compare.py` | Revenue/expense variance |
| P&L Deep Analysis | `pl-deep-analysis.py` | GL drill-down + accrual proposals |
| Bank Reconciliation | `bank-reconciliation.py` | Must complete before close PASS |

Bank Recon must be run first — `month-end-close` reads its CDC cache to verify completion.

---

## Notes

- All financial math uses Python `Decimal` for precision
- Proposed JE amounts marked "TBD" when determination requires human review (e.g. depreciation schedule)
- SOP parsing is additive: missing SOP = all checks enabled with defaults
- Run multiple times freely — CDC log accumulates close progress history
