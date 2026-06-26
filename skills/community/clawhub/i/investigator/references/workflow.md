# Workflow

## Goal
Map a public online footprint from a username or email and summarize likely profile matches without overclaiming identity.

## Step-by-step
1. Normalize the input.
2. Generate a small set of plausible username variants if useful.
3. Check major public platforms.
4. Record exact matches, likely matches, weak matches, and no-results.
5. Compare public signals across matches.
6. Score confidence using the scoring reference.
7. Return a concise summary.
8. Export JSON if requested.

## Signal types
Useful public signals include:
- exact handle match
- close handle variant
- matching display name
- same linked website
- similar bio wording
- explicit cross-links between profiles
- obvious public avatar similarity

## Evidence discipline
- Facts first.
- Confidence second.
- No dramatic claims.

## Failure handling
If public evidence is thin:
- say that evidence is weak
- avoid claiming the accounts are the same person
