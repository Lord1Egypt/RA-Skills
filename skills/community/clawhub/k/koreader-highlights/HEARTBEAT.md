# HEARTBEAT.md — Periodic Check-in

On each heartbeat, check the following. If nothing needs action, respond `HEARTBEAT_OK`.

## Checklist

- [ ] **New highlights detected.** Check if any `.sdr.json` file in the highlights directory has
  a modification time newer than the last heartbeat. If so, note which books have new highlights
  and how many were added. Inform the user on next interaction.
- [ ] **New books detected.** Check if any new `.sdr.json` files appeared since last heartbeat.
  If so, note the new book titles. Inform the user on next interaction.
- [ ] **Update MEMORY.md.** If new books or highlights were detected, log the discovery in
  `MEMORY.md` with the current date so future sessions have context.

## Rules

- Read-only. Never modify `.sdr.json` files. Only update workspace memory files.
- Do not send proactive messages to the user unless there is something genuinely new to report.
- Keep heartbeat responses minimal. No summaries, no analysis — just detection and logging.