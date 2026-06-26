# Eval 01: Log a Service Visit

## Input
"Hey, the Trane XR15 AC at our house got its annual tune-up today. Cool Air Services did it -- cleaned the coils, checked refrigerant, replaced the filter. $175. Guy said everything looks good for another year."

## Expected Behavior
1. Logs a service record with today's date
2. Captures the item (Trane XR15 AC), property (main house / default), contractor (Cool Air Services), work done (coil cleaning, refrigerant check, filter replacement), and cost ($175)
3. Adds Cool Air Services to the contractor directory under HVAC if not already there
4. Notes the "good for another year" comment and sets next service due in ~12 months
5. Confirms what was logged in a clear, scannable format
6. Asks if the user wants to add contractor contact info

## What to Watch For
- Does it capture ALL the details (not just some)?
- Does it auto-create the contractor directory entry?
- Does it set a maintenance reminder based on "another year"?
- Is the confirmation clear and easy to scan?
