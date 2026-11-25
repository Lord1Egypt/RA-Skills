# Paycheck Withholding — Reference

## 1. Why a "big refund" is a failure signal
A refund is your own money returned without interest. The average US
refund hovers around $3,000 — that's $250/month of take-home pay you
lent the Treasury at 0%. In a 4% HYSA, a steady $3,000 loan costs
~$60/year; the compounding habit costs more. Conversely, surprise
balances due above $1,000 with no safe harbor incur Form 2210
underpayment penalties (interest-rate-based, ~8% annualized in recent
years) plus the cash crunch.

The W-4 is the control surface, and almost nobody re-checks it after
life changes: marriage, a second earner, a raise that crosses a bracket,
a side business, a kid. IRS Publication 15-T computes withholding
per-paycheck; it cannot project your April outcome. This skill does the
projection half the W-4 lacks.

## 2. The projection model

    projected_gross   = YTD_gross + per_pay_gross × paychecks_left
    AGI               = projected_gross + other_income
    taxable           = max(0, AGI − max(standard, itemized))
    liability         = brackets(taxable) − child_tax_credit
    projected_withheld= YTD_withheld + per_pay_withheld × paychecks_left
    delta             = projected_withheld − liability   (>0 refund)

Child tax credit: $2,000 per qualifying child, phased out $50 per $1,000
of AGI above $200k (single/HoH) / $400k (MFJ). Other dependent credit
and education credits are out of scope — conservative by omission.

## 3. Safe harbors (Form 2210)
No underpayment penalty if withholding+estimates cover the **smallest**
of:
- 90% of the current year's tax;
- 100% of last year's tax (110% if last-year AGI > $150k);
- (special: 90% annualized — see quarterly-tax-ranger skill).

Withholding enjoys a timing privilege: it is **deemed paid evenly
through the year regardless of when withheld**. Estimated payments
count only on their quarterly dates. So a December W-4 bump can cure a
January–November shortfall that a December estimated payment cannot.

## 4. The W-4 fix, line by line
- **Step 2** (two jobs / spouse works): checkbox or the table — the
  #1 under-withholding cause in dual-earner households.
- **Step 3** (credits): $2,000/child + $500/other dependent. Adding
  entitled-but-unclaimed credits here reduces withholding by exactly
  that annual amount.
- **Step 4(a)**: other income (side business, interest) — annualized.
- **Step 4(b)**: itemized-deduction overflow above the standard
  deduction built into the default (mortgage interest, SALT up to cap,
  charity).
- **Step 4(c)**: flat extra withholding per paycheck — the precision
  tool this script's verdict prints.

## 5. Bracket constants
2026-shaped single/MFJ/HoH brackets, standard deductions ($15k/$30k/$22.5k
est.), matching the quarterly-tax-ranger skill's constants for
portfolio consistency. All overridable in-source; verify against the
current IRS Rev. Proc. before real filings — annual inflation
adjustments and legislation move these.

## 6. What's deliberately out of scope
- state/local income tax withholding (each state its own W-4 dialect);
- FICA (fixed-rate on wages; Additional Medicare 0.9% reconciles on
  Form 8959 — usually already withheld at the payroll provider);
- SE tax on side income (see quarterly-tax-ranger for that half).

## 7. Practical cadence
Check after every life event and twice a year fixed: mid-June (half the
year's paychecks in hand) and early November (enough paychecks left to
fix anything with ~2 months of runway). Target refund: $0–$300 — small
positive bias absorbs 1099 surprises without lending much.
