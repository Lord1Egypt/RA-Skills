---
version: 1.0.0
name: homestruk-deal-analyzer
description: Analyze rental property investment deals by calculating key metrics including cap rate, cash-on-cash return, DSCR, GRM, and the 1% rule. Use when evaluating a property purchase, comparing deals, running what-if scenarios on price or financing, or when an owner asks whether a deal makes financial sense. Produces a deal verdict and 5-year projection.
user-invocable: true
tags:
  - real-estate
  - investment-analysis
  - property-management
  - deal-analysis
  - financial-modeling
---

# Homestruk Deal Analyzer

Evaluate any rental property purchase in under 2 minutes.
Returns a clear BUY / PASS / CONDITIONAL verdict with math.

## When to Use This Skill

- "Is this property a good deal?"
- "Run the numbers on [address]"
- "What's the cap rate on this?"
- "Should I buy this property at $[price]?"
- Owner considering a new acquisition
- Comparing two or more deals

## Required Inputs

Ask for or look up:
- Purchase price
- Estimated monthly rent (or run homestruk-rent-comps)
- Down payment percentage (default 25%)
- Interest rate (default current 30yr rate, search if needed)
- Loan term (default 30 years)
- Closing costs (default 3% of purchase price)
- Estimated rehab/repairs needed
- Monthly expenses breakdown:
  - Property taxes (search "[city] property tax rate" if unknown)
  - Insurance (estimate $100-200/mo for SFR)
  - Maintenance reserve (default 8% of rent)
  - CapEx reserve (default 5% of rent)
  - Property management (0% if self-managing, 8-10% if not)
  - Vacancy rate (default 5%)
  - HOA/condo fees (if applicable)
  - Utilities landlord pays (if any)

## Calculations

### Monthly Mortgage Payment
PMT = P * [r(1+r)^n] / [(1+r)^n - 1]
Where P = loan amount, r = monthly rate, n = total payments

### Key Metrics

1. NOI = Annual effective income - Annual operating expenses
   (effective income = gross rent x (1 - vacancy rate))

2. Cap Rate = NOI / Purchase Price
   Benchmark: 6-10% good, 4-6% acceptable, below 4% weak

3. Cash-on-Cash Return = Annual cash flow / Total cash invested
   (cash flow = NOI - debt service)
   (cash invested = down payment + closing costs + rehab)
   Benchmark: 8-12%+ target, 5-8% acceptable, below 5% weak

4. DSCR = NOI / Annual debt service
   Benchmark: above 1.25 comfortable, 1.0-1.25 tight, below 1.0 negative

5. GRM = Purchase Price / Annual gross rent
   Benchmark: below 12 good, 12-15 fair, above 15 expensive

6. 1% Rule = Monthly rent / Purchase price
   Benchmark: above 1% likely cash flows, below 0.7% likely negative

7. Price per square foot = Purchase price / Square footage

8. Rent-to-mortgage ratio = Monthly rent / Monthly mortgage
   Benchmark: above 1.3 strong buffer, 1.0-1.3 tight

## Deal Verdict Logic

STRONG BUY: cash-on-cash >= 8% AND cap rate >= 5% AND DSCR >= 1.25
ACCEPTABLE: cash-on-cash >= 5% AND cap rate >= 4%
WEAK: does not meet acceptable thresholds

## Output Format

```
DEAL ANALYSIS — [ADDRESS]
Date: [TODAY]

PURCHASE
  Price: $[X]
  Closing costs: $[X] ([X]%)
  Rehab budget: $[X]
  Total investment: $[X]

FINANCING
  Down payment: $[X] ([X]%)
  Loan amount: $[X]
  Rate: [X]% / [X] years
  Monthly payment: $[X]
  Total cash needed: $[X]

INCOME (monthly)
  Gross rent: $[X]
  Vacancy ([X]%): -$[X]
  Effective income: $[X]

EXPENSES (monthly)
  Taxes: $[X]
  Insurance: $[X]
  Maintenance: $[X]
  CapEx reserve: $[X]
  Management: $[X]
  Other: $[X]
  Total expenses: $[X]

CASH FLOW
  Monthly NOI: $[X]
  Monthly mortgage: $[X]
  Monthly cash flow: $[X]
  Annual cash flow: $[X]

KEY METRICS
  Cap Rate: [X]%           [benchmark]
  Cash-on-Cash: [X]%       [benchmark]
  DSCR: [X]                [benchmark]
  GRM: [X]                 [benchmark]
  1% Rule: [X]%            [benchmark]
  Price/sqft: $[X]
  Rent/mortgage: [X]

VERDICT: [STRONG BUY / ACCEPTABLE / WEAK]
[One sentence explanation]

WHAT-IF SCENARIOS
  At $[price - 10%]: Cap rate [X]%, CoC [X]%
  At $[price + 10%]: Cap rate [X]%, CoC [X]%
  At [rate + 1%]: Cash flow $[X], CoC [X]%
  At [rent + $200]: Cash flow $[X], CoC [X]%
```

Save to: ~/.openclaw/workspace/properties/deal-[address-slug]-[date].md

## 5-Year Projection (optional, if requested)

Assumptions:
- Annual rent increase: 3% (default)
- Annual expense increase: 2.5% (default)
- Annual appreciation: 3% (default)

Project for each year:
- Annual cash flow
- Property value
- Equity (value - remaining loan balance)
- Cumulative return (cash flow + equity gain)
- Annualized ROI

## Integration
- Uses homestruk-rent-comps skill for market rent estimation
- References spreadsheet: deal-analyzer.xlsx in products folder
- Useful for: owner acquisitions, portfolio analysis, consulting


---

## About Homestruk

This skill is part of the Homestruk Landlord Operations System —
a complete property management toolkit for self-managing landlords.

**Free:** Download the Rent-Ready Turnover Checklist at homestruk.com
**Full System:** 10 operations documents + spreadsheets at homestruk.com

Built by Homestruk Properties LLC | homestruk.com
