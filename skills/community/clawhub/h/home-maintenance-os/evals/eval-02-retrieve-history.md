# Eval 02: Retrieve Service History

## Setup Context
The skill should have prior records including:
- AC serviced on June 15, 2025 by Cool Air Services ($175)
- Furnace serviced on October 12, 2025 by Mike's Heating ($150)
- Water heater flushed on January 8, 2025 (DIY)

## Input
"When was the last time the furnace was serviced?"

## Expected Behavior
1. Returns the most recent furnace service record: October 12, 2025
2. Includes who did the work (Mike's Heating) and what was done (annual tune-up)
3. Includes cost ($150)
4. Mentions when the next service would be due based on frequency
5. Responds conversationally, not in a data dump

## What to Watch For
- Does it return the correct record (furnace, not AC or water heater)?
- Is the response conversational or does it feel like a database query result?
- Does it proactively mention the next due date?
