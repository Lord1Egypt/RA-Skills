# Eval 08: Proactive Nudge Behavior

## Setup Context
home-data.json contains:
- Main House HVAC filter: quarterly, last replaced 4 months ago (overdue)
- Main House dishwasher warranty: expires in 45 days
- Rental water heater flush: annual, last done 14 months ago (overdue)

## Input
"The plumber came to the rental today and fixed a leaky faucet. $85."

## Expected Behavior
1. Logs the service: leaky faucet repair, Rental, $85, today's date
2. Asks for the plumber's name/contact if not already in the directory
3. Confirms what was logged
4. Appends ONE proactive nudge at the end about the most urgent item
   - The rental water heater flush is overdue by 2 months (most relevant since we're already talking about the rental)
   - OR the HVAC filter at main house (also overdue)
   - Should pick the most contextually relevant or most urgent one
5. Does NOT list all overdue items (that's not a nudge, that's a report)
6. Does NOT nudge about the warranty (45 days out, less urgent than overdue items)

## What to Watch For
- Does the nudge appear as a single line, separated from the main response?
- Does it pick the most relevant/urgent item (not just any random one)?
- Does it avoid listing multiple nudges?
- Is the nudge contextually aware (e.g., preferring the rental item since the conversation is about the rental)?
