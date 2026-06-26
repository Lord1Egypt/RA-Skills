# CSV Schema — Personal Finance Tracker

Use this when the user shares a bank export, card export, or manual transaction CSV.

If the user pastes raw transactions in chat, convert them into this schema before running summaries or recurring scans.

## Required Columns

| Column | Meaning | Notes |
|--------|---------|-------|
| `date` | Transaction date | Prefer `YYYY-MM-DD` |
| `amount` | Signed amount | Negative for spend, positive for income |
| `merchant` | Payee or payer | Normalize spelling when possible |

## Optional Columns

| Column | Meaning | Why it helps |
|--------|---------|--------------|
| `category` | Spend bucket | Faster summaries and cut lists |
| `account` | Bank, card, or cash source | Helps detect timing risk |
| `note` | Free text | Useful for debt or reimbursement flags |

## Normalization Rules

1. Convert dates to ISO format if possible.
2. Use one sign convention for the whole file.
3. Strip currency symbols and thousands separators from `amount`.
4. Collapse obvious merchant variants like `SPOTIFY*`, `Spotify`, and `SPOTIFY AB`.
5. Remove pending duplicates before trend analysis.

## Minimal Example

```csv
date,amount,merchant,category,account,note
2026-03-01,-14.99,Spotify,Subscriptions,Checking,monthly plan
2026-03-02,-820.00,Rent,Housing,Checking,March rent
2026-03-05,2450.00,Payroll,Income,Checking,main salary
2026-03-06,-58.40,Supermarket,Groceries,Credit Card,weekly shop
```

## When the export is messy

- If there is no `merchant`, use description text.
- If income and spend use separate columns, merge them into one signed `amount`.
- If dates are ambiguous, confirm locale before computing month-level trends.
