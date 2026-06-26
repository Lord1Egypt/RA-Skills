# india-tax-helper

SKILL.md is the primary interface. This README is for developers/maintainers.

## Status: FY 2026-27 rules verified

- Source: Income Tax Department official portal (`return-applicable-1` page for AY 2026-27)
- Verified at: 2026-05-04
- Rules file: `references/fy-2026-27/rules.verified.json`

## Scripts

All scripts are deterministic, JSON-in/JSON-out, and fail closed when rules are unverified.

| Script | Purpose | Key inputs |
|--------|---------|-----------|
| `tax_intake_normalizer.py` | Parse free text, extract signals | `--text` |
| `salary_tds_refund.py` | Salary tax, rebate, cess, refund | `fy`, `regime`, `gross_salary`, `tds`, `deductions`, `age` |
| `deductions_estimator.py` | Chapter VIA deductions (old regime) | `regime`, `80c`, `80d_*`, `24b`, etc. |
| `fd_rd_tds.py` | FD/RD TDS + 15G/15H indicator | `fy`, `interest_income`, `regime`, `age_category` |
| `capital_gains_estimator.py` | Equity, debt MF, general CG tax | `fy`, `asset_type`, `gain`, `holding_days` |
| `full_tax_estimator.py` | End-to-end: salary + other + FD + CG | All of the above combined |
| `test_suite.py` | Validation suite — run after changes | None (self-contained) |

## Running tests

```bash
cd scripts
python3 test_suite.py
```

## Adding a new FY

1. Create `references/fy-YYYY-YY/` folder
2. Fetch official slab page and populate `rules.verified.json`
3. Update `source-manifest.json` with verified sources
4. Run `test_suite.py` (update expectations for new slabs)
5. Update `lifecycle-calendar.md` with new due dates

## Known limitations

- Capital gains exemption (e.g., 1.25L LTCG exemption for equity) is applied in `full_tax_estimator.py` but not in `capital_gains_estimator.py` (which is rate-only)
- Surcharge computation is simplified (does not handle marginal relief precisely)
- 80GG rent deduction requires `income_before_80gg` which users may not have handy
- New regime deductions are limited to 80CCD(2) and 80CCH only
