# Scenario: Salaried with FD/RD

Use when salary questions are mixed with interest income, 15G/15H, bank TDS, or multiple deposits.

## Example: FD interest crosses TDS threshold
```json
{
  "fy": "FY-2026-27",
  "regime": "new",
  "interest_income": 60000,
  "estimated_total_income": 800000,
  "age_category": "non-senior"
}
```
- TDS threshold: 40,000 (non-senior)
- 60,000 > 40,000 → TDS applies @ 10% = 6,000
- Estimated total income 8L < 12L (new regime nil-tax limit)
- **15G eligible: likely yes** (income below basic exemption)

## Example: Senior citizen, multiple FDs
```json
{
  "fy": "FY-2026-27",
  "regime": "old",
  "interest_income": 80000,
  "estimated_total_income": 450000,
  "age_category": "senior"
}
```
- TDS threshold: 50,000 (senior)
- 80,000 > 50,000 → TDS applies @ 10% = 8,000
- Estimated total income 4.5L < 5L (old regime nil-tax limit with rebate)
- **15H eligible: likely yes**

## Important notes
- TDS is per bank branch, not aggregated across branches
- AIS aggregates ALL interest across banks — use for ITR reconciliation
- 15G/15H must be submitted to each deductor (bank branch)
- Interest is taxed at slab rate, not special rate
- 80TTA: savings interest deduction 10,000 (non-senior, old regime only)
- 80TTB: deposit interest deduction 50,000 (senior, old regime only)
