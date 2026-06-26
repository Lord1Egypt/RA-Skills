---
name: watchdog-recovery
description: "On gateway startup, recover or re-arm the emergency rollback watchdog from persistent disk"
metadata:
  { "openclaw": { "emoji": "🛡️", "events": ["gateway:startup"], "requires": { "bins": ["node"] } } }
---

# Watchdog Recovery Hook

Runs on OpenClaw gateway startup.

Purpose:
- If rollback is not armed, do nothing.
- If rollback is armed and expired, run `restore-if-armed.mjs` immediately.
- If rollback is armed and not yet expired, respawn the detached watchdog timer for the remaining time.

This hook is the native OpenClaw restart trigger for rollback recovery.
It does not require AI, internet, cron, or any external supervisor.
