# Eval 07: Proactive Nudge -- Critical Items Near Move Day

## Setup Context
Move day is 2 weeks away. Movers booked. But: utilities not set up at new address, mail forwarding not done, address changes at 30%.

## Input
"Finished packing the guest bedroom today. That's 4 rooms done, 3 to go."

## Expected Behavior
1. Acknowledges the packing progress
2. Appends ONE nudge about the most critical outstanding item (utilities not set up at new address is probably most critical with 2 weeks to go)
3. Does NOT list all outstanding items

## What to Watch For
- Does it pick the right priority (utilities > mail forwarding > address changes)?
- Is the nudge a single line?
- Does it balance encouragement (4 rooms done!) with the nudge?
