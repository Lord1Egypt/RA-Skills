# Scenario: Salaried with Capital Gains

Use when user has stock, mutual fund, or other asset sales alongside salary income.

## Equity (STT paid) — Long Term
```json
{
  "fy": "FY-2026-27",
  "asset_type": "equity_stt_paid",
  "gain": 200000,
  "holding_days": 400
}
```
- Classification: Long term (≥ 365 days)
- Exemption: first 1,25,000 of LTCG is tax-free
- Taxable LTCG: 75,000
- Rate: 12.5%
- **Tax: 9,375**

## Equity (STT paid) — Short Term
```json
{
  "fy": "FY-2026-27",
  "asset_type": "equity_stt_paid",
  "gain": 50000,
  "holding_days": 200
}
```
- Classification: Short term (< 365 days)
- Rate: 20% (special rate u/s 111A)
- **Tax: 10,000**

## Debt MF (acquired before 1-Apr-2024)
```json
{
  "fy": "FY-2026-27",
  "asset_type": "debt_mf_pre_2024",
  "gain": 100000,
  "holding_days": 1460
}
```
- Classification: Long term (≥ 1095 days)
- Indexation benefit may apply
- Rate: 20% with indexation OR 12.5% without
- Verify acquisition date before applying

## Debt MF (acquired on/after 1-Apr-2024)
```json
{
  "fy": "FY-2026-27",
  "asset_type": "debt_mf_post_2024",
  "gain": 100000,
  "holding_days": 400
}
```
- Both ST and LT taxed at slab rates
- No indexation, no special rate

## Key documents
- Broker capital gains statement (Trades + P&L)
- AIS/TIS for pre-filled validation
- Form 26AS for TDS on capital gains (if any)
