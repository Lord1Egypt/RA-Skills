# Acceptance Checklist

Use this checklist before claiming a phase is done.

## General
- Is there one clear canonical implementation path?
- Are duplicate or broken alternatives removed or intentionally ignored?
- Did you verify instead of assume?

## Frontend / App
- Main page renders
- Navigation works
- Primary actions are visible
- Empty states exist
- Forms can be completed
- Save actions give feedback
- Layout is acceptable on common viewport sizes
- No obvious broken placeholders in key paths

## Config / Integrations
- Provider can be selected
- Credential fields are visible and labeled
- Save works
- Test action exists if promised
- Real integration vs mock/local-only is clearly distinguished

## Code / Structure
- Files are not left in contradictory states
- Large rewrites were consolidated
- Build/run/check performed if available
- Errors found during verification were fixed or documented

## Reporting
Before marking done, state:
- what works
- what was verified
- what remains
- what is blocked externally
