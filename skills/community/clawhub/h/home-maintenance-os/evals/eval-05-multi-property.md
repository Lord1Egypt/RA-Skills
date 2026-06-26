# Eval 05: Multi-Property Context Handling

## Setup Context
Two properties on file: "Main House" and "Rental"

## Input (sequence of 3 messages)

**Message 1:** "The dishwasher at the rental broke down. Samsung model DW80R5061US. It's making a grinding noise and not draining."

**Message 2:** "Actually, can you also add that the fridge at the main house is a Whirlpool WRF535SWHZ, bought in 2023? Still under warranty until next March."

**Message 3:** "What appliances do I have on file?"

## Expected Behavior

**After Message 1:**
- Logs the Samsung dishwasher under the Rental property
- Notes the issue (grinding noise, not draining) in the appliance notes or as a service need
- Might ask if the user wants to find a repair contractor or log a service call

**After Message 2:**
- Logs the Whirlpool fridge under Main House
- Records the 2023 purchase date and March warranty expiration
- Might flag that the warranty is expiring soon (within ~12 months)

**After Message 3:**
- Returns a summary grouped by property
- Main House: Whirlpool fridge (warranty until March)
- Rental: Samsung dishwasher (has active issue noted)
- Includes any other appliances previously on file

## What to Watch For
- Does it handle property switching cleanly between messages?
- Does it proactively note the warranty timeline?
- Does the summary correctly group by property?
- Does it carry the dishwasher issue forward as an unresolved item?
