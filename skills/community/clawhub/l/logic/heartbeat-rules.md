# Logic Heartbeat Rules

Use heartbeat to keep `~/logic/` structured, compact, and trustworthy without turning it into a noisy warehouse.

## Source of Truth

Keep the workspace `HEARTBEAT.md` snippet minimal.
Treat this file as the stable contract for logic heartbeat behavior.
Store mutable run state only in `~/logic/heartbeat-state.md`.

## Start of Every Heartbeat

1. Ensure `~/logic/heartbeat-state.md` exists.
2. Write `last_heartbeat_started_at` immediately in ISO 8601.
3. Read the previous `last_reviewed_change_at`.
4. Scan `~/logic/` for files changed after that marker, excluding `heartbeat-state.md` itself.

## If Nothing Changed

- Set `last_heartbeat_result: HEARTBEAT_OK`
- Append a short "no material change" note to the action log
- Return `HEARTBEAT_OK`

## If Something Changed

Only perform conservative maintenance:

- refresh `index.md` if file lists drift
- compact `reflections.md` by merging obvious duplicates
- compact `candidates.md` by grouping repeated candidate rules
- keep `principles.md` stable unless a rule is clearly cross-context, repeatedly validated, and already matured through `candidates.md`
- never auto-promote weak or recent observations into the constitution
- update `last_reviewed_change_at` only after the review finishes cleanly

## Promotion Path

Use this upgrade path:

`reflection -> candidate rule -> stable pattern -> principle`

Do not skip steps.

## Safety Rules

- Most heartbeat runs should do very little
- Prefer append, summarize, or index fixes over large rewrites
- Never delete user-authored reasoning content
- Never reorganize files outside `~/logic/`
- If promotion is ambiguous, leave the rule in `candidates.md`
- Protect the constitution from bloat

## State Fields

Keep `~/logic/heartbeat-state.md` simple:

- `last_heartbeat_started_at`
- `last_reviewed_change_at`
- `last_heartbeat_result`
- `last_actions`

## Behavior Standard

Heartbeat exists to preserve structural quality.
If no important drift is detected, do nothing.
