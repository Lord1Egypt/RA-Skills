# Eval 07: Cost Summary Query

## Setup Context
Service history in home-data.json includes:
- Main House: HVAC tune-up $175 (March 2026), plumbing repair $150 (Feb 2026), dryer vent cleaning $95 (Jan 2026)
- Rental: AC capacitor $180 (Jan 2026), water heater flush (DIY, no cost), gutter cleaning $120 (March 2026)

## Input
"How much have I spent on maintenance this year?"

## Expected Behavior
1. Reads from home-data.json to pull all 2026 service records with costs
2. Groups spending by property
3. Shows per-service line items with dates
4. Shows property subtotals
5. Shows grand total
6. Notes that one service (water heater flush, DIY) has no cost logged
7. Mentions the visit count alongside totals (e.g., "$420 across 2 service calls")

## What to Watch For
- Does it group by property?
- Does it note the missing cost entry?
- Does it include visit counts?
- Is the math correct?
- Does it avoid counting DIY/$0 items in a misleading way?
