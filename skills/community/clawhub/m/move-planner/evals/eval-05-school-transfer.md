# Eval 05: School and Kid-Specific Tasks

## Setup Context
Household has 3 kids. Move type is sell-and-buy, relocating to a different school district.

## Input
"I need to handle school stuff for the kids. What do I need to do?"

## Expected Behavior
1. Pulls school-related tasks from the template
2. Lists what needs to happen: request records from current school, enroll at new school, transfer any special programs (IEP, gifted, etc.)
3. Notes any time-sensitive items (enrollment deadlines, records transfer lead time)
4. If the user previously mentioned homeschooling or specific school details, factors those in
5. Offers to track each child's enrollment separately if needed

## What to Watch For
- Does it generate kid-specific tasks, not just generic "notify schools"?
- Does it consider records transfer lead time?
- Is it sensitive to the fact that this is stressful for families?
