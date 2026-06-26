---
name: paragon-mls-analyze-deal
description: "Run spreadsheet-compatible Four-Square rental analysis for Paragon MLS deals. Use when evaluating rental properties for cash flow, NOI, DSCR, appreciation, depreciation, ROI, ROE, and IRR using the Google Sheet model."
metadata:
  openclaw:
    requires:
      bins:
        - node
    mcp:
      paragon-mls:
        command: node
        args:
          - /home/umbrel/.openclaw/workspace/deal-analyst/paragon-mls-mcp/dist/index.js
---

# Paragon MLS Analyze Deal

Use the `paragon-mls.analyze_deal` MCP tool for spreadsheet-compatible Four-Square rental analysis.

This skill is for actual investment underwriting, not just property lookup. It mirrors the major columns and assumptions from the Google Sheet model, including NOI, DSCR, appreciation, depreciation, ROI, ROE, and IRR.

## Typical use

- run full rental underwriting on one or more MLS listings
- compare multiple deals with the same assumptions
- override taxes, insurance, rent, or rehab inputs to match real underwriting notes
- produce sheet-style outputs without manually filling the spreadsheet

## Example

```bash
mcporter call paragon-mls.analyze_deal mlsNumbers="201918514" systemId="globalmls" holdingPeriodYears:5 downPaymentPct:0.25 interestRate:0.07
```

## Common inputs

- `mlsNumbers` (required)
- `systemId`
- `holdingPeriodYears`
- `offerPricePct`
- `downPaymentPct`
- `interestRate`
- `loanTermYears`
- recurring expense overrides like taxes, insurance, utilities, HOA, lawn, legal/accounting
- income overrides like unit rents, laundry, storage, misc income
- capital stack and tax overrides like closing costs, repair budget, reserve/prepaid, private money lender, land value

## Output shape

Returns:

- a compact comparison table for the requested properties
- a JSON block with the detailed sheet-compatible columns for each deal

## Notes

- Parsed MLS values are only a starting point. For serious underwriting, override rents and expenses with verified numbers.
- If the user specifically wants debt strategy comparison too, chain this with the VB Calc skill.
