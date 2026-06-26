# Pricing And Approval

Every paid execution must be quoted first.

## Public rule

Show price in `credits`.

If backend returns USD too:
- keep USD as backend settlement detail
- keep credits as user-facing unit

## `one-shot`

Return:
- capability
- estimated credits
- what will be produced
- whether it is synchronous or async

## `project`

Return either:
- phase quote
- or full-project estimate

Preferred fields:
- `estimatedCredits`
- `lineItems`
- `scope`
- `projectId`
- `episodeId` when relevant
- `budgetExceeded`

## Approval behavior

- if the user is clearly asking to proceed after seeing the cost, continue
- if the task is expensive or ambiguous, pause after quote and let the user confirm
- if budget is exceeded, do not silently continue
