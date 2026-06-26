# Commands — Personal Finance Tracker

Use these local commands when the user provides transaction CSV files and wants a deterministic summary.

## Cashflow Rollup

```bash
python3 cashflow_rollup.py transactions.csv
```

What it gives:
- total inflow and outflow
- net cashflow
- monthly totals
- top spend categories and merchants

## Recurring Charge Scan

```bash
python3 recurring_scan.py transactions.csv
```

What it gives:
- likely monthly or annual recurring charges
- average amount per merchant
- repeat count and cadence hint

## Recommended Workflow

1. Normalize the CSV using `csv-schema.md`
2. Run `cashflow_rollup.py`
3. Run `recurring_scan.py`
4. Summarize with the `review-rhythm.md` output format
5. If debt pressure exists, apply `debt-triage.md`

## Interpretation Rules

- Large positive months do not mean safety if due dates cluster early
- Top merchants matter more when they are recurring
- Category spikes need context before recommending cuts
