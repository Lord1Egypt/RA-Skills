# Summary + Handoff

## Cycle summary
Every cycle should summarize:
- current state (`running`, `waiting-human`, `closed`)
- what changed
- what stayed blocked
- next step or required human action

## Waiting-human
If the project stops because only a human decision remains, the loop should say so explicitly and point to the pending decision backlog.

## Closed
If the project is done, the loop should say so explicitly and recommend disabling the cron.

## Fallback
If live delivery is unavailable, the handoff still has to exist in local project artifacts.
