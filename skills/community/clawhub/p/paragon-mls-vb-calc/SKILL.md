---
name: paragon-mls-vb-calc
description: "Compare amortized debt, extra payments, chunking/basic acceleration, and advanced velocity banking for a real estate deal. Use when deciding whether chunking or advanced VB makes sense for a property."
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

# Paragon MLS VB Calc

Use the `paragon-mls.vb_calc` MCP tool to compare debt payoff strategies for a deal.

This skill is for deciding whether standard amortization, extra payments, chunking/basic acceleration, or advanced velocity banking makes the most sense.

## Typical use

- compare plain amortization versus aggressive payoff strategies
- test whether chunking actually improves the deal
- estimate interest savings and payoff time before using a HELOC or VB workflow
- pair with Four-Square outputs from the analyze-deal skill

## Example

```bash
mcporter call paragon-mls.vb_calc debtBalance:350000 interestRate:0.05 loanTermYears:30 monthlyIncome:8000 monthlyExpenses:4878.875681 extraPayment:1000
```

## Inputs

- `debtBalance`
- `interestRate`
- `loanTermYears`
- `extraPayment`
- `monthlyIncome`
- `monthlyExpenses`
- `helocRate`
- `advancedRate`
- `helocLimit`
- `chunkMonths`

## Output shape

Returns a comparison table plus JSON for:

- amortized debt
- amortized debt with extra payments
- debt with basic acceleration
- advanced debt acceleration
- savings versus baseline
- a recommendation on whether chunking or advanced VB makes sense

## Notes

- This is a decision tool, not lending advice.
- Use actual income and expense numbers from the target property or operator budget, otherwise the recommendation will be noisy.
