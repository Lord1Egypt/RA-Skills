# Scenario: Salaried Basic

Use for users asking only about salary, Form 16, employer declaration, and ITR basics.

## Example: New regime, no other income
```json
{
  "fy": "FY-2026-27",
  "regime": "new",
  "gross_salary": 1200000,
  "deductions": 0,
  "tds_salary": 50000
}
```
- Taxable: 11,25,000 (after 75,000 standard deduction)
- Base tax: 52,500
- Rebate 87A: 52,500 (full, since taxable ≤ 12L)
- **Total tax: 0** → full TDS refund of 50,000

## Example: Old regime with 80C
```json
{
  "fy": "FY-2026-27",
  "regime": "old",
  "age": 30,
  "gross_salary": 1200000,
  "deductions": 150000,
  "tds_salary": 80000
}
```
- Taxable: 10,00,000 (after 1.5L deductions + 50K standard)
- Base tax: 1,12,500 (12,500 + 1,00,000)
- Cess: 4,500
- **Total tax: 1,17,000** → additional 37,000 payable

## Key forms
- Form 12BB: declare investments/HRA to employer
- Form 16: employer TDS certificate (due by 15-Jun)
- ITR-1: if income ≤ 50L, only salary + 1 house + interest + LTCG ≤ 1.25L
