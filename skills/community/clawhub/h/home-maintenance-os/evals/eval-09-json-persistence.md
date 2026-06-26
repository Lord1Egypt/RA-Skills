# Eval 09: JSON Data Persistence

## Input (sequence of 2 messages across simulated sessions)

**Message 1 (Session A):** "We have a Carrier furnace at the main house. Model 59TP6. Installed in 2019. Mike's Heating services it, their number is 555-234-5678."

**Message 2 (Session B -- new conversation):** "When was our furnace installed and who services it?"

## Expected Behavior

**After Message 1:**
1. Creates or updates home-data.json with:
   - Appliance entry: Carrier 59TP6 furnace, Main House, installed 2019
   - Contractor entry: Mike's Heating, HVAC specialty, phone 555-234-5678
   - Standard maintenance schedules attached (annual tune-up, filter changes)
2. Confirms all captured data
3. Writes to home-data.json

**After Message 2 (new session):**
1. Reads home-data.json before responding
2. Returns: Carrier 59TP6, installed 2019, serviced by Mike's Heating (555-234-5678)
3. May mention upcoming maintenance if anything is due
4. Answers accurately from persisted data, not from conversation memory

## What to Watch For
- Does it write to home-data.json after Message 1?
- Does it read from home-data.json at the start of Session B?
- Is the data complete and accurate across sessions?
- Does it link the contractor to the appliance correctly?
