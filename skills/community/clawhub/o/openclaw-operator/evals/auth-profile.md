# Eval — auth profile missing

## Expectation
The skill must distinguish global provider config from agent-level auth profile config.

## Pass criteria
- Explains the two-layer auth model clearly
- Points to `auth-profiles.json` as the missing link
- Verifies via gateway error logs
- Does not imply that global config alone is sufficient
