# Eval 06: Buy/Sell Transaction Milestones

## Input
"Inspection on the new house is March 25. Appraiser is coming April 5. Our house goes under contract this Friday."

## Expected Behavior
1. Logs buying milestones: inspection March 25, appraisal April 5
2. Logs selling milestone: under contract as of Friday
3. Updates the sell-and-buy timeline accordingly
4. Confirms all captured dates
5. May note any tasks that should happen between now and the inspection (e.g., "review inspection report and negotiate repairs within your contingency window")

## What to Watch For
- Does it handle both buy and sell milestones in one message?
- Does it connect milestones to downstream tasks?
- Does it update the transaction status (selling: under contract)?
