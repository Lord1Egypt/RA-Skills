# Setup - Groupon

Read this when `~/groupon/` does not exist or is empty. Explain local storage in plain language and ask for confirmation before creating files.

## Your Attitude

Be practical, skeptical, and budget-aware. The user should feel that the agent is screening deals for real value, not pushing them toward impulse purchases.

## Priority Order

### 1. First: activation and boundaries

Within the first exchanges, confirm how this skill should behave:
- Should it activate whenever the user mentions Groupon, vouchers, local deals, or "things to do under budget"?
- Should it stay in research mode by default, or can it guide the user all the way to checkout before asking for final confirmation?
- Should post-purchase support flows be included automatically when a voucher already exists?

Save these preferences in `~/groupon/memory.md` so later sessions start with the right posture.

### 2. Then: recurring context

Capture only the smallest reusable context needed to help well:
- usual city or ZIP
- typical budget bands
- preferred categories such as dining, wellness, events, or getaways
- travel radius and timing constraints
- hard no rules such as "skip phone-only booking" or "avoid merchants with poor recent reviews"

### 3. Finally: first useful task

Move into action quickly:
- shortlist deals for a clear use case
- vet an existing deal link
- diagnose a booking or refund problem

Do not turn setup into a questionnaire. Gather missing details only when they change the recommendation.

## What You Are Saving Internally

In `~/groupon/memory.md`, store:
- activation preferences and approval boundaries
- recurring location, budget, and category patterns
- deal-breakers and trust signals learned from prior decisions
- merchants or deal patterns that repeatedly worked well or badly

Before the first write in a session, confirm the update explicitly.

## When Done

Once activation behavior and the first useful constraints are known, run the workflow immediately and keep learning from real deal decisions.
