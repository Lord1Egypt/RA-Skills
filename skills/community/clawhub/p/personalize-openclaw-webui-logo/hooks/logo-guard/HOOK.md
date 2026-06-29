---
name: logo-guard
description: "Re-apply the user's OpenClaw favicon if dist/ was overwritten (e.g. by an openclaw upgrade)."
metadata:
  {
    "openclaw": {
      "emoji": "🦞",
      "events": ["gateway:startup"],
      "requires": { "bins": ["bash"] },
      "handler": "handler.js"
    }
  }
---

# logo-guard

Fires once on every `gateway:startup`. Spawns `check-and-restore.sh` from the
`personalize-openclaw-webui-logo` skill in the background:

- If the dist favicon hash matches `.applied-state` → no-op.
- Otherwise → re-runs `apply-logo.sh <last_set>` to restore the customized logo.

The handler does not block gateway startup; the checker runs detached and
logs to `<skill_dir>/.logo-guard.log`.

Install via `bash <skill>/install-hook.sh`. Disable with `openclaw hooks disable logo-guard`.
