---
name: linux-security-guardian-post-action
description: Verify action succeeded after execution. Rollback if failed. Per-client/per-server.
---

# Post-Action Verification

## After Every Executed Action

```
1. Verify expected outcome:
   → For chmod: stat the file/dir, check permissions
   → For service start: systemctl is-active <service>
   → For account lock: grep <user> /etc/shadow | cut -d: -f2 | grep "^!"

2. Outcome as expected?
   YES → log success to actions/<client>/<server>/auto-done/<id>.md:
         "YYYY-MM-DD HH:MM | action: <desc> | result: SUCCESS | verified: <how>"

   NO  → log failure:
         "YYYY-MM-DD HH:MM | action: <desc> | result: FAILED | attempting rollback"
         → Execute rollback from actions/<client>/<server>/history/<id>-ROLLBACK.sh
         → Verify rollback succeeded
         → Alert owner of failure

3. Save after-state:
   → actions/<client>/<server>/history/<id>-AFTER.txt

4. Update soul [AUTO-ACTION HISTORY]
```
