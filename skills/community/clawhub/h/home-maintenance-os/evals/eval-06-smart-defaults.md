# Eval 06: Smart Maintenance Defaults on New Appliance

## Input
"Just had a new Rheem 50-gallon gas water heater installed at the main house today."

## Expected Behavior
1. Logs the appliance: Rheem water heater, 50-gal gas, Main House, installed today
2. Automatically attaches standard maintenance reminders:
   - Annual tank flush (next due in ~12 months)
   - Anode rod inspection (every 2-3 years, next due in ~2 years)
   - T&P relief valve test (annually, next due in ~12 months)
3. Presents the defaults clearly and offers to adjust
4. Asks about warranty info since it's a new install
5. Writes all of this to home-data.json

## What to Watch For
- Does it pull from built-in knowledge automatically (not wait to be asked)?
- Does it present the schedules as adjustable defaults, not rigid rules?
- Does it prompt for warranty info on a new install?
- Does it write to the data file?
