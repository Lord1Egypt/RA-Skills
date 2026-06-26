---
name: proposal-service
description: Inspect and create real OpenClaw proposals in public.openclaw_proposals for the current closed-loop workflow. Use for checking duplicate pending proposals and creating trigger-driven proposals based on real workspace logic.
metadata: {"clawdbot":{"notes":["Uses only public.openclaw_* tables","Current implementation supports the stale_missions_alert proposal flow","Wraps the real proposal pattern already present in stale_missions_engine.sh"]}}
---

# Proposal Service

Inspect and create real proposals for the current OpenClaw closed loop.

## Commands

- Check whether the current stale-missions proposal already exists as pending
  `{baseDir}/scripts/proposal-service.sh check-stale-duplicate`

- Create the current stale-missions proposal
  `{baseDir}/scripts/proposal-service.sh create-stale-proposal`

## Notes

- This skill uses the current real proposal pattern already implemented in the workspace.
- It works against `public.openclaw_proposals`.
- It is currently scoped to the `stale_missions_alert` flow.
