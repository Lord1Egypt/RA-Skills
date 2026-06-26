# Scenario: Old vs New Regime Comparison

This is the most common question. Use `scripts/regime_comparator.py`.

## When new regime typically wins
- Moderate income (≤ 15L) with moderate deductions (≤ 3L)
- Any income where taxable after std deduction ≤ 12L (full rebate 87A wipes tax to 0)
- Younger taxpayers without home loans or heavy 80C investments

## Example: 12L salary, no deductions
```json
{"fy": "FY-2026-27", "age": 30, "gross_salary": 1200000, "deductions": 0}
```
- New regime: taxable 11.25L → tax 52.5K → rebate 87A = 52.5K → **total tax: 0**
- Old regime: taxable 11.5L → tax 1,70,000 + cess → **total tax: 1,76,800**
- **New saves 1,76,800**

## When old regime typically wins
- High deductions (> 4-5L) from home loan interest (24b), 80C, 80D, 80E
- Senior citizens with 80TTB (50K deposit interest deduction)
- Very high income where surcharge makes old regime's 37% vs new regime's 25% matter

## Example: 18L salary, 8.5L deductions (home loan + 80C + 80D + 80E)
```json
{"fy": "FY-2026-27", "age": 30, "gross_salary": 1800000, "deductions": 850000}
```
- New regime: taxable 17.25L → **total tax: 1,50,800**
- Old regime: taxable 9L → **total tax: 96,200**
- **Old saves 54,600**

## Break-even rule of thumb (FY 2026-27)
For a 30-year-old:
- At 10L salary: old needs ~3L+ deductions to beat new
- At 15L salary: old needs ~5.5L+ deductions to beat new
- At 20L salary: old needs ~7.5L+ deductions to beat new
- At 25L+ salary: old rarely wins unless deductions are extreme

## Script usage
```bash
python3 scripts/regime_comparator.py \
  --input <(echo '{"fy":"FY-2026-27","age":30,"gross_salary":1500000,"deductions":200000}') \
  --rules references/fy-2026-27/rules.verified.json
```
