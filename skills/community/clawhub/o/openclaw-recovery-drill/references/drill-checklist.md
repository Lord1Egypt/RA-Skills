# Recovery Drill Checklist

## Objective
Prove that OpenClaw can be recovered with acceptable confidence, speed, and operator clarity.

## Minimum drill standard
1. Identify the production workspace to protect.
2. Identify the expected backup source.
3. Restore into a safe non-production path.
4. Confirm key files are present after restore:
   - `SOUL.md`
   - `USER.md`
   - `TOOLS.md`
   - `MEMORY.md` when applicable
   - `memory/`
5. Confirm the restored environment can at least reach a basic startup/inspection state.
6. Record actual restore duration and key failure points.
7. Convert missing steps into automation or a runbook.

## Questions to ask
- What is the newest backup you would trust right now?
- How long would restoration take if the machine died today?
- Who could execute recovery without tribal knowledge?
- Which secrets or external dependencies would block restore success?
- Can the operator distinguish backup existence from restore success?

## Failure patterns
- Backups exist but are stale.
- Backup path is known, restore path is not.
- Restore requires undocumented human memory.
- Workspace is backed up, but config/secrets are not recoverable.
- Recovery has never been timed or rehearsed.
