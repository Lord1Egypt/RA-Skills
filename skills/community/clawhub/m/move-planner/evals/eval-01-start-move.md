# Eval 01: Start a Sell-and-Buy Move

## Input
"We're selling our house and buying a new one. Closing on the new place is June 1, moving day is June 15. Two adults, three kids, one dog."

## Expected Behavior
1. Creates move record: sell-and-buy, closing June 1, move day June 15, household details
2. Offers the sell-and-buy template with due dates calculated from June 15
3. Loads the address change checklist
4. Asks about move budget
5. Presents as adjustable

## What to Watch For
- Does it capture both closing date AND move date?
- Does it note household details (kids, pet)?
- Are due dates calculated correctly from June 15?
