---
version: 1.0.0
name: homestruk-rent-comps
description: Analyze rental comps and recommend rent pricing for Massachusetts properties. Use when user asks about rent pricing, market rent, comparable properties, rent increases, or what to charge for rent. Searches Zillow, Apartments.com, and Craigslist data to find comparable listings and calculates recommended rent based on property features, location, and market conditions.
user-invocable: true
tags:
  - real-estate
  - property-management
  - rent-pricing
  - market-analysis
  - massachusetts
---

# Homestruk Rent Comps Analyzer

Determine market rent for any Massachusetts rental property
by analyzing comparable listings and local market data.

## When to Use This Skill

- Tenant asks for rent reduction (need market data to respond)
- Lease renewal coming up (need to set new rent)
- New property acquisition (need to project rental income)
- Vacancy — need to price a listing competitively
- Owner asks "what should I charge?"

## How It Works

### Step 1: Gather Property Details

Ask for or look up in ~/.openclaw/shared/properties.json:
- Address and city
- Bedrooms / bathrooms
- Square footage (approximate)
- Property type (SFR, multi-family, condo)
- Key features: parking, laundry, A/C, pets allowed
- Current rent (if renewing)
- Condition: updated / average / needs work

### Step 2: Search for Comps

Run web searches for comparable active listings:

```bash
# Search pattern — run 3-4 queries
web_search "[CITY] MA [BEDS] bedroom apartment for rent"
web_search "[CITY] MA rental listings [BEDS]br"
web_search "apartments.com [CITY] MA [BEDS] bedroom"
web_search "zillow [CITY] MA rentals [BEDS] bed"
```

For each comp found, record:
- Address or listing URL
- Listed rent
- Bedrooms / bathrooms
- Square footage (if available)
- Key features (parking, laundry, pets, A/C)
- Days on market
- Condition notes

### Step 3: Adjust Comps

For each comp, apply adjustments vs the subject property:

| Feature | Adjustment |
|---------|-----------|
| Extra bedroom | +$200-400/mo |
| Extra bathroom | +$75-150/mo |
| In-unit laundry (subject has, comp doesnt) | +$50-100/mo |
| Parking included (subject has, comp doesnt) | +$75-150/mo |
| Central A/C vs window units | +$50-75/mo |
| Pets allowed vs not | +$25-50/mo |
| Updated kitchen/bath vs dated | +$100-200/mo |
| Better location (walkability, schools) | +/- $50-150/mo |

### Step 4: Calculate Recommended Rent

1. Average the adjusted comp rents
2. Calculate the median
3. Recommended rent = average of mean and median
4. Round to nearest $25 or $50

### Step 5: Output the Analysis

Format the report as:

```
RENT COMPS ANALYSIS — [ADDRESS]
Date: [TODAY]

SUBJECT PROPERTY
[Details]

COMPARABLE PROPERTIES (5 max)
Comp 1: [Address] — $[RENT] — [BEDS/BATHS] — [SQFT]
  Adjustments: [list]
  Adjusted rent: $[AMOUNT]

[Repeat for each comp]

ANALYSIS
Average adjusted rent: $[X]
Median adjusted rent: $[X]
Range: $[LOW] - $[HIGH]

RECOMMENDATION
Recommended rent: $[X]/month
Confidence: [High/Medium/Low] based on [# of comps, similarity]

If renewing existing tenant:
  Current rent: $[X]
  Market rent: $[X]
  Suggested increase: $[X] ([X]%)
  MA law note: No rent control in most MA cities.
  30 days notice required for at-will tenancies.
  Lease term increases take effect at renewal.
```

Save the full report to:
~/.openclaw/workspace/properties/comps-[address-slug]-[date].md

## Massachusetts-Specific Notes

- Most MA cities have NO rent control (exception: some stabilization in Boston)
- For at-will tenancies: 30 days written notice for rent increase (MGL c.186 s.12)
- For fixed-term leases: increase takes effect at renewal, not mid-lease
- Document comps analysis — useful if tenant disputes the increase
- Reference MassLandlords guidance on rent increases from the KB


---

## About Homestruk

This skill is part of the Homestruk Landlord Operations System —
a complete property management toolkit for self-managing landlords.

**Free:** Download the Rent-Ready Turnover Checklist at homestruk.com
**Full System:** 10 operations documents + spreadsheets at homestruk.com

Built by Homestruk Properties LLC | homestruk.com
