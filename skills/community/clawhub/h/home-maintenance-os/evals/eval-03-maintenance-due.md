# Eval 03: Maintenance Reminders Check

## Setup Context
The skill should have these maintenance schedules:
- HVAC filter: quarterly, last changed 4 months ago (overdue)
- Dryer vent cleaning: annual, last done 11 months ago (due soon)
- Water heater flush: annual, last done 14 months ago (overdue)
- Gutter cleaning: twice yearly, last done 3 months ago (not due)

Two properties: "Main House" and "Rental"
- HVAC filter and dryer vent are at Main House
- Water heater and gutters are at Rental

## Input
"What maintenance is due?"

## Expected Behavior
1. Groups results by property
2. Flags overdue items clearly (HVAC filter, water heater flush)
3. Flags upcoming items (dryer vent cleaning)
4. Does NOT list items that aren't due yet (gutters)
5. Includes last-completed dates for context
6. Offers to mark items as completed

## What to Watch For
- Does it group by property?
- Does it distinguish between overdue and upcoming?
- Does it skip items that aren't due?
- Is the output scannable without being overwhelming?
