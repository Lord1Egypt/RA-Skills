# Eval 04: Contractor Lookup

## Setup Context
Contractor directory includes:
- Cool Air Services: HVAC, (555) 123-4567, "Fast, fair pricing, showed up on time"
- Mike's Heating: HVAC/Furnace, no phone on file, "Did a good job but was hard to schedule"
- Dave the Plumber: Plumbing, (555) 987-6543, "Expensive but excellent work"

## Input
"Who do we use for HVAC stuff?"

## Expected Behavior
1. Returns both HVAC contractors (Cool Air Services and Mike's Heating)
2. Includes contact info where available
3. Includes user notes/ratings
4. References past service history (e.g., "Cool Air Services last serviced your AC on June 15")
5. Does NOT return Dave the Plumber (wrong specialty)

## What to Watch For
- Does it filter by specialty correctly?
- Does it include the user's own notes about quality?
- Does it cross-reference service history?
- Does it flag missing contact info (Mike's Heating has no phone)?
