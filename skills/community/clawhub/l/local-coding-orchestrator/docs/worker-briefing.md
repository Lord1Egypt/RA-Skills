# Worker briefing guidance

This document defines how worker briefs should be shaped in constrained local environments.

## Principle

When shell policy is restrictive, do not start with broad context loading and complex command composition.
Start with the smallest useful repo probe.

## Preferred order

1. verify repo path access
2. inspect minimal directory structure
3. check whether build/test execution is realistically possible
4. only then attempt deeper implementation or review actions

## Avoid

- complex multi-line `powershell -Command` strings
- unnecessary shell batching just to gather context
- profile-dependent shell setup
- expensive probing before basic repo access is confirmed

## Prefer

- TaskFile prompt handoff
- filesystem inspection when available
- concise explanations of policy or sandbox limits
- early environment blocking when execution cannot proceed
