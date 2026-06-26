---
name: handover-hangover
description: "Archive or generate Handover Hangover batons before the next agent turn"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔄",
        "events": ["message:received", "command:new", "command:reset", "gateway:startup"],
        "requires": { "bins": ["bash"] },
        "always": true,
      },
  }
---

# Handover Hangover Hook

Runs the Handover Hangover watchdog at safe lifecycle boundaries:

- `message:received` — before the next model turn, so an incoming model sees a baton before acting.
- `command:new` / `command:reset` — at explicit session boundaries.
- `gateway:startup` — after Gateway restarts or upgrades.

The handler is intentionally provider-agnostic. It does not inspect model names or call model APIs. It only runs the filesystem watchdog against the configured workspace.
