# Test Cases

Use these cases for manual QA, smoke tests, or acceptance checks.

## Case 1: Weekly Menu Plus Pantry Snapshot

Input shape:
- two-person household
- weekly menu with repeated breakfast and three dinners
- explicit low eggs and milk
- tissues nearly empty

Expected behavior:
- separate fresh meal pressure from household staple pressure
- route urgent breakfast gap items ahead of non-urgent stock-up
- avoid turning tissues into a same-day emergency if coverage still exists

## Case 2: Mixed Urgency Basket

Input shape:
- dinner ingredient missing tonight
- detergent and paper goods also getting low
- user wants one answer, not three disconnected carts

Expected behavior:
- recommend a clean split only if it materially helps
- put tonight's gap on fast local path
- push stock-up goods to a patient route when appropriate

## Case 3: Duplicate-Buy Risk

Input shape:
- recent purchase screenshot shows a large rice bag last week
- user adds rice again because of a promotion

Expected behavior:
- flag rice as likely duplicate buy
- downgrade promo appeal
- keep focus on real low-stock items

## Case 4: Small Household Over-Stocking

Input shape:
- one-person household
- large PDD family packs look cheapest
- no strong storage capacity

Expected behavior:
- penalize oversized packs
- explain why unit price is not the only metric
- prefer moderate replenishment depth

## Case 5: Three-Plan Output

Input shape:
- user explicitly asks for lowest total, fastest, and lowest-friction plans
- basket includes urgent fresh items plus non-urgent pantry goods

Expected behavior:
- provide all three plans
- keep each plan executable
- make one default call instead of leaving the user with a tie
