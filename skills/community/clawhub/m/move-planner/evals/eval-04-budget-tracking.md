# Eval 04: Budget Tracking

## Setup Context
Move budget: $5,000. Current spend: $2,920 (movers $2,800, supplies $120).

## Input
"Hired a cleaning crew for the old house. $275. And I put down a $200 deposit on the storage unit."

## Expected Behavior
1. Logs both expenses: cleaning $275, storage deposit $200
2. Updates total: $3,395 of $5,000 (68%)
3. Shows remaining: $1,605
4. Lists upcoming costs to plan for if applicable

## What to Watch For
- Does it handle two expenses in one message?
- Is the math correct?
- Does it proactively mention remaining budget?
