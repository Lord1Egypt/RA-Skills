# Request analysis patterns

## First pass
Ignore noise. Look for the smallest chain that explains success.

## Questions per request
- Is it part of the action or just page noise?
- Does a later request depend on its response?
- Does it create or upload something?
- Does it finalize or publish something?
- Does it poll for readiness?

## Common chain shapes

### Upload flow
1. INIT
2. APPEND or chunk upload
3. FINALIZE
4. STATUS polling
5. publish or schedule mutation

### Direct create flow
1. optional draft creation
2. create/publish mutation
3. readback confirmation

### Schedule flow
1. create payload object
2. submit schedule mutation
3. returned id or scheduled item confirmation

## Field classification
Mark fields as:
- constant
- session-derived
- generated
- returned from previous response
- user input

## Red flags
- analytics endpoints mistaken for workflow calls
- passive timeline refresh calls
- duplicate requests caused by retries
- stale query ids from a different bundle version

## Good output from analysis
A concise table or note set listing:
- stage name
- method
- URL
- required headers
- payload skeleton
- response fields reused later
