# V2 Blueprint

## Positioning

This document records design-only V2 extensions that are not yet part of the
portable runtime contract.

## Candidate V2 features

- toggleable rhythm/nudge behavior
- configurable cadence/frequency
- proactive extension based on schedule and context
- optional daily-memory participation in proactive extension

## Already clarified

- outbound/channel failures should stay outside the portable skill contract
- task/continuity hooks and optional rhythm behavior should stay separate
- provider/model bottlenecks should not be misattributed to the continuity core

## Arbiter ideas for future V2 work

- rank multiple proactive sources before rendering
- keep sleep/rest suppress at highest priority
- never let operational/source-query replies reset absence
- let task/progress hooks outrank rhythm/nudge
- separate cron/info-push frontstage guards from hook/rhythm guards

## Not implemented here

This document is design-only. It is not the source of truth for shipped
runtime behavior; use `SKILL.md`, `README.md`, and the release gate docs for
that.
